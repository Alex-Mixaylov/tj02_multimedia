import asyncio
import random

import time
import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram import types

import imaplib
import email
from email.header import decode_header

from gtts import gTTS

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')


bot = Bot(token=TOKEN)
dp = Dispatcher()


# обработка загрузки exel файла
@dp.message(F.document)
async def react_document(message: types.Message):
    # Список поддерживаемых форматов файлов
    supported_formats = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
                         'application/vnd.ms-excel'
                         ]  # .xls

    # Получение информации о документе
    document = message.document

    # Проверка, является ли файл Excel документом
    if document.mime_type in supported_formats:
        file_id = document.file_id
        file_name = document.file_name
        file_path = f'tmp/{file_name}'

        # Скачивание файла
        await bot.download(document, destination=file_path)

        # Отправка ответа пользователю
        await message.answer(f'Файл {file_name} успешно сохранён в {file_path}')
    else:
        await message.answer('Этот формат файла не поддерживается. Пожалуйста, отправьте Excel файл.')


@dp.message(Command('photo'))
async def down_photo(message:Message):
    list = ['https://fikiwiki.com/uploads/posts/2022-02/1644991183_16-fikiwiki-com-p-kartinki-krasivikh-koshechek-24.jpg',
            'https://funik.ru/wp-content/uploads/2018/10/17478da42271207e1d86.jpg',
            'https://furman.top/uploads/posts/2022-06/1655449861_20-furman-top-p-koti-na-rabochii-stol-23.jpg'
            ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')
@dp.message(F.photo)
async def react_photo(message:Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше'
            ]
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1],destination=f'tmp/{message.photo[-1].file_id}.jpg')
@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message:Message):
    await message.answer('Искусственный интеллект (ИИ) — это область компьютерных наук, занимающаяся созданием систем, способных выполнять задачи, требующие человеческого интеллекта, такие как обучение, распознавание речи, принятие решений и решение проблем.')
@dp.message(Command('help'))
async def help(message:Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start - Начало работы \n /help - Справка')
@dp.message(CommandStart())
async def start(message:Message):
    await message.answer(f'Приветики, {message.from_user.first_name}') # Полное фио {message.from_user.full_name}

# @dp.message()
# async def empty(message: Message):
#     await message.answer("Я бот, я не умею обрабатывать такие сообщения.")

@dp.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)
async def main():
    await dp.start_polling(bot)

if __name__ =='__main__':
    asyncio.run(main())