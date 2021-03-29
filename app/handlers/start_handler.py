from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup


async def start(message: types.Message):
    await message.reply(StartHandler.messages["help"], reply=False)


async def get_id(message: types.Message):
    await message.reply(message.from_user.id, reply=False)


class StartHandler(StatesGroup):
    def __init__(self, dispatcher: Dispatcher):
        self.dp = dispatcher

    HELP = {"help", "start", "/help", "/start", "About", "О боте"}

    messages = {
        "help":
            "Привет! Если нужна помощь в подготовке к экзамену, можешь попросить меня "
            "присылать тебе задания.\nЯ могу собирать статистику, задавать вопросы, "
            "в которых больше всего ошибок, и постоянно напоминать тебе о важности учебы.\n"
    }

    def register_handler(self):
        self.dp.register_message_handler(start, lambda m: m.text in self.HELP, state=None)
        self.dp.register_message_handler(get_id, commands="getId", state=None)
