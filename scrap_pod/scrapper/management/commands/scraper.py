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
        # options.add_argument(f"--headless=new")
        options.add_argument(f"--user-data-dir={BASE_DIR.absolute()}/user_data_dirs/special/user_data")

        driver = webdriver.Chrome(options=options, keep_alive=True)
        
        print(f'url  : {type(url)}   , {url}')
        print(f'store: {type(store)} , {store}')
        
        if store == 'Home Shopping': # homeshopping
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
                finally:
                    break
        elif store == 'Telemart': # telemart
            tries = 0
            driver.get(url)
            # print("[ ] Searching on Telemart.")
            while True:
                try:
                    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[@class="flex-col w-full"]/div[1]')))
                except TimeoutException:
                    tries += 1
                    if tries < MAX_TRIES:
                        continue
                    else:
                        break
                else:
                    cards = driver.find_elements(By.XPATH, '//div[@class="flex-col w-full"]/div[1]/div/a')
                    for card in cards:
                        link  = card.get_attribute('href')
                        detail_box = card.find_element(By.XPATH, './div/a//div[1]')
                        image = detail_box.find_element(By.XPATH, './/img').get_attribute('src')
                        title = detail_box.find_element(By.XPATH, './/h4').text
                        price = card.find_element(By.XPATH, './div/a//div[2]//span[contains(concat(" ",normalize-space(@class)," ")," tracking-tighter ")][1]').text
                        products.append({
                            'title': title,
                            'price': extract_price(price),
                            'image': image,
                            'url': link,
                        })
                finally:
                    break
        elif store == 'Daraz': # daraz
            tries = 0
            driver.get(url)
            while True:
                try:
                    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//a[@id="id-a-link"][last()]')))
                except TimeoutException:
                    tries += 1
                    if tries < MAX_TRIES:
                        continue
                    else:
                        break
                else:
                    cards = driver.find_elements(By.XPATH, '//a[@id="id-a-link"]')
                    for card in cards:
                        description = card.find_element(By.XPATH, './div[2]')
                        title = description.find_element(By.XPATH, './div[1]').text
                        price = description.find_element(By.XPATH, './div[@id="id-price"]/div/div[1]').text
                        image = card.find_element(By.XPATH, './/*[@id="module_item_gallery_1"]/div/div[1]/div[1]/img').get_attribute('src')
                        link  = urlunparse(urlparse(card.get_attribute('href'))._replace(query=''))
                        products.append({
                            'title': title,
                            'price': extract_price(price),
                            'image': image,
                            'url': link,
                        })
                finally:
                    break
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
            self.stdout.write(f"Scraping data for sub-category: {sub_category.name}")
            self.stdout.write(f"url: {sub_category.url}")
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
