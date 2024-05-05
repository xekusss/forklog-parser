#6653090046:AAFGkXVixvHmtzljz9_6ERfgeQ1lZnA4Mek
#1094017014
#@cryptonewssss9999
import requests
from bs4 import BeautifulSoup
import time

def send_to_telegram(text, image_url, bot_token, channel_username):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    data = {"chat_id": channel_username, "caption": text}

    if image_url:
        data["photo"] = image_url

    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f"Изображение и текст отправлены в Telegram.")
    else:
        print(f"Ошибка {response.status_code}. Не удалось отправить изображение и текст в Telegram.")

def send_all_to_telegram(news_list, bot_token, channel_username):
    for news in news_list:
        text, image_url = news
        send_to_telegram(text, image_url, bot_token, channel_username)
        # Добавляем задержку в 1 минуту перед отправкой следующего сообщения
        time.sleep(1)

def parse_and_send_images_with_text(url, bot_token, channel_username, sent_file_path):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find news links and extract text and image URL from them
        news_links = soup.select('a[href*="/news/"]')

        # Read the list of already sent texts from the file
        with open(sent_file_path, 'r') as file:
            sent_texts = set(line.strip() for line in file)

        news_list = []
        news_found = False  # Initialize the news_found variable

        for link in news_links:
            text = link.text.strip()
            image_url = link.find_previous('img')
            if image_url:
                image_url = image_url.get('src')
            else:
                image_url = None

            # Check if the text is not in the sent_texts set
            if text not in sent_texts:
                # Add the text to the sent_texts set
                sent_texts.add(text)
                # Add the news to the news_list
                news_list.append((text, image_url))
                news_found = True  # Set news_found to True when a news is found
                print(f"Новость найдена: {text}")  # Print the found news

        if news_found:
            send_all_to_telegram(news_list, bot_token, channel_username)

            # Write the updated list of sent texts back to the file
            with open(sent_file_path, 'w') as file:
                for sent_text in sent_texts:
                    file.write(sent_text + '\n')
        else:
            print("Новости не найдены")  # Print a message if no news was found
    else:
        print(f"Ошибка {response.status_code}. Не удалось получить страницу.")

if __name__ == "__main__":
    url_to_parse = "Название сайта"
    telegram_bot_token = "токен вашего бота(Bot Father)"
    channel_username = "имя канала"  # Замените на ваше имя канала
    sent_file_path = "sent_news.txt"

    while True:
        parse_and_send_images_with_text(url_to_parse, telegram_bot_token, channel_username, sent_file_path)
        # Добавьте здесь задержку перед следующим запросом, чтобы не нагружать сервер
        time.sleep(7)  # Например, задержка в 10 минут
