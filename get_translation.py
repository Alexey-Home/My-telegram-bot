# -*- coding: utf8 -*-
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


def translation(words, out_language):

    language = dict({"ru": "русский",
                     "en": "английский",
                     "be": "белорусский"})

    url = "https://www.google.com/search?q=%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA"

    options = webdriver.ChromeOptions()

    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                         " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
    options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/"
                         "avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")

    # headless mode
    options.add_argument("--no-sandbox")
    options.headless = True

    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)

    try:
        print("Определяю язык текста...")

        in_lang = language["ru"]
        out_lang = language["en"]

        if re.compile(r"[Aa-zZ]+").findall(words):
            in_lang = language["en"]
            out_lang = language["ru"]

        if out_language:
            out_lang = language[out_language]

        print("Открываю страницу переводчика...")
        driver.get(url=url)
        time.sleep(3)
        print("Ввожу в поле ввода текст...")
        input_text = driver.find_element("xpath", "//textarea[@class='tw-ta tw-text-large q8U8x goog-textarea']")
        input_text.clear()
        input_text.send_keys(words)
        time.sleep(1)
        print("Выбираю язык в поле ввода...")
        driver.find_element("xpath", "//div[@id='tw-sl']").click()
        time.sleep(1)
        input_lang = driver.find_element("xpath", "//input[@id='sl_list-search-box']")
        input_lang.send_keys(in_lang)
        time.sleep(1)
        input_lang.send_keys(Keys.ENTER)
        time.sleep(1)
        print("Выбираю язык в поле вывода...")
        driver.find_element("xpath", "//div[@id='tw-tl']").click()
        time.sleep(1)
        output_lang = driver.find_element("xpath", "//input[@id='tl_list-search-box']")
        output_lang.send_keys(out_lang)
        time.sleep(1)
        output_lang.send_keys(Keys.ENTER)
        time.sleep(1)
        tr_text = driver.find_element("xpath", "//pre[@id='tw-target-text']").text
        print("Готово")
        return tr_text

    except Exception as ex:
        print(ex)
        return ex
    finally:
        driver.close()
        driver.quit()


def main(words, out_language):
    return translation(words, out_language)


# if __name__ == '__main__':
#     main(words, out_lang)
