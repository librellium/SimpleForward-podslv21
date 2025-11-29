import asyncio
import logging

from aiogram import Bot, Dispatcher

from simpleforward.bot import MessageManager, build
from simpleforward.config import Config

from . import paths


async def main():
    config = Config.load(paths.CONFIG_FILE)

    message_manager = MessageManager()

    logging.basicConfig(format=config.logging.fmt,
                        datefmt=config.logging.date_fmt,
                        level=config.logging.level)

    bot = Bot(token=config.bot.token.get_secret_value())
    dispatcher = Dispatcher()

    dispatcher.include_router(build(config.forwarding,
                                    message_manager))

    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())