# -*- coding: utf8 -*-
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def get_weather_gismeteo(count_days):
    """
    Переходит на страницу сайта "Gismeteo". Сохраняет ее.И со страницы собирает информацию:
    Число,погода,температура,ветер, осадки.
    Вовзращает составленое сообщение с гиметео.
    """

    url = "https://www.gismeteo.ru/weather-arzamas-4377/3-days/"

    get_page_html(url, "гисметео")

    days = get_info_days_gismeteo(count_days)

    message = url
    message = get_message(days, message, "гисметео")

    return message


def get_weather_yandex(count_days):
    """
    Переходит на страницу сайта яндекс-погода. Сохраняет ее.И со страницы собирает информацию:
    Число,погода,температура,ветер, рассвет, закат.
    Вовзращает составленое сообщение с гиметео.
    """

    url = "https://yandex.ru/pogoda/details?lat=55.38680267&lon=43.81413651&via=ms"

    get_page_html(url, "яндекс-погода")

    days = get_info_days_yandex(count_days)

    message = url
    message = get_message(days, message, "яндекс-погода")

    return message


def get_page_html(url, name_site):
    """Функция сохраняет страницу с ссылки"""
    options = webdriver.ChromeOptions()

    # user-agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
    options.add_argument(
        "accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/"
        "avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")

    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")

    # headless mode
    options.add_argument("--no-sandbox")
    options.headless = True

    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)

    try:
        print(f"Открываю страницу {name_site}...")
        driver.get(url=url)
        time.sleep(5)
        print(f"Сохраняю страницу {name_site}...")
        with open("sites/index_weather.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
        return f"Не могу перейти на страницу {name_site}..."
    finally:
        driver.close()
        driver.quit()
    print("Готово")


def get_info_days_gismeteo(count_days):
    """Функция собирает информацию по дням с сайта гисметео"""
    try:
        with open("sites/index_weather.html", "r", encoding="utf-8") as file:
            page_html = file.read()
        soup = BeautifulSoup(page_html, "lxml")
        cards = soup.find("div", class_="widget-items")
    except Exception as ex:
        print(ex)
        return "Что то пошло не так, не могу найти блок..."
    os.remove("sites/index_weather.html")

    print("Собираю информацию: число, погода, температура, ветер, осадки...")
    count = 0
    days = []
    src_day = cards.find_all("a", class_=re.compile(r"item item-day-[0-9] link date-left"))
    src_weather = cards.find_all("div", class_="weather-icon tooltip")
    src_temperature = cards.find_all("span", class_="unit unit_temperature_c")
    src_wind = cards.find_all("span", class_="wind-unit unit unit_wind_m_s")
    src_precipitation = cards.find_all("div", class_="item-unit unit-blue")

    for i in range(len(src_day)):
        if count == count_days:
            break
        temperature = []
        weather = []
        wind = []
        precipitation = []
        day = dict({"time_day": ["Ночь: ", "Утро: ", "День: ", "Вечер: "]})
        try:
            day["date_day"] = src_day[i].text

            for j in range(len(day["time_day"])):
                weather.append(src_weather[j].get("data-text"))
                temperature.append(src_temperature[j].text)
                wind.append(src_wind[j].text)
                precipitation.append(src_precipitation[j].text)
        except Exception as ex:
            print(ex)
            return ex

        day["weather"] = weather
        day["temperature"] = temperature
        day["wind"] = wind
        day["precipitation"] = precipitation
        days.append(day)
        count += 1

        lenght = len(day["time_day"])

        src_weather = src_weather[lenght:]
        src_temperature = src_temperature[lenght:]
        src_wind = src_wind[lenght:]
        src_precipitation = src_precipitation[lenght:]

    print("Готово")
    return days


def get_info_days_yandex(count_days):
    """Функция собирает информацию с карточек с сайта яндекс-погода"""
    try:
        with open("sites/index_weather.html", "r", encoding="utf-8") as file:
            page_html = file.read()
        soup = BeautifulSoup(page_html, "lxml")
        cards = soup.find_all("article", class_=re.compile("card"))
    except Exception as ex:
        print(ex)
        return f"Что то пошло не так, не могу найти блок...Ошибка: {ex}"
    os.remove("sites/index_weather.html")

    count = 0
    days = []
    print("Собираю информацию: число, температура, погода, ветер, рассвет, закат")
    for i in range(len(cards)):
        if count == count_days:
            break
        temperature = []
        weather = []
        wind = []
        day = dict({"time_day": ["Ночь: ", "Утро: ", "День: ", "Вечер: "]})
        try:
            day["date_day"] = cards[i].find("strong", class_="forecast-details__day-number").text + " " + cards[i]\
                .find("span", class_="forecast-details__day-month").text

            time_days = cards[i].find_all("tr", class_="weather-table__row")
            for time_day in time_days:
                temperature.append(time_day.find("div", class_="weather-table__temp").text)

                weather.append(
                    time_day.find("td", class_="weather-table__body-cell weather-table__body-cell_type_condition").text)

                wind.append(time_day.find("span", class_="weather-table__wind").text)
            day["temperature"] = temperature
            day["weather"] = weather
            day["wind"] = wind
            day["sunrise"] = cards[i].find("dl", class_="sunrise-sunset__description sunrise-sunset__description_value_sunrise")\
                .find("dd", class_="sunrise-sunset__value").text
            day["sunset"] = cards[i].find("dl", class_="sunrise-sunset__description sunrise-sunset__description_value_sunset")\
                .find("dd", class_="sunrise-sunset__value").text
            count += 1
            days.append(day)
        except Exception as ex:
            print(ex)
            continue
    print("Готов")
    return days


def get_message(days, message, name_site):
    """Функция формирует сообщение для отправки"""
    print(f"Составляю текст сообщения с {name_site}...")
    try:
        for i in range(len(days)):
            message += "\n" + "-" * 60
            message += "\n" + days[i]["date_day"] + ": "
            if name_site == "яндекс-погода":
                if days[i]["sunrise"]:
                    message += "Восход: " + days[i]["sunrise"]
                if days[i]["sunset"]:
                    message += " - Закат: " + days[i]["sunset"]
            message += "\n"
            for j in range(len(days[i]["time_day"])):
                message += days[i]["time_day"][j] + "\n"
                message += days[i]["temperature"][j] + "; "
                message += days[i]["weather"][j] + "; "
                message += "Ветер: " + days[i]["wind"][j] + ";"
                if name_site == "гисметео":
                    message += "Осадки: " + days[i]["precipitation"][j] + ";\n"
                else:
                    message += "\n"
    except Exception as ex:
        print(f"Что то пошло не так, не могу составить сообщение с {name_site}; Ошибка {ex}")
        return f"Что то пошло не так, не могу составить сообщение с {name_site}; Ошибка {ex}"
    print("Готово")
    return message


def main(count_days):
    message = get_weather_gismeteo(count_days) + "\n\n" + get_weather_yandex(count_days)
    return message
