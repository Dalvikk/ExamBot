from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import exam_bot.handlers
from exam_bot.commands import *
from exam_bot.messages import *


async def moderator_panel(message: types.message, state: FSMContext):
    await exam_bot.handlers.moderator.Moder.MODERATOR_PANEL.set()
    await exam_bot.handlers.start.reply_welcome(message, state)


async def back(message: types.message, state: FSMContext):
    await Admin.previous()
    await exam_bot.handlers.start.reply_welcome(message, state)


async def print_moders(message: types.message, state: FSMContext):
    await Admin.WAITING_MODER.set()
    async with state.proxy() as data:
        if message.text in ADD_MODER.values():
            data["mode"] = "add"
        else:
            data["mode"] = "delete"
    await exam_bot.handlers.admin.Admin.WAITING_MODER.set()
    await exam_bot.handlers.start.reply_welcome(message, state)


async def add_del_moder(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        mode = data["mode"]
    if mode == "add":
        await exam_bot.handlers.admin.Admin.ADMIN_PANEL.set()
        await exam_bot.handlers.start.add_moder(message.text)
        await exam_bot.handlers.start.reply_by_dict(MODER_ADDED, message, state)
    else:
        if not await exam_bot.handlers.start.is_moder(message.text):
            await exam_bot.handlers.start.reply_by_dict(WRONG_MODER, message, state)
        else:
            await exam_bot.handlers.admin.Admin.ADMIN_PANEL.set()
            await exam_bot.handlers.start.del_moder(message.text)
            await exam_bot.handlers.start.reply_by_dict(MODER_DELETED, message, state)


class Admin(StatesGroup):
    ADMIN_PANEL = State()
    WAITING_MODER = State()

    def __init__(self, dispatcher: Dispatcher):
        self.dp = dispatcher

    def register_handler(self):
        self.dp.register_message_handler(back, lambda m: m.text in BACK.values(), state=Admin.all_states)
        self.dp.register_message_handler(print_moders,
                                         lambda m: m.text in ADD_MODER.values() or m.text in DEL_MODER.values(),
                                         state=self.ADMIN_PANEL)
        self.dp.register_message_handler(add_del_moder, state=self.WAITING_MODER)
        self.dp.register_message_handler(moderator_panel, lambda m: m.text in MODER_PANEL.values(),
                                         state=self.ADMIN_PANEL)
        self.dp.register_message_handler(exam_bot.handlers.start.unknown, state=Admin.all_states)
