import os

from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup

import exam_bot
from exam_bot.commands import *
from exam_bot.config import *
from exam_bot.messages import *


async def keyboard(m: types.Message, state: FSMContext) -> ReplyKeyboardMarkup:
    s = None
    if state is not None:
        s = await state.get_state()
    if s is None:
        return await default_keyboard(m)
    elif s == "General:WAITING_QUESTION_TYPE":
        return QUESTION_TYPE_KEYBOARD[lang(m)]
    elif s == "General:WAITING_COURSE" or s == "Moder:WAITING_COURSE":
        return await COURSE_LIST_KEYBOARD(m)
    elif s == "General:WAITING_MODULE" or s == "Moder:WAITING_MODULE":
        return await MODULE_LIST_KEYBOARD(m, state)
    elif s == "General:WAITING_QUESTION" or s == "Moder:WAITING_QUESTION":
        return await QUESTION_LIST_KEYBOARD(m, state)
    elif s == "General:WAITING_ANSWER":
        return WAIT_ANSWER_KEYBOARD[lang(m)]
    elif s == "Admin:ADMIN_PANEL":
        return ADMIN_PANEL_KEYBOARD[lang(m)]
    elif s == "Admin:WAITING_MODER":
        return await WAITING_MODER_KEYBOARD(m)
    elif s == "Moder:MODERATOR_PANEL":
        return MODERATOR_PANEL_KEYBOARD[lang(m)]
    elif s == "Moder:WAITING_ANSWER":
        return BACK_KEYBOARD[lang(m)]


# Functions get message and state, dictionaries -- language (str)

DEFAULT_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(GET_QUESTION[lang], ABOUT[lang])
    for lang in LANGUAGES
}

DEFAULT_ADMIN_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(GET_QUESTION[lang], ABOUT[lang])
            .row(ADMIN_PANEL[lang])
    for lang in LANGUAGES
}

DEFAULT_MODERATOR_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(GET_QUESTION[lang], ABOUT[lang])
            .row(MODER_PANEL[lang])
    for lang in LANGUAGES
}

WAIT_ANSWER_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(GET_ANSWER[lang], BACK[lang])
    for lang in LANGUAGES
}

ADMIN_PANEL_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(ADD_MODER[lang], DEL_MODER[lang])
            .row(MODER_PANEL[lang])
            .row(BACK[lang])
    for lang in LANGUAGES
}

MODERATOR_PANEL_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(ADD_QUESTION[lang], DEL_QUESTION[lang])
            .row(DEL_COURSE[lang], DEL_MODULE[lang])
            .row(BACK[lang])
    for lang in LANGUAGES
}

BACK_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(BACK[lang])
    for lang in LANGUAGES
}

QUESTION_TYPE_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(RANDOM_QUESTION[lang], RANDOM_COURSE_QUESTION[lang])
            .row(RANDOM_MODULE_QUESTION[lang], CONCRETE_QUESTION[lang])
            .row(BACK[lang])
    for lang in LANGUAGES
}


async def COURSE_LIST_KEYBOARD(m: types.Message) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(BACK[lang(m)])
    if os.path.isdir(PATH):
        markup.add(*os.listdir(PATH))
    return markup


async def MODULE_LIST_KEYBOARD(m: types.Message, state: FSMContext) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(BACK[lang(m)])
    async with state.proxy() as data:
        if os.path.isdir(data["course"]):
            markup.add(*os.listdir(data["course"]))
    return markup


async def QUESTION_LIST_KEYBOARD(m: types.Message, state: FSMContext) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(BACK[lang(m)])
    async with state.proxy() as data:
        if os.path.isdir(data["module"]):
            markup.add(*os.listdir(data["module"]))
    return markup


async def WAITING_MODER_KEYBOARD(m: types.Message) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(BACK[lang(m)])
    if m.text in DEL_MODER.values():
        for MODERATOR in await exam_bot.handlers.start.get_moders():
            markup.add(MODERATOR)
    return markup


async def default_keyboard(m: types.Message) -> ReplyKeyboardMarkup:
    if m.from_user.id == OWNER_ID:
        return DEFAULT_ADMIN_KEYBOARD[lang(m)]
    elif str(m.from_user.id) in await exam_bot.handlers.start.get_moders():
        return DEFAULT_MODERATOR_KEYBOARD[lang(m)]
    return DEFAULT_KEYBOARD[lang(m)]
