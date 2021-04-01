from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup

import exam_bot.bot
import exam_bot.handlers
from exam_bot import config
from exam_bot.commands import *
from exam_bot.config import OWNER_ID
from exam_bot.keyboards import keyboard
from exam_bot.messages import *


async def getOrSetDefault(state: FSMContext, key: str, default):
    exam_bot.bot.db = await state.get_data()
    if key in exam_bot.bot.db:
        return exam_bot.bot.db[key]
    else:
        exam_bot.bot.db[key] = default
        return default


# Send msg to the user's language with keyboard
async def reply(msg: str, message: types.message, state: FSMContext):
    await message.reply(msg, reply=False, reply_markup=await keyboard(message, state))


# Get messages dict and send msg corresponding to the user's language with keyboard
async def reply_by_dict(text_dict: dict, message: types.message, state: FSMContext):
    await message.reply(text_dict[lang(message)], reply=False, reply_markup=await keyboard(message, state))


async def reply_welcome(message: types.message, state: FSMContext):
    await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


async def is_moder(user_id: str):
    return user_id in await get_moders()


async def add_moder(user_id: str):
    await exam_bot.bot.db.update_one({'name': 'moderators'}, {'$push': {"moderators": user_id}})


async def del_moder(user_id: str):
    await exam_bot.bot.db.update_one({'name': 'moderators'}, {'$pull': {"moderators": user_id}})


async def get_moders():
    return (await exam_bot.bot.db.find_one({"name": "moderators"}))["moderators"]


async def start(message: types.message, state: FSMContext):
    await reply_by_dict(HELP_MSG, message, state)


async def get_id(message: types.message, state: FSMContext):
    await reply(str(message.from_user.id), message, state)


async def admin_panel(message: types.message, state: FSMContext):
    if message.from_user.id != OWNER_ID:
        await unknown(message, state)
    else:
        await exam_bot.handlers.admin.Admin.ADMIN_PANEL.set()
        await reply_welcome(message, state)


async def moder_panel(message: types.message, state: FSMContext):
    if not await is_moder(str(message.from_user.id)):
        await unknown(message, state)
    else:
        await exam_bot.handlers.moderator.Moder.MODERATOR_PANEL.set()
        await reply_welcome(message, state)


async def get_question(message: types.message, state: FSMContext):
    await exam_bot.handlers.general.General.WAITING_QUESTION_TYPE.set()
    await reply_welcome(message, state)


async def unknown(message: types.message, state: FSMContext):
    await reply_by_dict(UNKNOWN_MSG, message, state)


async def back(message: types.message, state: FSMContext):
    await state.reset_state(with_data=False)
    await reply_welcome(message, state)


async def get_state(message: types.message, state: FSMContext):
    await reply(str(await state.get_state()), message, state)


async def error(update, exception):
    if config.ERRORS_IN_CHAT:
        await Bot.get_current().send_message(OWNER_ID, f"Error happened! {exception}")
    await update.message.reply("Error happened! Please, contact the developer")


class Start(StatesGroup):
    def __init__(self, dispatcher: Dispatcher):
        self.dp = dispatcher

    def register_handler(self):
        self.dp.register_errors_handler(error)
        self.dp.register_message_handler(start, lambda m: m.text == "/start" or m.text in ABOUT.values(),
                                         state=None)
        self.dp.register_message_handler(get_question, lambda m: m.text in GET_QUESTION.values(), state=None)
        self.dp.register_message_handler(get_id, commands="getId", state=None)
        self.dp.register_message_handler(admin_panel, lambda m: m.text in ADMIN_PANEL.values(), state=None)
        self.dp.register_message_handler(moder_panel, lambda m: m.text in MODER_PANEL.values(), state=None)
        self.dp.register_message_handler(back, lambda m: m.text in BACK.values(), state=None)
        self.dp.register_message_handler(get_state, commands="getstate", state="*")
        self.dp.register_message_handler(unknown, state=None)
