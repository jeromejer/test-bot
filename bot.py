import requests
from bs4 import BeautifulSoup
import datetime
import os

def telegram_bot_sendtext(bot_message, bot_token, chat_id):
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={bot_message}'
    response = requests.get(send_text)
    return response.json()

def fetch_website_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Найти заголовок <h2> с конкретным текстом
    header = None
    for h2 in soup.find_all('h2'):
        if "Новые комбо-карты в хомяке на" in h2.text:
            header = h2.text
            break
    
    if header:
        # Найти следующий элемент <ul> после найденного <h2>
        ul = h2.find_next_sibling('ul')
        if ul:
            ul_items = ul.text.strip()
        else:
            ul_items = "Список не найден"
    else:
        header = "Заголовок не найден"
        ul_items = ""

    return header + "\n\n" + ul_items

def main():
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    today = datetime.datetime.now()
    next_day = today + datetime.timedelta(days=1)
    
    date_str = f"{today.day}-{next_day.day} {today.strftime('%b')} {today.year}"
    url = f"https://www.championat.com/cybersport/news-5634642-novye-kombo-karty-v-igre-hamster-kombat-na-{today.day}-{next_day.day}-{today.strftime('%m')}-kartochki-dlya-homyaka.html"
    
    website_data = fetch_website_data(url)
    
    message = f"Информация для {date_str}:\n\n{website_data}"
    result = telegram_bot_sendtext(message, bot_token, chat_id)
    
    print(result)

if __name__ == "__main__":
    main()
