import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

from common import register_handlers_common
from quotes import register_handlers_quotes

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="/quotes", description="Избранные цитаты через заданное время"
        ),
        BotCommand(
            command="/cancel", description="Отменить отправку цитат через заданное время"
        ),
        BotCommand(command="/now", description="Цитата сейчас"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_quotes(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
