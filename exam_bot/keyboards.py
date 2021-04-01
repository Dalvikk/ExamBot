import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup

import exam_bot.commands
import exam_bot.config
import exam_bot.messages
import exam_bot.handlers


async def keyboard(m: types.Message, state: FSMContext) -> ReplyKeyboardMarkup:
    s = None
    if state is not None:
        s = await state.get_state()
    if s is None:
        return await default_keyboard(m)
    elif s == "General:WAITING_QUESTION_TYPE":
        return QUESTION_TYPE_KEYBOARD[exam_bot.messages.lang(m)]
    elif s == "General:WAITING_COURSE" or s == "Moder:WAITING_COURSE":
        return await COURSE_LIST_KEYBOARD(m)
    elif s == "General:WAITING_MODULE" or s == "Moder:WAITING_MODULE":
        return await MODULE_LIST_KEYBOARD(m, state)
    elif s == "General:WAITING_QUESTION" or s == "Moder:WAITING_QUESTION":
        return await QUESTION_LIST_KEYBOARD(m, state)
    elif s == "General:WAITING_ANSWER":
        return WAIT_ANSWER_KEYBOARD[exam_bot.messages.lang(m)]
    elif s == "Admin:ADMIN_PANEL":
        return ADMIN_PANEL_KEYBOARD[exam_bot.messages.lang(m)]
    elif s == "Admin:WAITING_MODER":
        return await WAITING_MODER_KEYBOARD(m)
    elif s == "Moder:MODERATOR_PANEL":
        return MODERATOR_PANEL_KEYBOARD[exam_bot.messages.lang(m)]
    elif s == "Moder:WAITING_ANSWER":
        return BACK_KEYBOARD[exam_bot.messages.lang(m)]


# Functions get message and state, dictionaries -- language (str)

DEFAULT_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(exam_bot.commands.GET_QUESTION[lang], exam_bot.commands.ABOUT[lang])
    for lang in exam_bot.messages.LANGUAGES
}

DEFAULT_ADMIN_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(exam_bot.commands.GET_QUESTION[lang], exam_bot.commands.ABOUT[lang])
            .row(exam_bot.commands.ADMIN_PANEL[lang])
    for lang in exam_bot.messages.LANGUAGES
}

DEFAULT_MODERATOR_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(exam_bot.commands.GET_QUESTION[lang], exam_bot.commands.ABOUT[lang])
            .row(exam_bot.commands.MODER_PANEL[lang])
    for lang in exam_bot.messages.LANGUAGES
}

WAIT_ANSWER_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(exam_bot.commands.GET_ANSWER[lang], exam_bot.commands.BACK[lang])
    for lang in exam_bot.messages.LANGUAGES
}

ADMIN_PANEL_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(exam_bot.commands.ADD_MODER[lang], exam_bot.commands.DEL_MODER[lang])
            .row(exam_bot.commands.MODER_PANEL[lang])
            .row(exam_bot.commands.BACK[lang])
    for lang in exam_bot.messages.LANGUAGES
}

MODERATOR_PANEL_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(exam_bot.commands.ADD_QUESTION[lang], exam_bot.commands.DEL_QUESTION[lang])
            .row(exam_bot.commands.DEL_COURSE[lang], exam_bot.commands.DEL_MODULE[lang])
            .row(exam_bot.commands.BACK[lang])
    for lang in exam_bot.messages.LANGUAGES
}

BACK_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(exam_bot.commands.BACK[lang])
    for lang in exam_bot.messages.LANGUAGES
}

QUESTION_TYPE_KEYBOARD = {
    lang:
        ReplyKeyboardMarkup(resize_keyboard=True)
            .row(exam_bot.commands.RANDOM_QUESTION[lang], exam_bot.commands.RANDOM_COURSE_QUESTION[lang])
            .row(exam_bot.commands.RANDOM_MODULE_QUESTION[lang], exam_bot.commands.CONCRETE_QUESTION[lang])
            .row(exam_bot.commands.BACK[lang])
    for lang in exam_bot.messages.LANGUAGES
}


async def COURSE_LIST_KEYBOARD(m: types.Message) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(exam_bot.commands.BACK[exam_bot.messages.lang(m)])
    if os.path.isdir(exam_bot.config.PATH):
        markup.add(*os.listdir(exam_bot.config.PATH))
    return markup


async def MODULE_LIST_KEYBOARD(m: types.Message, state: FSMContext) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(exam_bot.commands.BACK[exam_bot.messages.lang(m)])
    async with state.proxy() as data:
        if os.path.isdir(data["course"]):
            markup.add(*os.listdir(data["course"]))
    return markup


async def QUESTION_LIST_KEYBOARD(m: types.Message, state: FSMContext) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(exam_bot.commands.BACK[exam_bot.messages.lang(m)])
    async with state.proxy() as data:
        if os.path.isdir(data["module"]):
            markup.add(*os.listdir(data["module"]))
    return markup


async def WAITING_MODER_KEYBOARD(m: types.Message) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(exam_bot.commands.BACK[exam_bot.messages.lang(m)])
    if m.text in exam_bot.commands.DEL_MODER.values():
        for MODERATOR in await exam_bot.handlers.start.get_moders():
            markup.add(MODERATOR)
    return markup


async def default_keyboard(m: types.Message) -> ReplyKeyboardMarkup:
    if m.from_user.id == exam_bot.config.OWNER_ID:
        return DEFAULT_ADMIN_KEYBOARD[exam_bot.messages.lang(m)]
    elif str(m.from_user.id) in await exam_bot.handlers.start.get_moders():
        return DEFAULT_MODERATOR_KEYBOARD[exam_bot.messages.lang(m)]
    return DEFAULT_KEYBOARD[exam_bot.messages.lang(m)]
