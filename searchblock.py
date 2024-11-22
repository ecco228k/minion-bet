import requests
from bs4 import BeautifulSoup

# URL сайта
url = "https://sunlight.net/catalog"

# Заголовки для обхода блокировок
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# Выполняем GET-запрос
response = requests.get(url, headers=headers)

# Проверяем статус ответа
if response.status_code == 200:
    # Создаём объект BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Находим все карточки товаров
    items = soup.find_all('div', class_='cl-item js-cl-item')
    if items:
        print(f"Найдено {len(items)} товаров:")
        for item in items:
            # Извлекаем название
            name = item.find('span', itemprop='name')
            name = name.text.strip() if name else "Название отсутствует"

            # Извлекаем цену
            price = item.find('div', class_='cl-item-info-price-discount')
            price = price.text.strip() if price else "Цена отсутствует"

            # Извлекаем ссылку
            link = item.find('a', class_='cl-item-img')
            link = link['href'] if link else "Ссылка отсутствует"

            # Извлекаем рейтинг (если есть)
            rating = item.find('div', class_='cl-item-info-rating')
            rating = rating.find('span').text.strip() if rating else "Рейтинг отсутствует"

            # Выводим данные о товаре
            print(f"Название: {name}")
            print(f"Цена: {price}")
            print(f"Ссылка: {link}")
            print(f"Рейтинг: {rating}\n")
    else:
        print("Товары не найдены на странице.")
else:
    print(f"Ошибка загрузки страницы: {response.status_code}")

