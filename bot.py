import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from db import init_db, add_expense, get_expenses, get_total_expenses

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("BOT_TOKEN не найден в .env")

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    username = message.from_user.username if message.from_user else None
    who = f"@{username}" if username else "(username в профиле не задан)"
    await message.answer(
        f"Привет, {who}! Я бот для учета трат на кофе ☕\n"
        "Добавить трату: /add 250 капучино\n"
        "Итог: /result\n"
        "Список трат: /list",
    )


def parse_add_command(text: str) -> tuple[int, str, str | None]:
    parts = text.strip().split(maxsplit=3)

    if len(parts) < 2:
        raise ValueError("missing amount")

    amount_raw = parts[1]

    try:
        amount = int(amount_raw)
    except ValueError as error:
        raise ValueError("invalid amount") from error

    if amount <= 0:
        raise ValueError("amount must be positive")

    drink = parts[2].strip() if len(parts) > 2 else "кофе"
    coffee_shop = parts[3].strip() if len(parts) > 3 else None

    return amount, drink, coffee_shop


def get_add_error_message(error: ValueError) -> str:
    error_code = str(error)

    if error_code == "missing amount":
        return "Сумма отсутствует. Пример: /add 250 капучино"

    if error_code == "invalid amount":
        return "Не понял сумму. Пример: /add 250 капучино"

    if error_code == "amount must be positive":
        return "Сумма должна быть больше нуля"

    return (
        "☕ Формат: /add <сумма> [напиток] [кофейня]\n"
        "Пример: /add 250 капучино"
    )


@dp.message(Command("add"))
async def cmd_add(message: Message) -> None:
    if not message.from_user:
        await message.answer("Не удалось определить пользователя.")
        return

    try:
        amount, drink, coffee_shop = parse_add_command(message.text or "")
    except ValueError as error:
        await message.answer(get_add_error_message(error))
        return

    uid = message.from_user.id

    add_expense(
        user_id=uid,
        amount=amount,
        drink=drink,
        coffee_shop=coffee_shop,
    )

    shop_text = f" ({coffee_shop})" if coffee_shop else ""

    await message.answer(
        f"☕ Записал: {amount} ₽ — {drink}{shop_text}"
    )


@dp.message(Command("result"))
async def cmd_result(message: Message) -> None:
    if not message.from_user:
        await message.answer("Не удалось определить пользователя.")
        return

    uid = message.from_user.id

    total = get_total_expenses(uid)

    if total == 0:
        await message.answer("Пока нет трат ☕")
        return

    await message.answer(f"Итого по кофе: {total} ₽ ☕")


@dp.message(Command("list"))
async def cmd_list(message: Message) -> None:
    if not message.from_user:
        await message.answer("Не удалось определить пользователя.")
        return

    uid = message.from_user.id
    expenses = get_expenses(uid)

    if not expenses:
        await message.answer("Пока нет трат ☕")
        return

    lines = []

    for index, (_id, user_id, amount, drink, coffee_shop, created_at) in enumerate(expenses, start=1):
        shop_text = f" — {coffee_shop}" if coffee_shop else ""
        lines.append(f"{index}. {amount} ₽ — {drink}{shop_text}")

    result = "\n".join(lines)

    await message.answer(f"Список трат ☕\n{result}")


async def main() -> None:
    if not bot_token:
        raise ValueError("BOT_TOKEN не найден в .env")

    bot = Bot(token=bot_token)
    print("Бот успешно запущен ☕ Записываем траты на кофе...")
    init_db()
    print("База данных инициализирована")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
