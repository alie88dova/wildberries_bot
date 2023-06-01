import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import requests
import re


class Card(object):
    """
    search_input - хранит искомый запрос
    """

    def __init__(self, search_input: str, article: int):
        self.search_input = search_input
        self.article = article
        self.row = None
        self.column = None
        self.page = None

    @property
    def get_possition(self):
        return (self.column, self.row,self.page )



    def check_correct_article(self) -> str:
        """
        Проверяет все ли в порядке с вашим артикулем
        :return correct если все впорядке
                incorrect_article если данный артикль не существует
                unfound_article если данный артикль нельзя найти в поисковом запросе (Нет в наличие)
        """
        url = f"https://www.wildberries.ru/catalog/{self.article}/detail.aspx"

        driver = webdriver.Chrome()
        driver.set_window_size(1920, 1080)
        driver.get(url)
        time.sleep(1) #Задердка на необходимую подгрузку

        #Если он может найти данную строку то искать товар в выдаче безполезно
        try:
            elem = driver.find_element(By.CLASS_NAME, "content404__title")
            return "incorrect_article"
        except Exception as e:
            print("It's real")
        time.sleep(1)  # Задердка на необходимую подгрузку

        try:
            elem = driver.find_element(By.CLASS_NAME, "product-page__aside-container")
            price = elem.find_element(By.CLASS_NAME, "product-page__price-block")
            if price.text == "Нет в наличии":
                return "unfound_article"
            return "correct"

        except Exception as e:
            pass


    def __scroll_to_end_page(self, driver: webdriver):
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

    def __wb_search(self) -> webdriver:
        driver = webdriver.Chrome()
        driver.set_window_size(1920, 1080)
        driver.get("https://www.wildberries.ru")

        elem = driver.find_element(By.ID, "searchInput")
        elem.send_keys("")
        time.sleep(1)
        for letter in self.search_input:
            elem.send_keys(f"{letter}")
            time.sleep(random.randint(1, 3) / 10)
        elem.send_keys(Keys.ENTER)
        time.sleep(2)
        return driver

    def __find_position(self, ids: list) -> int:
        """
        Устанавливает позицию если найдено соответсвие искомым данным
        :param ids:
        :return: 1 - позиция найдена
                 0 - позиция не найдена
        """
        # Стандартне значения для выдачи в wildberries
        rows = 5
        column = 1
        print(len(ids))
        for i in range(len(ids)):
            if (i + 1) % rows == 0:
                column += 1
            if ids[i] == str(self.article):
                self.row = i % rows + 1
                self.column = column
                return 1
        return 0


    def __get_page_number(self, driver):
        print(driver)
        try:
            pattern = r'page=(\d+)'
            url = driver.current_url
            page = re.findall(pattern, url)
            return page[0]
        except Exception as e:
            print(e)
            return 1

    def find_position_by_article(self):

        # Это тестовый бот поэтому реализовывать сисетму очереди плка не стал
        # Но если использовать бота в боевой задаче это будет необходимо
        driver = self.__wb_search()
        pattern = r'id="c(\d+)"'  # Тк мы получаем
        while True:
            self.__scroll_to_end_page(driver)
            elements = driver.find_element(By.CLASS_NAME, "product-card-list")
            full_text = elements.get_attribute("innerHTML")
            ids = re.findall(pattern, full_text)
            # Проверяет есть ли в искомом блоке товары
            # Если товары не обнаруженны
            if not ids:
                return -1
            postion = self.__find_position(ids)
            if postion != 0:
                page = self.__get_page_number(driver)
                self.page = int(page)
                return 1
            try:
                el = driver.find_element(By.CLASS_NAME, "pagination-next")

                time.sleep(0.5)
                el.click()
            except Exception as e:
                print(e)






if __name__ == "__main__":
    #print(find_position_by_article(, "Газировка"))
    card = Card("K-girl", 122997863 )
    print(card.check_correct_article())
    print(card.find_position_by_article())
    print(card.get_possition)
