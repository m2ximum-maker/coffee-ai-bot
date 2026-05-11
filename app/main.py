import asyncio

from aiogram import Bot

from config import get_bot_token
from db import init_db
from bot import dp


async def main() -> None:
    bot_token = get_bot_token()
    bot = Bot(token=bot_token)
    
    init_db()
    print("База данных инициализирована")
    print("Бот успешно запущен ☕ Записываем траты на кофе...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
