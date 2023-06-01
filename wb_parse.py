from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
import random

#Это тестовый файл

def search(user_request) -> webdriver:
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    driver.get("https://www.wildberries.ru")

    elem = driver.find_element(By.ID, "searchInput")
    elem.send_keys("")
    time.sleep(1)
    for letter in user_request:
        elem.send_keys(f"{letter}")
        time.sleep(random.randint(1, 3) / 10)
    elem.send_keys(Keys.ENTER)
    time.sleep(2)
    return driver


def get_page_number(driver: webdriver):

    pattern = r'page=(\d+)'
    url = driver.current_url
    page = re.findall(pattern, url)
    return page


def find_position(article: int, ids: list):
    #Стандартне значения для выдачи в wildberries
    stolbci = 5
    stroka= 1
    for i in range(len(ids)):
        if (i+1)%stolbci == 0:
            stroka += 1
        if ids[i] == str(article):

            return ((i)%stolbci+1, stroka)
    return 0


def scroll_to_end_page(driver: webdriver):
    after_scroll = 0
    repeat_scroll_h = 0
    scroll = 0
    while repeat_scroll_h != 10:
        scroll += 350
        schroll = after_scroll
        driver.execute_script(f"window.scrollTo(0, {scroll});")
        # wait to load page

        time.sleep(0.2)
        after_scroll = driver.execute_script("return document.body.scrollHeight")

        if after_scroll == schroll:
            repeat_scroll_h += 1
        else:
            repeat_scroll_h = 0


def find_position_by_article(article: int, search_str: str):

    #Это тестовый бот поэтому реализовывать сисетму очереди плка не стал
    #Но если использовать бота в боевой задаче это будет необходимо
    driver = search(search_str)
    pattern = r'id="c(\d+)"' # Тк мы получаем
    while True:

        scroll_to_end_page(driver)
        elements = driver.find_element(By.CLASS_NAME, "product-card-list")
        full_text = elements.get_attribute("innerHTML")
        ids = re.findall(pattern, full_text)
        #Проверяет есть ли в искомом блоке товары
        #Если товары не обнаруженны

        if not ids:
            return -1

        postion = find_position(article, ids)

        if postion != 0:
            print(postion)
            return postion, get_page_number(driver)

        try:
            el = driver.find_element(By.CLASS_NAME, "pagination-next")

            time.sleep(0.5)
            el.click()
        except Exception as e:
            print(e)



