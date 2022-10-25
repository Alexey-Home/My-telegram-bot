# -*- coding: utf8 -*-
import re
import get_weather
import get_games
from aiogram import Bot, Dispatcher, executor, types
from autn_token import token
from aiogram.dispatcher.filters import Text


bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Команды"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Приветствую Вас!!!", reply_markup=keyboard)


@dp.message_handler(Text(equals="Команды"))
async def send_text(message: types.Message):
    await message.answer("/погода - узнать погоду\n"
                         "/игры - узнать новинки на торренте")


@dp.message_handler(Text)
async def send_text(message: types.Message):

    with open("data\commands.dat", "r") as file:
        list_commands = file.readlines()
        file.close()

        for number, command in enumerate(list_commands):
            command = command.replace("\n", "")
            if re.compile(command.replace("\n", "")).findall(message.text.lower()):
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

                message.text = "!!!DONE!!!"
                break

    if message.text != "!!!DONE!!!":
        if message.text.lower() == "привет":
            await message.answer("Привет, Леха")
        else:
            await message.answer("Не понял, что?")


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()

