from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app.config import MODERATORS
from app.commands import MODER_PANEL, BACK, ADD_MODER, DEL_MODER
from app.keyboards import keyboard
from app.messages import lang, welcome_msg, MODER_ADDED, MODER_DELETED, WRONG_MODER


async def moderator_panel(message: types.message, state: FSMContext):
    await app.handlers.moderator.Moder.MODERATOR_PANEL.set()
    await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


async def back(message: types.message, state: FSMContext):
    await Admin.previous()
    await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


async def print_moders(message: types.message, state: FSMContext):
    await Admin.WAITING_MODER.set()
    async with state.proxy() as data:
        if message.text in ADD_MODER.values():
            data["mode"] = "add"
        else:
            data["mode"] = "delete"
    await app.handlers.admin.Admin.WAITING_MODER.set()
    await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


async def add_del_moder(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        mode = data["mode"]
    if mode == "add":
        await app.handlers.admin.Admin.ADMIN_PANEL.set()
        MODERATORS.append(message.text)
        msg = MODER_ADDED[lang(message)]
    else:
        if message.text not in MODERATORS:
            msg = WRONG_MODER[lang(message)]
        else:
            await app.handlers.admin.Admin.ADMIN_PANEL.set()
            MODERATORS.remove(message.text)
            msg = MODER_DELETED[lang(message)]
    await message.reply(msg, reply=False, reply_markup=await keyboard(message, state))


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
        self.dp.register_message_handler(app.handlers.start.unknown, state=Admin.all_states)
