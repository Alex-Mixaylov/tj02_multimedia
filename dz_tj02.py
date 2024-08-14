import asyncio
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from gtts import gTTS
from googletrans import Translator

# Загрузка токена из .env файла
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Инициализация переводчика
translator = Translator()

# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.full_name}')

# Команда /fotosave для сохранения фото
@dp.message(Command('fotosave'))
async def fotosave(message: Message):
    await message.answer('Отправьте мне фото, и я сохраню его.')

@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Сохранение фото в папку img
    destination = f'img/{file_id}.jpg'
    await bot.download_file(file_path, destination)

    await message.answer(f'Фото сохранено как {destination}')

# Команда /voice для отправки голосового сообщения
@dp.message(Command('voice'))
async def send_voice(message: Message):
    # Проверяем, существует ли уже voice.ogg, если нет — создаем его
    if not os.path.exists('voice.ogg'):
        text = ("Aiogram — это асинхронная библиотека для Python, "
                "предназначенная для создания ботов в Telegram. "
                "Она поддерживает работу с API Telegram и позволяет "
                "легко создавать и управлять ботами. Aiogram работает на базе asyncio, "
                "что делает её высокопроизводительной и эффективной, "
                "особенно в обработке множества сообщений одновременно. "
                "Aiogram позволяет быстро разрабатывать сложные и функциональные боты, "
                "используя мощные встроенные фильтры и декораторы.")
        tts = gTTS(text, lang='ru')
        tts.save("voice.ogg")

    # Отправка голосового сообщения
    audio = FSInputFile("voice.ogg")
    await bot.send_voice(chat_id=message.chat.id, voice=audio)
    await message.answer('Отправлено голосовое сообщение.')

# Команда /translate для перевода текста на английский язык
@dp.message(Command('translate'))
async def translate(message: Message):
    await message.answer('Отправьте текст, который нужно перевести на английский язык.')

@dp.message(lambda message: not message.text.startswith('/'))
async def handle_text(message: Message):
    translated = translator.translate(message.text, dest='en')
    await message.answer(f'Перевод на английский: {translated.text}')

# Команда /help с перечислением доступных команд
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Этот бот умеет выполнять команды: \n'
        '/start - Начало работы \n'
        '/help - Справка \n'
        '/fotosave - Сохранить фото \n'
        '/voice - Отправить голосовое сообщение \n'
        '/translate - Перевести текст на английский'
    )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
