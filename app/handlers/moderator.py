import os
import shutil
from os import path
from typing import List

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType

from app.commands import *
from app.config import *
from app.keyboards import keyboard
from app.messages import *


async def back(message: types.message, state: FSMContext):
    if message.from_user.id == OWNER_ID and await state.get_state() == "Moder:MODERATOR_PANEL":
        await app.handlers.admin.Admin.ADMIN_PANEL.set()
        await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                            reply_markup=await keyboard(message, state))
    else:
        await Moder.previous()
        await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                            reply_markup=await keyboard(message, state))


async def print_courses(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data["mode"] = message.text
    await Moder.WAITING_COURSE.set()
    await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


async def print_modules(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data["course"] = PATH + "/" + message.text
    mode = data["mode"]
    if mode in DEL_COURSE.values():
        await Moder.MODERATOR_PANEL.set()
        await delete_dir(data["course"], 0)
        await successfully_deleted(message, state)
    else:
        await Moder.WAITING_MODULE.set()
        await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False, reply_markup=await keyboard(message, state))


async def print_questions(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data["module"] = data["course"] + "/" + message.text
    mode = data["mode"]
    if mode in DEL_MODULE.values():
        await Moder.MODERATOR_PANEL.set()
        await delete_dir(data["module"], 1)
        await successfully_deleted(message, state)
    else:
        await Moder.WAITING_QUESTION.set()
        await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                            reply_markup=await keyboard(message, state))


async def ask_answer(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data["question"] = data["module"] + "/" + message.text
    mode = data["mode"]
    if mode in DEL_QUESTION.values():
        await Moder.MODERATOR_PANEL.set()
        await delete_dir(data["question"], 2)
        await successfully_deleted(message, state)
    else:
        await Moder.WAITING_ANSWER.set()
        await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                            reply_markup=await keyboard(message, state))


async def successfully_deleted(message: types.message, state: FSMContext):
    await message.reply(SUCCESSFUL[lang(message)], reply=False, reply_markup=await keyboard(message, state))


async def delete_dir(cur_path: str, depth: int):
    shutil.rmtree(cur_path)
    while depth != 0:
        cur_path = os.path.dirname(cur_path)
        if not os.listdir(cur_path):
            shutil.rmtree(cur_path)
            depth -= 1
        else:
            break


async def load_answer(message: types.message, state: FSMContext, album: List[types.Message] = None):
    await Moder.MODERATOR_PANEL.set()
    if album is None:
        album = [message]
    async with state.proxy() as data:
        s = data["question"]
        if not path.isdir(s):
            os.makedirs(s)
    bot = Bot.get_current()
    for (idx, obj) in enumerate(album):
        if obj.photo:
            file = obj.photo[-1]
        else:
            file = obj[obj.content_type]
        file_path = (await bot.get_file(file.file_id)).file_path
        await file.download(s + "/" + str(idx) + path.splitext(file_path)[1])
    await message.reply(SUCCESSFUL[lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


class Moder(StatesGroup):
    MODERATOR_PANEL = State()
    WAITING_COURSE = State()
    WAITING_MODULE = State()
    WAITING_QUESTION = State()
    WAITING_ANSWER = State()

    def __init__(self, dispatcher: Dispatcher):
        self.dp = dispatcher

    def register_handler(self):
        self.dp.register_message_handler(back, lambda m: m.text in BACK.values(), state=Moder.all_states)
        self.dp.register_message_handler(print_courses,
                                         lambda m: m.text in ADD_QUESTION.values()
                                                   or m.text in DEL_QUESTION.values()
                                                   or m.text in DEL_MODULE.values()
                                                   or m.text in DEL_COURSE.values(),
                                         state=self.MODERATOR_PANEL)
        self.dp.register_message_handler(print_modules, state=self.WAITING_COURSE)
        self.dp.register_message_handler(print_questions, state=self.WAITING_MODULE)
        self.dp.register_message_handler(ask_answer, state=self.WAITING_QUESTION)
        self.dp.register_message_handler(load_answer, is_media_group=True, state=self.WAITING_ANSWER,
                                         content_types=ContentType.ANY)
        self.dp.register_message_handler(load_answer, state=self.WAITING_ANSWER, content_types=ContentType.ANY)
        self.dp.register_message_handler(app.handlers.start.unknown, state=Moder.all_states)
