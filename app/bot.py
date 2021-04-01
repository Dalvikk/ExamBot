from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from handlers.admin import Admin
from handlers.album_handler.album_middleware import AlbumMiddleware
from handlers.general import General
from handlers.moderator import Moder
from handlers.start import Start


async def shutdown(d: Dispatcher):
    await d.storage.close()
    await d.storage.wait_closed()


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    dispatcher = Dispatcher(bot, storage=MemoryStorage())
    dispatcher.middleware.setup(LoggingMiddleware())
    dispatcher.middleware.setup(AlbumMiddleware())
    Start(dispatcher).register_handler()
    Admin(dispatcher).register_handler()
    Moder(dispatcher).register_handler()
    General(dispatcher).register_handler()
    executor.start_polling(dispatcher, on_shutdown=shutdown)
