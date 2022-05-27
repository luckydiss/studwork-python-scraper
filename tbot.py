from os import getenv
from async_scrapper import main
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os

TOKEN = ''
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Программирование', 'Математика']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Please select a discipline', reply_markup=keyboard)

@dp.message_handler(Text(equals='Программирование'))
async def mathematics(message: types.Message):
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(chat_id=chat_id)

@dp.message_handler(Text(equals='Математика'))
async def programming(message: types.Message):
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(chat_id=chat_id)

async def send_data(disc_code='', chat_id=''):
    file = await main()
    await bot.send_document(chat_id=chat_id, document=open(file, 'rb'))
    await os.remove(file)

if __name__ == '__main__':
    executor.start_polling(dp)
