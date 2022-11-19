# -*- coding: utf8 -*-
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def info_wiki(words):

    url = "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"

    options = webdriver.ChromeOptions()

    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                         " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
    options.add_argument("accept=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                         "537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")

    # headless mode
    options.add_argument("--no-sandbox")
    options.headless = True

    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)

    try:
        print("Открываю страницу википедии...")
        driver.get(url=url)
        time.sleep(3)
        print("Ввожу текст в поиск...")
        input_text = driver.find_element("xpath", "//input[@class='vector-search-box-input']")
        input_text.send_keys(words)
        time.sleep(1)
        driver.find_element("xpath", "//input[@id='searchButton']")
        if driver.find_element("xpath", "//div[@class='mw-search-results-container']"):
            driver.find_element("xpath", "//div[@class='mw-search-results-container']").\
               find_element("xpath", "//a[@data-serp-pos='0']").click()
        time.sleep(1)
        href = driver.current_url
        print("Сохраняю страницу...")
        with open("sites/index_wiki.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        time.sleep(1)
        print("Готово")
    except Exception as ex:
        print(ex)
        return ex
    finally:
        driver.close()
        driver.quit()

    try:
        with open("sites/index_wiki.html", "r", encoding="utf-8") as file:
            page_html = file.read()
            file.close()
        print("Поиск пунктов информации...")
        soup = BeautifulSoup(page_html, "lxml")

        if soup.find("div", class_="mw-search-results-container"):
            pass

        src = soup.find("div", class_="mw-parser-output")

        text = src.find_all("p")

        message = ""

        for i in range(2):
            message += text[i].text

        message = re.compile(r"[A-zА-яёЁ,.\s0-9-+()—]+").findall(message)
        message = " ".join(message)
        message += '\n' + href

        return message

    except Exception as ex:
        print("что то пошло не так")
        print(ex)
        return ex


def main(words):
    return info_wiki(words)

# if __name__ == '__main__':
#     print(main(words))

