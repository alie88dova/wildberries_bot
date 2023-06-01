from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import random


driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
driver.get("https://www.wildberries.ru")

elem = driver.find_element(By.ID, "searchInput")
elem.send_keys("")
time.sleep(1)
elem.send_keys(f"Ф")
time.sleep(random.randint(1, 3)/10)
elem.send_keys(f"о")
time.sleep(random.randint(1, 3)/10)
elem.send_keys(f"р")
time.sleep(random.randint(1, 3)/10)
elem.send_keys(f"т", Keys.ENTER)

time.sleep(2)

elements = driver.find_elements(By.CLASS_NAME, "product-card__wrapper")
print(len(elements))


while True:
    after_scroll = 0
    schroll = 0
    repeat_scroll_h = 0
    scroll_h = []
    scroll = 0
    while repeat_scroll_h != 5:
        scroll += 500
        schroll = after_scroll
        driver.execute_script(f"window.scrollTo(0, {scroll});")
        # wait to load page


        time.sleep(0.2)
        print(after_scroll)
        after_scroll = driver.execute_script("return document.body.scrollHeight")

        if after_scroll == schroll:
            repeat_scroll_h += 1
            print('repeat')
        else:
            repeat_scroll_h = 0


    elements = driver.find_elements(By.CLASS_NAME, "product-card__wrapper")
    print(len(elements))
    try:
        el = driver.find_element(By.CLASS_NAME, "pagination-next")
        print(el.text)
        el.click()
        print("Следующая страница")
    except Exception as e:
        print(e)
        print("Больше страниц нет")
        break


while True:
    h = 1

driver.close()
