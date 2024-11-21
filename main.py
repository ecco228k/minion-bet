import requests
from bs4 import BeautifulSoup
import telebot

# Токен Telegram
TOKEN = 'Ваш токен'

# Создаем бота
bot = telebot.TeleBot(TOKEN)

# Функция для извлечения ссылки на изображение
def get_photo_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Проверка статуса

        # Парсинг HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим div с id lensDiv
        lens_div = soup.find('div', id='lensDiv')

        if not lens_div:
            print("Элемент lensDiv не найден")
            return None

        # Проверяем, есть ли background-image
        style = lens_div.get('style', '')
        if 'background' in style:
            # Ищем URL изображения в background
            start_idx = style.find('url(')
            end_idx = style.find(')', start_idx)
            if start_idx != -1 and end_idx != -1:
                img_url = style[start_idx + 4:end_idx].strip('"\'')
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url  # Приводим относительные пути к абсолютным
                return img_url
    except Exception as e:
        print(f"Ошибка: {e}")
    return None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Отправьте ссылку из Taobao, чтобы получить фотографию.')

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    url = message.text.strip()
    if not url.startswith('http'):
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте корректную ссылку.')
        return
    
    photo_url = get_photo_url(url)
    if photo_url:
        bot.send_photo(message.chat.id, photo_url)
    else:
        bot.send_message(message.chat.id, 'Не удалось найти фотографию. Проверьте ссылку.')

# Запуск бота
bot.polling(none_stop=True)
