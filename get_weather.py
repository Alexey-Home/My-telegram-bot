# -*- coding: utf8 -*-
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
        print("Открываю страницу гисметео...")
        driver.get(url=url)
        time.sleep(5)
        print("Сохраняю страницу гисметео...")
        with open("index_g.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
        return "Что то пошло не так, не могу перейти по ссылке..."
    finally:
        driver.close()
        driver.quit()
    print("Готово")

    with open("index_g.html", "r", encoding="utf-8") as file:
        page_html = file.read()
    try:
        print("Собираю информацию: число, погода, температура, ветер, осадки...")
        soup = BeautifulSoup(page_html, "lxml")

        src = soup.find("div", class_="widget-date-wrap")\
            .find_all("a", class_=re.compile(r"item item-day-[0-9] link date-left"))
        date_days = get_value(src)
        src = soup.find("div", class_="widget-row widget-row-icon").find_all("div", class_="row-item")

        weather = []
        for text in src:
            weather.append(text.find("div").get("data-text"))

        src = soup.find("div", class_="widget-row-chart widget-row-chart-temperature")\
            .find_all("span", class_="unit unit_temperature_c")
        temperature = get_value(src)

        src = soup.find("div", class_="widget-row widget-row-wind-speed-gust row-with-caption")\
            .find_all("span", class_="wind-unit unit unit_wind_m_s")
        wind = get_value(src)

        src = soup.find("div", class_="widget-row widget-row-precipitation-bars row-with-caption")\
            .find_all("div", class_="row-item")
        precipitation = get_value(src)
        print("Готово")
    except Exception as ex:
        print(ex)
        return "Что то пошло не так, не могу найти один из блоков."

    date_time = ["Ночь: ", "Утро: ", "День: ", "Вечер: "]

    print("Составляю текст сообщения с гисметео...")

    message = "https://www.gismeteo.ru/weather-arzamas-4377/3-days\n"
    try:
        for i in range(count_days):
            message += "-" * 60 + "\n"
            message += date_days[i] + "\n"
            for j in range(4):
                message += "\t" + date_time[j] + "\n\t\t" + temperature[0] + " " + weather[0]
                message += ", Ветер:" + wind[0] + ", Осадки:" + precipitation[0] + "\n"
                temperature.pop(0)
                weather.pop(0)
                wind.pop(0)
                precipitation.pop(0)
        print("Готово")
    except Exception as ex:
        print(ex)
        return "Что то пошло не так, не могу составить текст сообщения c гисметео"

    return message


def get_weather_yandex(count_days):
    """
    Переходит на страницу сайта яндекс-погода. Сохраняет ее.И со страницы собирает информацию:
    Число,погода,температура,ветер, рассвет, закат.
    Вовзращает составленое сообщение с гиметео.
    """

    url = "https://yandex.ru/pogoda/details?lat=55.38680267&lon=43.81413651&via=ms"

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
        print("Открываю страницу яндекс-погода...")
        driver.get(url=url)
        time.sleep(5)
        print("Сохраняю страницу яндекс-погода...")
        with open("index_y.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
        return "Не могу перейти на страницу яндекс-погода..."
    finally:
        driver.close()
        driver.quit()
    print("Готово")

    with open("index_y.html", "r", encoding="utf-8") as file:
        page_html = file.read()

    try:
        soup = BeautifulSoup(page_html, "lxml")
        cards = soup.find_all("article", class_=re.compile("card"))
    except Exception as ex:
        print(ex)
        return "Что то пошло не так, не могу найти блок..."

    date_days = []
    temperature = []
    weather = []
    wind = []
    sunrise = []
    sunset = []
    print("Собираю информацию: число, температура, погода, ветер, рассвет, закат")
    for card in cards:
        try:
            date_days.append(card.find("strong", class_="forecast-details__day-number").text + " " + card
                             .find("span", class_="forecast-details__day-month").text)
            time_days = card.find_all("tr", class_="weather-table__row")
            for time_day in time_days:
                temperature.append(time_day.find("div", class_="weather-table__temp").text)
                weather.append(
                    time_day.find("td", class_="weather-table__body-cell weather-table__body-cell_type_condition").text)
                wind.append(time_day.find("span", class_="weather-table__wind").text)
            sunrise.append(
                card.find("dl", class_="sunrise-sunset__description sunrise-sunset__description_value_sunrise")
                .find("dd", class_="sunrise-sunset__value").text)
            sunset.append(
                card.find("dl", class_="sunrise-sunset__description sunrise-sunset__description_value_sunset")
                .find("dd", class_="sunrise-sunset__value").text)

        except Exception as ex:
            print(ex)
            continue
    print("Готов")

    date_time = ["Ночь: ", "Утро: ", "День: ", "Вечер: "]

    print("Составляю текст сообщения с яндекс-погоды...")
    message = "https://yandex.ru/pogoda/details?lat=55.38680267&lon=43.81413651&via=ms\n"
    try:
        for i in range(count_days):
            message += "-" * 60 + "\n"
            message += date_days[i] + ": Восход:" + sunrise[0] + "-Закат:" + sunset[0] + "\n"
            for j in range(4):
                message += "\t" + date_time[j] + "\n\t\t" + temperature[0] + ", "\
                           + weather[0] + ", Ветер:" + wind[0] + "\n"
                temperature.pop(0)
                weather.pop(0)
                wind.pop(0)
            sunrise.pop(i)
            sunset.pop(i)
    except Exception as ex:
        print(ex)
        return "Что то пошло не так, не могу составить сообщение с яндекс-погоды..."
    print("Готово")

    return message


def get_value(src):
    tmp = []
    for i in src:
        tmp.append(i.text.strip())
    return tmp


def main(count_days):
    message = get_weather_gismeteo(count_days) + "\n\n" + get_weather_yandex(count_days)
    return message
