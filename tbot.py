import asyncio
from async_scrapper import main
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os
import pandas as pd

TOKEN = ''
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    start_buttons = ['Программирование', 'Математика']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Please select a discipline', reply_markup=keyboard)

@dp.message_handler(Text(equals = 'Программирование'))
async def mathematics(message: types.Message):
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(chat_id=chat_id)

@dp.message_handler(Text(equals = 'Математика'))
async def programming(message: types.Message):
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(chat_id = chat_id)

async def send_data(disc_code='', chat_id=''):
    file = await main()
    await bot.send_document(chat_id = chat_id, document = open(file, 'rb'))

    df = pd.read_csv(open(file, 'rb'), sep = ';')
    #df = pd.read_csv('order_19_08_2022_09_18_async.csv', sep = ';')
    df = df.sort_values(by='start_date', ascending = True).reset_index()

    for i in range(len(df)):
        try:
            await bot.send_message(chat_id = chat_id, text = f"*{df['order_name'][i]}* \n {df['order_text'][i]} \n\n *Размещен:* {df['start_date'][i]} \n *Cрок сдачи:* {df['deadline_date'][i]} \n\n *Заказчик:* {df['user_name'][i]} \n\n *Ссылка:* {df['order_href'][i]}",
                                   parse_mode="Markdown")
        except:
            continue

    await os.remove(file)

    while True:
        file = await main()

        df1 = pd.read_csv(open(file, 'rb'), sep=';')
        # df = pd.read_csv('order_19_08_2022_09_18_async.csv', sep = ';')
        df1 = df1.sort_values(by='start_date', ascending=True).reset_index()

        for i in range(len(df1)):
            if df1['order_href'][i] not in df['order_href'].values:
                try:
                    await bot.send_message(chat_id=chat_id,
                                           text=f"*{df1['order_name'][i]}* \n {df1['order_text'][i]} \n\n \
                                           *Размещен:* {df1['start_date'][i]} \n *Cрок сдачи:* {df1['deadline_date'][i]}\
                                            \n\n *Заказчик:* {df1['user_name'][i]} \n\n *Ссылка:* {df1['order_href'][i]}",
                                           parse_mode="Markdown")
                except:
                    continue

        df = df1

        await asyncio.sleep(600)

        await os.remove(file)

if __name__ == '__main__':
    executor.start_polling(dp)
