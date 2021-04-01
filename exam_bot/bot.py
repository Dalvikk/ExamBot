import asyncio

from aiogram import Bot
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import exam_bot.config
import exam_bot.handlers.admin
import exam_bot.handlers.general
import exam_bot.handlers.moderator
import exam_bot.handlers.start
from handlers.album_handler.album_middleware import AlbumMiddleware

bot = Bot(token=exam_bot.config.TOKEN)
storage = MongoStorage(host=exam_bot.config.HOST, port=exam_bot.config.PORT, db_name=exam_bot.config.DB_NAME)
dispatcher = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()
db = loop.run_until_complete(storage.get_db())[exam_bot.config.DB_NAME]
res = loop.run_until_complete(db.find_one({'name': 'moderators'}))
if res is None:
    loop.run_until_complete(db.insert_one({'name': 'moderators', 'moderators': []}))


async def shutdown(d: Dispatcher):
    await d.storage.close()
    await d.storage.wait_closed()


if __name__ == '__main__':
    if exam_bot.config.PATH.endswith("/"):
        exam_bot.config.PATH = exam_bot.config.PATH[:-1]
    dispatcher.middleware.setup(LoggingMiddleware())
    dispatcher.middleware.setup(AlbumMiddleware())
    exam_bot.handlers.start.Start(dispatcher).register_handler()
    exam_bot.handlers.general.General(dispatcher).register_handler()
    exam_bot.handlers.admin.Admin(dispatcher).register_handler()
    exam_bot.handlers.moderator.Moder(dispatcher).register_handler()
    executor.start_polling(dispatcher, on_shutdown=shutdown)
