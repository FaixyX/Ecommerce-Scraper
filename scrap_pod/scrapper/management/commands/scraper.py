from django.core.management.base import BaseCommand
from django.conf import settings

from scrapper.models import SubCategories, Product

from urllib.parse import quote, urlparse, urlunparse
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from re import search as rsearch, sub as rsub

def extract_price(s: str):
    f = rsearch(r'\d', s)
    l = rsearch(r'\d(?=[^\d]*$)', s)
    if not f or not l:
        return ""
    parts = s[f.start():l.end()].split('.', 1)  # Split at the first dot
    return rsub(r'[^\d.]', '', '.'.join([parts[0], parts[1].replace('.', '') if len(parts)>1 else '00']))

BASE_DIR = settings.BASE_DIR
TIMEOUT = 5
MAX_TRIES = 2

def scrape_category(url, store):
    products = []
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f"--headless=new")
        options.add_argument(f"--user-data-dir={BASE_DIR.absolute()}/user_data_dirs/special/user_data")

        driver = webdriver.Chrome(options=options, keep_alive=True)
        
        # print(f'store: {type(store)} , {store}')
        
        if store == 'Home Shopping': # homeshopping
            # print('Scraping for Home Shopping')
            tries = 0
            driver.get(url)
            while True:
                try:
                    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(concat(" ",normalize-space(@class)," ")," ProductsList ")]/div[contains(concat(" ",normalize-space(@class)," ")," product-box ")][last()]')))
                except TimeoutException:
                    tries += 1
                    if tries < MAX_TRIES:
                        continue
                    else:
                        break
                else:
                    cards = driver.find_elements(By.XPATH, '//div[contains(concat(" ",normalize-space(@class)," ")," ProductsList ")]/div[contains(concat(" ",normalize-space(@class)," ")," product-box ")]')
                    for card in cards:
                        image = card.find_element(By.XPATH, './/img[contains(concat(" ",normalize-space(@class)," ")," imgcent ")]').get_attribute('src')
                        title = card.find_element(By.XPATH, './/h5[contains(concat(" ",normalize-space(@class)," ")," ProductDetails ")]').text
                        price_a = card.find_element(By.XPATH, './/a[contains(concat(" ",normalize-space(@class)," ")," price ")]')
                        link = price_a.get_attribute('href')
                        price = price_a.text
                        products.append({
                            'title': title,
                            'image': image,
                            'price': extract_price(price),
                            'url': link,
                        })
                finally:
                    break
        elif store == 'Priceoye': # priceoye
            # print('Scraping for Priceoye')
            tries = 0
            driver.get(url)
            # print("[ ] Searching on PriceOye.")
            while True:
                try:
                    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(concat(" ",normalize-space(@class)," ")," product-list ")]//div[contains(concat(" ",normalize-space(@class)," ")," productBox ")][last()]')))
                except TimeoutException:
                    tries += 1
                    if tries < MAX_TRIES:
                        continue
                    else:
                        break
                else:
                    cards = driver.find_elements(By.XPATH, '//div[contains(concat(" ",normalize-space(@class)," ")," product-list ")]//div[contains(concat(" ",normalize-space(@class)," ")," productBox ")]/a')
                    # print('len of cards in Priceoye', len(cards))
                    for card in cards:
                        link  = card.get_attribute('href')
                        image = card.find_element(By.XPATH, './div[contains(concat(" ",normalize-space(@class)," ")," image-box ")]/amp-img/img').get_attribute('src')
                        detail_box = card.find_element(By.XPATH, './div[contains(concat(" ",normalize-space(@class)," ")," detail-box ")]')
                        title = detail_box.find_element(By.XPATH, './div[contains(concat(" ",normalize-space(@class)," ")," p-title ")]').text
                        price = detail_box.find_element(By.XPATH, './div[contains(concat(" ",normalize-space(@class)," ")," price-box ")]').text
                        products.append({
                            'title': title,
                            'price': extract_price(price),
                            'image': image,
                            'url': link,
                        })
                        # print('len of products in PriceOye', len(products))
                finally:
                    break
        elif store == 'Telemart': # telemart
            # print('Scraping for Telemart')
            tries = 0
            driver.get(url)
            # print("[ ] Searching on Telemart.")
            while True:
                try:
                    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[5]/div[1]/div')))
                except TimeoutException:
                    tries += 1
                    if tries < MAX_TRIES:
                        continue
                    else:
                        break
                else:
                    cards = driver.find_elements(By.XPATH, '//*[@id="wrapper"]/div/div[5]/div[1]/div/div')
                    for card in cards:
                        # print('I am here')
                        link = card.find_element(By.XPATH, './a').get_attribute('href')
                        # print('link', link)
                        image = card.find_element(By.XPATH, './a//img').get_attribute('src')
                        # print('image', image)
                        title = card.find_element(By.XPATH, './a//h4[contains(@class, "text-xs")]').text
                        # print('title', title)
                        price = card.find_element(By.XPATH, './a//span[contains(@class, "text-green-600")]').text
                        # print('price', price)
                        products.append({
                            'title': title,
                            'price': extract_price(price),
                            'image': image,
                            'url': link,
                        })
                    # print('len of products in Telemart', len(products))
                finally:
                    break
        elif store == 'Daraz': # daraz
            # print('Scraping for Daraz')
            tries = 0
            driver.get(url)
            while True:
                try:
                    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div[1]/div[2]/div//div[@id="id-img"]/img')))
                except TimeoutException:
                    tries += 1
                    if tries < MAX_TRIES:
                        continue
                    else:
                        break
                else:
                    cards = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div[1]/div[2]/div')
                    # print('len of cards in daraz', len(cards))
                    for card in cards:
                        # print('I am here')
                        title = card.find_element(By.XPATH, './/div[@id="id-title"]').text
                        price = card.find_element(By.XPATH, './/div[@id="id-price"]//span[contains(@class, "currency--GVKjl")]').text
                        image = card.find_element(By.XPATH, './/div[@id="id-img"]/img').get_attribute('src')
                        link = card.find_element(By.XPATH, './/a[@id="id-a-link"]').get_attribute('href')
                        products.append({
                            'title': title,
                            'price': extract_price(price),
                            'image': image,
                            'url': link,
                        })
                        # print('len of products in daraz', len(products))
                finally:
                    break
        else:
            pass
    except Exception as e:
        print(e)
        raise e
    finally:
        driver.quit()
    return products

class Command(BaseCommand):
    help = 'Scrape the data and dump it in the Products table'
    def handle(self, *args, **kwargs):
        # Iterate through each sub-category
        for sub_category in SubCategories.objects.all():
            self.stdout.write(f"Scraping data for sub-category: {sub_category.name}, {sub_category.store}")
            products = scrape_category(sub_category.url, sub_category.store.name)
            for product_data in products:
                # Check if the product already exists
                product, created = Product.objects.get_or_create(
                    name=product_data['title'],
                    defaults={
                        'image': product_data.get('image'),
                        'price': product_data.get('price'),
                        'url': product_data.get('url'),
                        'store': sub_category.store,
                        'category': sub_category.category,
                        'sub_category': sub_category,
                    }
                )
                if created:
                    self.stdout.write(f"Added new product: {product.name}")
                else:
                    self.stdout.write(f"Updated existing product: {product.name}")
                product.save()
