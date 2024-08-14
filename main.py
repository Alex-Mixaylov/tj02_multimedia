import asyncio
import random

import time
import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram import types

from gtts import gTTS

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')


bot = Bot(token=TOKEN)
dp = Dispatcher()


# отправка голосовых сообщений
# @dp.message(Command('voice'))
# async def voice(message: Message):
#     training_list = [
#         "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
#         "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
#         "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
#     ]
#     rand_training = random.choice(training_list)
#     voice = FSInputFile("sample.ogg")
#     await message.answer_voice(voice)
#     tts = gTTS(text=rand_training, lang='ru')
#     tts.save("training.ogg")
#     audio = FSInputFile("training.ogg")
#     await bot.send_voice(chat_id=message.chat.id, voice=audio)
#     os.remove("training.ogg")

#озвучивание текста
@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")
   tts = gTTS(text=rand_tr, lang='ru')
   tts.save("training.mp3")
   audio = FSInputFile('training.mp3')
   await bot.send_audio(message.chat.id, audio)
   os.remove("training.mp3")

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
async def down_photo(message: Message):
    list = ['https://fikiwiki.com/uploads/posts/2022-02/1644991183_16-fikiwiki-com-p-kartinki-krasivikh-koshechek-24.jpg',
            'https://funik.ru/wp-content/uploads/2018/10/17478da42271207e1d86.jpg',
            'https://furman.top/uploads/posts/2022-06/1655449861_20-furman-top-p-koti-na-rabochii-stol-23.jpg'
            ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше'
            ]
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1],destination=f'tmp/{message.photo[-1].file_id}.jpg')
@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer('Искусственный интеллект (ИИ) — это область компьютерных наук, занимающаяся созданием систем, способных выполнять задачи, требующие человеческого интеллекта, такие как обучение, распознавание речи, принятие решений и решение проблем.')
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start - Начало работы \n /help - Справка')
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}') # Полное фио {message.from_user.full_name}

# @dp.message()
# async def empty(message: Message):
#     await message.answer("Я бот, я не умею обрабатывать такие сообщения.")
# @dp.message()
# async def testing(message: Message):
#     if message.text.lower() == 'test':
#         await message.answer('Тестируем')
@dp.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)
async def main():
    await dp.start_polling(bot)

if __name__ =='__main__':
    asyncio.run(main())