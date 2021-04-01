import os
from random import Random

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from app.commands import *
from app.config import PATH
from app.keyboards import keyboard
from app.messages import welcome_msg, lang, QUESTION_NOT_EXIST


async def back(message: types.message, state: FSMContext):
    await General.previous()
    await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                        reply_markup=await keyboard(message, state))


async def question_type_select(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data["mode"] = message.text
    if message.text in RANDOM_QUESTION.values():
        path = await random_path(await random_path(await random_path(PATH)))
        await print_task(path, message, state)
    else:
        await General.WAITING_COURSE.set()
        await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                            reply_markup=await keyboard(message, state))


async def print_modules(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data["course"] = PATH + "/" + message.text
    mode = data["mode"]
    if mode in RANDOM_COURSE_QUESTION.values():
        path = await random_path(await random_path(data["course"]))
        await print_task(path, message, state)
    else:
        await General.WAITING_MODULE.set()
        await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                            reply_markup=await keyboard(message, state))


async def print_questions(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data["module"] = data["course"] + "/" + message.text
    mode = data["mode"]
    if mode in RANDOM_MODULE_QUESTION.values():
        path = await random_path(data["module"])
        await print_task(path, message, state)
    else:
        await General.WAITING_QUESTION.set()
        await message.reply(welcome_msg[await state.get_state()][lang(message)], reply=False,
                            reply_markup=await keyboard(message, state))


async def random_path(cur_path: str):
    lst = os.listdir(cur_path)
    return cur_path + "/" + lst[Random().randrange(0, len(lst))]


async def process_concrete(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        pass
    await print_task(data["module"] + "/" + message.text, message, state)


async def print_task(path: str, message: types.message, state: FSMContext):
    await General.WAITING_ANSWER.set()
    async with state.proxy() as data:
        data["question"] = path
    name = os.path.basename(path)
    await message.reply(name, reply=False, reply_markup=await keyboard(message, state))


async def print_answer(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        pass
    path = data["question"]
    await state.reset_state()
    if not os.path.isdir(path):
        await message.reply(QUESTION_NOT_EXIST[lang(message)], reply=False, reply_markup=await keyboard(message, state))
    media = types.MediaGroup()
    for file in os.listdir(path):
        media.attach_document(types.InputFile(path + "/" + file), "file: " + file)
    await message.reply_media_group(media, reply=False)
    await message.reply("Here it is", reply=False, reply_markup=await keyboard(message, state))


class General(StatesGroup):
    WAITING_QUESTION_TYPE = State()
    WAITING_COURSE = State()
    WAITING_MODULE = State()
    WAITING_QUESTION = State()
    WAITING_ANSWER = State()

    def __init__(self, dispatcher: Dispatcher):
        self.dp = dispatcher

    def register_handler(self):
        self.dp.register_message_handler(back, lambda m: m.text in BACK.values(), state=General.all_states)
        self.dp.register_message_handler(question_type_select,
                                         lambda m: m.text in RANDOM_QUESTION.values()
                                                   or m.text in RANDOM_COURSE_QUESTION.values()
                                                   or m.text in RANDOM_MODULE_QUESTION.values()
                                                   or m.text in CONCRETE_QUESTION.values(),
                                         state=General.WAITING_QUESTION_TYPE)
        self.dp.register_message_handler(print_modules, state=General.WAITING_COURSE)
        self.dp.register_message_handler(print_questions, state=General.WAITING_MODULE)
        self.dp.register_message_handler(process_concrete, state=General.WAITING_QUESTION)
        self.dp.register_message_handler(print_answer, lambda m: m.text in GET_ANSWER.values(),
                                         state=General.WAITING_ANSWER)
        self.dp.register_message_handler(app.handlers.start.unknown, state=General.all_states)
