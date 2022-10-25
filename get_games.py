# -*- coding: utf8 -*-
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def get_games_torrent(count_games):

    url = "http://s522030602.games-torrents.org/2022-god/"

    options = webdriver.ChromeOptions()

    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
                         "/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")

    # accept
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
        print("Загружаю страницу со списком игр...")
        driver.get(url=url)
        time.sleep(5)
        print("Сохраняю страницу со списком игр...")
        with open("index_games.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
        return "Что то пошло не так, не могу перейти на страницу игр..."
    finally:
        driver.close()
        driver.quit()

    with open("index_games.html", "r", encoding="utf-8") as file:
        page_html = file.read()
    try:
        soup = BeautifulSoup(page_html, "lxml")
        src = soup.find_all("div", class_="short")
    except Exception as ex:
        print(ex)
        return "Что то пошло не так...Не могу найти блок со списком игр!"

    urls = []
    try:
        for i in range(count_games):
            print("Получаю ссылку страницы номер {0}...".format(i+1))
            urls.append(src[i].find("a").get("href"))
    except Exception as ex:
        print(ex)
        return "Что то пошло не так...Не могу найти ссылки на игры!"

    message = ""
    for number, url in enumerate(urls):

        options = webdriver.ChromeOptions()

        # user-agent
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                             " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")

        # accept
        options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/"
                             "avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")

        # for ChromeDriver version 79.0.3945.16 or over
        options.add_argument("--disable-blink-features=AutomationControlled")

        # headless mode
        options.add_argument("--no-sandbox")
        options.headless = True

        s = Service("chromedriver.exe")
        driver = webdriver.Chrome(service=s, options=options)

        print("Открываю страницу {0}...".format(number + 1))

        try:
            driver.get(url=url)
            time.sleep(5)
            print("Сохраняю страницу {0}...".format(number + 1))
            with open("games.html", "w", encoding="utf-8") as file:
                file.write(driver.page_source)
            print("Страница сохранена...")

        except Exception as ex:
            return ex
        finally:
            driver.close()
            driver.quit()

        with open("games.html", "r", encoding="utf-8") as file:
            page_html = file.read()
        try:
            soup = BeautifulSoup(page_html, "lxml")
            text = soup.find("div", class_="full12").get_text()
        except Exception as ex:
            print(ex)
            return "Что то пошло не так...Не нахожу блок с описанием игры..."

        print("Начинаю сбор информации игры {0}".format(number + 1))
        try:
            src = soup.find("iframe").get("src")
        except Exception as ex:
            print(ex)
            src = "!!!Не могу найти..."
        try:
            title = re.compile(r"Название:\s*([\w+\s+:;\+-\\(\\).,\"«»–]+)\s*Дата").findall(text)[0]
        except Exception as ex:
            print(ex)
            title = "!!!Не могу найти..."
        try:
            date = re.compile(r"Дата выхода:\s*([\w+\s+:;\+-\\(\\).,\"«»–]+)\s*Жанр").findall(text)[0]
        except Exception as ex:
            print(ex)
            date = "!!!Не могу найти..."
        try:
            genre = re.compile(r"Жанр:\s*([\w+\s+:;\+-\\(\\).,\"«»–]+)\s*Разработчик:").findall(text)[0]
        except Exception as ex:
            print(ex)
            genre = "!!!Не могу найти..."
        try:
            lang_interface = re.compile(r"Язык интерфейса:\s*([\w+\s+:;\+-\\(\\).,\"«»–]+)\s*Язык").findall(text)[0]
        except Exception as ex:
            print(ex)
            lang_interface = "!!!Не могу найти..."
        try:
            lang_voice = re.compile(r"Язык озвучки:\s*([\w+\s+:;\+-\\(\\).,\"«»–]+)\s*Таблетка").findall(text)[0]
        except Exception as ex:
            print(ex)
            lang_voice = "!!!Не могу найти..."
        try:
            tablet = re.compile(r"Таблетка:\s*([\w+\s+:;\+-\\(\\).,\"«»–]+)\s*Описание").findall(text)[0]
        except Exception as ex:
            print(ex)
            tablet = "!!!Не могу найти..."
        try:
            sys_req = re.compile(r"Системные требования:\s*([\w+\s+:;\+-\\(\\).,\"«»–]+GB)").findall(text)[0]
        except Exception as ex:
            print(ex)
            sys_req = "!!!Не могу найти..."

        message += "-" * 60 + "\n"
        message += "Название: " + title + "\n"
        message += "\t\tДата выхода: " + date + "\n"
        message += "\t\tЖанр: " + genre + "\n"
        message += "\t\tЯзык интерфейса: " + lang_interface + "\n"
        message += "\t\tЯзык озвучки: " + lang_voice + "\n"
        message += "\t\tТаблетка: " + tablet + "\n"
        message += "\t\tСистемные требования: " + sys_req + "\n"
        message += "\t\tВидео: " + src

        print("Готово!")
    return message


def main(count_games):
    return get_games_torrent(count_games)


