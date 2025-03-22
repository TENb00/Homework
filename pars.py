import requests
from bs4 import BeautifulSoup

url = 'https://msk.blokart.su/'
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    products = soup.find_all('div', class_='product-item')

    for product in products:
        name = product.find('h2').text.strip()
        price = product.find('span', class_='price').text.strip()
        print(f"Название: {name}, Цена: {price}")