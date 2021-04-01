from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup

import app.handlers.general
import app.handlers.moderator
import app.handlers.admin
from app.config import OWNER_ID, MODERATORS
from app.commands import *
from app.keyboards import keyboard
from app.messages import *


async def start(message: types.message, state: FSMContext):
    await message.reply(HELP_MSG[lang(message)], reply=False, reply_markup=await keyboard(message, state))


async def get_id(message: types.message, state: FSMContext):
    await message.reply(message.from_user.id, reply=False, reply_markup=await keyboard(message, state))


async def admin_panel(message: types.message, state: FSMContext):
    await app.handlers.admin.Admin.ADMIN_PANEL.set()
    await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


async def moder_panel(message: types.message, state: FSMContext):
    await app.handlers.moderator.Moder.MODERATOR_PANEL.set()
    await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


async def get_question(message: types.message, state: FSMContext):
    await app.handlers.general.General.WAITING_QUESTION_TYPE.set()
    await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


async def unknown(message: types.message, state: FSMContext):
    await message.reply(UNKNOWN_MSG[lang(message)], reply=False, reply_markup=await keyboard(message, state))


async def back(message: types.message, state: FSMContext):
    await state.reset_state()
    await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


async def get_state(message: types.message, state: FSMContext):
    await message.reply(str(await state.get_state()), reply=False, reply_markup=await keyboard(message, state))


class Start(StatesGroup):
    def __init__(self, dispatcher: Dispatcher):
        self.dp = dispatcher

    def register_handler(self):
        self.dp.register_message_handler(start, lambda m: m.text == "/start" or m.text in ABOUT.values(),
                                         state=None)
        self.dp.register_message_handler(get_question, lambda m: m.text in GET_QUESTION.values(), state=None)
        self.dp.register_message_handler(get_id, commands="getId", state=None)
        self.dp.register_message_handler(admin_panel,
                                         lambda m: m.text in ADMIN_PANEL.values() and m.from_user.id == OWNER_ID,
                                         state=None)
        self.dp.register_message_handler(moder_panel,
                                         lambda m: m.text in MODER_PANEL.values() and str(
                                             m.from_user.id) in MODERATORS,
                                         state=None)
        self.dp.register_message_handler(back, lambda m: m.text in BACK.values(), state=None)
        self.dp.register_message_handler(get_state, commands="getstate", state="*")
        self.dp.register_message_handler(unknown, state=None)
