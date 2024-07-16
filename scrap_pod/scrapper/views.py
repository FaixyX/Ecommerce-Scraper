
from django.shortcuts import render
from django.conf import settings

from urllib.parse import quote, urlparse, urlunparse
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .utils import extract_price

from random import choice

BASE_DIR = settings.BASE_DIR
TIMEOUT = 5
MAX_TRIES = 2

IDs = []
ARB = set(range(100))

def get_id():
    global IDs
    try:
        x = choice(list(ARB - set(IDs)))
        IDs.append(x)
    except IndexError:
        x = None
    return x

def release_id(id):
    global IDs
    IDs.remove(id)

def home(request):
    return render(request, 'Home.html')

def admin(request):
    return render(request, 'Admin.html')

def productlist(request):
    return render(request, 'Productlist.html')

def register(request):
    return render(request, 'Register.html')

def login(request):
    return render(request, 'Login.html')

def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('query', None)
        if search_query is None or search_query.strip() == '':
            render(request, 'Search.html', {'products': [], 'search_query': '[Try searching something]'})
        
        results = []
        searchID = get_id()
        try:
            tries = 0
            options = webdriver.ChromeOptions()
            options.add_argument(f"--headless=new")
            options.add_argument(f"--user-data-dir={BASE_DIR.absolute()}/user_data_dirs/{searchID}/user_data")
            
            driver = webdriver.Chrome(options=options, keep_alive=True)
            
            # {search} homeshopping
            driver.get("https://homeshopping.pk/search.php?category%%5B%%5D=&search_query=%s" % quote(search_query))
            # print("[ ] Searching on Home Shopping.")
            while True:
                try:
                    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(concat(" ",normalize-space(@class)," ")," ProductList ")]/div[contains(concat(" ",normalize-space(@class)," ")," product-box ")][last()]')))
                except TimeoutException:
                    tries += 1
                    if tries < MAX_TRIES:
                        continue
                    else:
                        break
                else:
                    cards = driver.find_elements(By.XPATH, '//div[contains(concat(" ",normalize-space(@class)," ")," ProductList ")]/div[contains(concat(" ",normalize-space(@class)," ")," product-box ")]')
                    for card in cards:
                        image = card.find_element(By.XPATH, './/*[@id="prodcut-desc"]/div[1]/div/div/div[3]/div[4]/img').get_attribute('src')
                        title = card.find_element(By.XPATH, './/h5[contains(concat(" ",normalize-space(@class)," ")," ProductDetails ")]').text
                        price_a = card.find_element(By.XPATH, './/a[contains(concat(" ",normalize-space(@class)," ")," price ")]')
                        link = price_a.get_attribute('href')
                        price = price_a.text
                        results.append({
                            'title': title,
                            'price': extract_price(price),
                            'link': link,
                            'img': image,
                            'site': 'homeshopping'
                        })
                finally:
                    break
            
            # {search} priceoye
            tries = 0
            driver.get("https://priceoye.pk/search?q=%s" % quote(search_query))
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
                        results.append({
                            'title': title,
                            'price': extract_price(price),
                            'link': link,
                            'img': image,
                            'site': 'priceoye'
                        })
                finally:
                    break
                
            # {search} telemart
            tries = 0
            driver.get("https://telemart.pk/search?query=%s" % quote(search_query))
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
                        results.append({
                            'title': title,
                            'price': extract_price(price),
                            'link': link,
                            'img': image,
                            'site': 'telemart'
                        })
                finally:
                    break
            
            # {search} daraz
            tries = 0
            driver.get("https://www.daraz.pk/catalog/?q=%s" % quote(search_query))
            # print("[ ] Searching on Daraz.")
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
                        results.append({
                            'title': title,
                            'price': extract_price(price),
                            'link': link,
                            'img': image,
                            'site': 'daraz'
                        })
                finally:
                    break
        except:
            pass
        finally:
            release_id(searchID)
            driver.quit()
    return render(request, 'Search.html', {'products': results, 'search_query': search_query})
