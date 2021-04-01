from aiogram import types

LANGUAGES = ["ru"]


def lang(message: types.message) -> str:
    return "ru"


welcome_msg = {
    None: {
        "ru": "Главное меню"
    },

    "General:WAITING_QUESTION_TYPE": {
        "ru": "Выберите тип вопроса"
    },

    "General:WAITING_COURSE": {
        "ru": "Выберите курс"
    },

    "General:WAITING_MODULE": {
        "ru": "Выберите модуль"
    },

    "General:WAITING_QUESTION": {
        "ru": "Выберите вопрос"
    },

    "General:WAITING_ANSWER": {
        "ru": "Нажмите кнопку, чтобы узнать ответ, но сначала попробуйте ответить сами!"
    },

    "Admin:ADMIN_PANEL": {
        "ru": "Вы вошли в панель администратора"
    },

    "Admin:WAITING_MODER": {
        "ru": "Введите id модератора"
    },

    "Moder:MODERATOR_PANEL": {
        "ru": "Вы вошли в панель модератора"
    },

    "Moder:WAITING_COURSE": {
        "ru": "Выберите курс или введите название, если хотите создать новый"
    },

    "Moder:WAITING_MODULE": {
        "ru": "Выберите модуль или введите название, если хотите создать новый"
    },

    "Moder:WAITING_QUESTION": {
        "ru": "Выберите вопрос или введите название, если хотите создать новый"
    },

    "Moder:WAITING_ANSWER": {
        "ru": "Готово! Теперь пришлите мне альбом документов в том порядке, в котором их следует загрузить."
    }
}

UNKNOWN_MSG = {
    "ru": "Неизвестная комманда. Пожалуйста, попробуйте еще раз используя клавиатуру",
    "en": "Unknown command. Please, retry using keyboard"
}

HELP_MSG = {
    "ru": "Привет! Если нужна помощь в подготовке к экзамену, можешь попросить меня "
          "присылать тебе задания.\nЯ могу собирать статистику, задавать вопросы, "
          "в которых больше всего ошибок, и постоянно напоминать тебе о важности учебы.\n"
}

MODER_ADDED = {
    "ru": "Модератор успешно добавлен"
}

MODER_DELETED = {
    "ru": "Модератор успешно удален"
}

WRONG_MODER = {
    "ru": "Модератор с таким id не существует. Пожалуйста, повторите попытку используя клавиатуру ниже."
}

SUCCESSFUL = {
    "ru": "All done"
}

QUESTION_NOT_EXIST = {
    "ru": "Выбранный вами вопрос не существует. Пожалуйста, повторите попытку"
}

ANSWER_LOADED = {
    "ru": "Держи!"
}
