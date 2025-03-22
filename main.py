import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Базовый URL сайта
base_url = 'https://msk.blokart.su'


# Функция для получения HTML-кода страницы
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Ошибка при запросе {url}: {response.status_code}")
        return None


# Функция для извлечения ссылок на подкатегории
def get_category_links(soup):
    categories = []
    # Ищем все ссылки на подкатегории
    for category in soup.find_all('div', class_='good-item b-catalog__item'):
        link = category.find('a', href=True)
        if link:
            category_url = urljoin(base_url, link['href'])
            categories.append(category_url)
    return categories


# Функция для извлечения данных о товарах
def get_products(soup):
    products = []
    # Находим все товары на странице
    for product in soup.find_all('div', class_='good-item'):
        # Название товара
        name = product.find('a', class_='good-item__title-link').text.strip() if product.find('a',
                                                                                              class_='good-item__title-link') else 'Нет названия'

        # Цена товара
        price = product.find('span', class_='b-price').text.strip() if product.find('span',
                                                                                    class_='b-price') else 'Нет цены'

        # Ссылка на товар
        link = product.find('a', class_='good-item__title-link', href=True)
        if link:
            product_url = urljoin(base_url, link['href'])  # Преобразуем относительную ссылку в абсолютную
        else:
            product_url = 'Нет ссылки'

        # Код товара (артикул)
        article = product.find('div', class_='good-item__article').text.strip() if product.find('div',
                                                                                                class_='good-item__article') else 'Нет артикула'

        # Производитель
        developer = product.find('div', class_='good-item__developer').text.strip() if product.find('div',
                                                                                                    class_='good-item__developer') else 'Нет производителя'

        # Изображение товара
        image = product.find('img', src=True)
        image_url = urljoin(base_url, image['src']) if image else 'Нет изображения'

        # Добавляем товар в список
        products.append({
            'name': name,
            'price': price,
            'url': product_url,
            'article': article,
            'developer': developer,
            'image': image_url
        })
    return products


# Основная функция
def main():
    # URL главной страницы каталога
    main_page_url = urljoin(base_url, '/netshop/')

    # Получаем HTML главной страницы
    main_page_html = get_page(main_page_url)
    if not main_page_html:
        return

    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(main_page_html, 'html.parser')

    # Получаем ссылки на подкатегории
    category_links = get_category_links(soup)
    print(f"Найдено {len(category_links)} подкатегорий.")

    # Проходим по каждой подкатегории и извлекаем товары
    all_products = []
    for category_url in category_links:
        print(f"Обрабатывается подкатегория: {category_url}")
        category_html = get_page(category_url)
        if category_html:
            category_soup = BeautifulSoup(category_html, 'html.parser')
            products = get_products(category_soup)
            all_products.extend(products)

    # Выводим результаты
    print(f"Всего найдено {len(all_products)} товаров.")
    for product in all_products:
        print(f"Название: {product['name']}")
        print(f"Цена: {product['price']}")
        print(f"Ссылка: {product['url']}")
        print(f"Артикул: {product['article']}")
        print(f"Производитель: {product['developer']}")
        print(f"Изображение: {product['image']}")
        print("-" * 40)


if __name__ == '__main__':
    main()