# -*- coding: utf8 -*-
import re
import info_wiki
import get_weather
import get_games
import os
import get_translation
from aiogram import Bot, Dispatcher, executor, types
from autn_token import token
from aiogram.dispatcher.filters import Text


bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["/start", "/погода", "игры", "/перевод", "/вики"]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("/погода - узнать погоду,\n"
                         "/игры - узнать новинки на торренте\n"
                         "/перевод - перевести предыдущее сообщение, на другой язык\n"
                         "/вики", reply_markup=keyboard)


@dp.message_handler(Text)
async def send_text(message: types.Message):

    if not os.path.exists(f"message_user\\{message.from_user.username}_{ message.from_user.id}"):
        with open(f"message_user\\{message.from_user.username}_{message.from_user.id}",
                  "w", encoding="utf-8") as file:
            file.write(message.text + "\n")
    else:
        with open(f"message_user\\{message.from_user.username}_{message.from_user.id}",
                  "a", encoding="utf-8") as file:
            file.write(message.text + "\n")

    with open("data\\commands.dat", "r") as file:
        list_commands = file.readlines()

        for number, command in enumerate(list_commands):
            command = command.replace("\n", "")
            if re.compile(command).findall(message.text.lower()):
                num = number

                # погода
                if num == 0:
                    count_days = re.compile(command).findall(message.text.lower())
                    if count_days[0] != "":
                        count_days = int(count_days[0])
                    else:
                        count_days = 2
                    await message.answer("Понял, начинаю сбор информации...")
                    await message.answer(get_weather.main(count_days))

                # игры
                if num == 1:
                    count_games = re.compile(command).findall(message.text.lower())
                    if count_games[0] != "":
                        count_games = int(count_games[0])
                    else:
                        count_games = 2
                    await message.answer("Принял, сейчас найду...")
                    await message.answer(get_games.main(count_games))

                # перевод
                if num == 2:
                    out_language = re.compile(command).findall(message.text.lower())[0]
                    with open(f"message_user\\{message.from_user.username}_{message.from_user.id}",
                              "r", encoding="utf-8") as f:
                        messages = f.readlines()

                    await message.answer("ОК, понял...")
                    await message.answer(get_translation.main(messages[-2], out_language))

                # википедия
                if num == 3:
                    with open(f"message_user\\{message.from_user.username}_{message.from_user.id}",
                              "r", encoding="utf-8") as f:
                        messages = f.readlines()
                    await message.answer("Понял, начинаю поиск...")
                    await message.answer(info_wiki.main(messages[-2]))

                message.text = "!!!DONE!!!"
                break

    if message.text != "!!!DONE!!!":
        if message.text.lower() == "привет":
            await message.answer("Привет, " + message.from_user.first_name + "!")
        else:
            await message.answer("Не понял, что?")


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
