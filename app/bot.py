from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start', 'help'])
async def process_help(message: types.Message):
    await message.reply("""
Привет! 
    Если нужна помощь в подготовке к экзамену, можешь попросить меня \
присылать тебе задания. 
    Я могу собирать статистику, задавать вопросы, \
в которых больше всего ошибок, и постоянно напоминать тебе о важности ученья.
    """)


@dispatcher.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dispatcher)
