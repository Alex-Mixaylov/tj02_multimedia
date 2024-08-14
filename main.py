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
IMAP_SERVER = os.getenv('IMAP_SERVER')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# получение exel документов с почты email

def fetch_email_attachment():
    # Подключение к почтовому серверу
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)

    # Выбор папки для работы
    mail.select("inbox")

    # Поиск всех писем
    status, messages = mail.search(None, "ALL")

    # Получение списка писем
    email_ids = messages[0].split()

    for email_id in email_ids:
        # Получение конкретного письма
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')

                # Проверка на определённый текст в теме письма
                if "Excel Report" in subject:  # Измените "Excel Report" на нужный вам текст
                    # Проверка на вложение
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" in content_disposition:
                                # Сохранение файла
                                filename = part.get_filename()
                                if filename and (filename.endswith(".xlsx") or filename.endswith(".xls")):
                                    filepath = os.path.join("tmp", filename)
                                    with open(filepath, "wb") as f:
                                        f.write(part.get_payload(decode=True))

                                    # Возвращаем путь к файлу для дальнейшей обработки
                                    return filepath

    mail.logout()
    return None


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