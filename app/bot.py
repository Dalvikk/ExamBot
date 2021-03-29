import asyncio

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from app.handlers.start_handler import StartHandler
from config import TOKEN


async def shutdown(d: Dispatcher):
    await d.storage.close()
    await d.storage.wait_closed()


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    dispatcher = Dispatcher(bot, storage=MemoryStorage())
    dispatcher.middleware.setup(LoggingMiddleware())
    StartHandler(dispatcher).register_handler()
    executor.start_polling(dispatcher, on_shutdown=shutdown)
