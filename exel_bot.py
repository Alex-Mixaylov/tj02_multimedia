import os
import asyncio
import imaplib
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()
TOKEN = os.getenv('TOKEN')
IMAP_SERVER = os.getenv('IMAP_SERVER')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Временные интервалы для проверки почты
CHECK_INTERVALS = [
    (datetime.time(10, 0), datetime.time(12, 0)),  # с 10:00 до 12:00
    # Добавьте другие интервалы, если необходимо
]


def is_within_check_intervals():
    """Проверяет, находится ли текущее время в одном из указанных интервалов."""
    current_time = datetime.datetime.now().time()
    for start_time, end_time in CHECK_INTERVALS:
        if start_time <= current_time <= end_time:
            return True
    return False


async def fetch_email_attachment():
    """Функция для подключения к почтовому серверу и обработки новых писем."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)

        # Периодическая проверка новых писем
        while is_within_check_intervals():
            mail.select("inbox")
            status, messages = mail.search(None, "UNSEEN")  # Поиск только новых писем

            if messages[0]:
                for email_id in messages[0].split():
                    status, msg_data = mail.fetch(email_id, "(RFC822)")
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            subject, encoding = email.header.decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else 'utf-8')

                            # Проверка на вложение
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_disposition = str(part.get("Content-Disposition"))
                                    if "attachment" in content_disposition:
                                        filename = part.get_filename()
                                        if filename and (filename.endswith(".xlsx") or filename.endswith(".xls")):
                                            filepath = os.path.join("tmp", filename)
                                            with open(filepath, "wb") as f:
                                                f.write(part.get_payload(decode=True))

                                            # Сохранение файла в папку tmp
                                            await save_file_to_tmp(filepath, filename)

                                            # Отправляем файл пользователю в Telegram
                                            await bot.send_document(chat_id=your_chat_id, document=open(filepath, 'rb'))

            await asyncio.sleep(60)  # Проверка раз в минуту

        mail.logout()
    except Exception as e:
        print(f"Ошибка при работе с почтовым сервером: {e}")


async def save_file_to_tmp(filepath, filename):
    """Сохранение файла в папку tmp."""
    # Здесь уже сохранён файл по пути filepath
    # Важно убедиться, что директория tmp существует
    os.makedirs('tmp', exist_ok=True)
    new_filepath = os.path.join('tmp', filename)
    os.rename(filepath, new_filepath)  # Перемещаем файл в папку tmp
    print(f"Файл {filename} успешно сохранён в {new_filepath}")


async def monitor_email():
    """Постоянный мониторинг почты с учётом временных интервалов."""
    while True:
        if is_within_check_intervals():
            print("Проверка почты...")
            await fetch_email_attachment()
        else:
            print("Вне временного интервала, ожидание...")
        await asyncio.sleep(60)  # Ожидание 1 минуту перед следующей проверкой


@dp.message(Command("start"))
async def start_handler(message: Message):
    """Обработчик команды /start."""
    await message.answer("Бот запущен и готов к работе!")


# Обработка загрузки Excel файла через Telegram
@dp.message(types.Message)
async def react_document(message: types.Message):
    """Обработчик документов, загружаемых в бот через Telegram."""
    supported_formats = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
                         'application/vnd.ms-excel']  # .xls

    document = message.document

    if document.mime_type in supported_formats:
        file_id = document.file_id
        file_name = document.file_name
        file_path = f'tmp/{file_name}'

        await bot.download(document, destination=file_path)
        await message.answer(f'Файл {file_name} успешно сохранён в {file_path}')
    else:
        await message.answer('Этот формат файла не поддерживается. Пожалуйста, отправьте Excel файл.')


async def on_startup(dp):
    """Запуск мониторинга почты при старте бота."""
    asyncio.create_task(monitor_email())


if __name__ == "__main__":
    from aiogram import executor

    # Запуск бота и передача on_startup для запуска мониторинга
    executor.start_polling(dp, on_startup=on_startup)
