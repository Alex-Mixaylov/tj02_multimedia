import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo'))
async def down_photo(message:Message):
    list = ['https://fikiwiki.com/uploads/posts/2022-02/1644991183_16-fikiwiki-com-p-kartinki-krasivikh-koshechek-24.jpg',
            'https://funik.ru/wp-content/uploads/2018/10/17478da42271207e1d86.jpg',
            'https://furman.top/uploads/posts/2022-06/1655449861_20-furman-top-p-koti-na-rabochii-stol-23.jpg'
            ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')
@dp.message(F.photo)
async def upload_photo(message:Message):
    list = ['Ого, какая фотка', 'Не присылай мне больше такое!', 'Непонятно что это']
    rand_answer = random.choice(list)
    await message.answer(rand_answer)
@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message:Message):
    await message.answer('Искусственный интеллект (ИИ) — это область компьютерных наук, занимающаяся созданием систем, способных выполнять задачи, требующие человеческого интеллекта, такие как обучение, распознавание речи, принятие решений и решение проблем.')
@dp.message(Command('help'))
async def help(message:Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start - Начало работы \n /help - Справка')
@dp.message(CommandStart())
async def start(message:Message):
    await message.answer('Приветики! Я бот:)')

async def main():
    await dp.start_polling(bot)

if __name__ =='__main__':
    asyncio.run(main())