import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from dotenv import load_dotenv

from db import init_db
from formatting import format_expense_item
from parsing import (
    get_add_error_message,
    get_delete_error_message,
    parse_add_command,
    parse_amount,
    parse_delete_command,
)
from services import (
    create_expense,
    delete_user_expense,
    get_user_expenses,
    get_user_total_expenses,
)

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("BOT_TOKEN не найден в .env")

dp = Dispatcher()


class AddExpense(StatesGroup):
    waiting_for_amount = State()
    waiting_for_drink = State()
    waiting_for_coffee_shop = State()


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    username = message.from_user.username if message.from_user else None
    who = f"@{username}" if username else "(username в профиле не задан)"
    await message.answer(
        f"Привет, {who}! Я бот для учета трат на кофе ☕\n"
        "Добавить трату: /add 250 капучино\n"
        "Удалить трату: /delete 3\n"
        "Итог: /result\n"
        "Список трат: /list",
    )


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Сейчас нечего отменять")
        return

    await state.clear()
    await message.answer("Добавление отменено")


@dp.message(AddExpense.waiting_for_amount)
async def process_add_amount(message: Message, state: FSMContext) -> None:
    try:
        amount = parse_amount(message.text or "")
    except ValueError:
        await message.answer("Введи сумму числом больше нуля, например: 250")
        return

    await state.update_data(amount=amount)
    await state.set_state(AddExpense.waiting_for_drink)
    await message.answer("Что пил? Например: капучино")


@dp.message(AddExpense.waiting_for_drink)
async def process_add_drink(message: Message, state: FSMContext) -> None:
    drink = (message.text or "").strip()

    if not drink:
        await message.answer("Введи название напитка, например: капучино")
        return

    await state.update_data(drink=drink)
    await state.set_state(AddExpense.waiting_for_coffee_shop)
    await message.answer("Где купил? Если не хочешь указывать, отправь -")


@dp.message(AddExpense.waiting_for_coffee_shop)
async def process_add_coffee_shop(message: Message, state: FSMContext) -> None:
    if not message.from_user:
        await message.answer("Не удалось определить пользователя.")
        return

    coffee_shop_raw = (message.text or "").strip()
    coffee_shop = None if coffee_shop_raw == "-" else coffee_shop_raw

    data = await state.get_data()
    amount = data["amount"]
    drink = data["drink"]

    create_expense(
        user_id=message.from_user.id,
        amount=amount,
        drink=drink,
        coffee_shop=coffee_shop,
    )

    await state.clear()

    shop_text = f" ({coffee_shop})" if coffee_shop else ""
    await message.answer(f"☕ Записал: {amount} ₽ — {drink}{shop_text}")


@dp.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext) -> None:
    if not message.from_user:
        await message.answer("Не удалось определить пользователя.")
        return

    if (message.text or "").strip() == "/add":
        await state.set_state(AddExpense.waiting_for_amount)
        await message.answer("Введи сумму траты, например: 250")
        return

    try:
        amount, drink, coffee_shop = parse_add_command(message.text or "")
    except ValueError as error:
        await message.answer(get_add_error_message(error))
        return

    uid = message.from_user.id

    create_expense(
        user_id=uid,
        amount=amount,
        drink=drink,
        coffee_shop=coffee_shop,
    )

    shop_text = f" ({coffee_shop})" if coffee_shop else ""

    await message.answer(
        f"☕ Записал: {amount} ₽ — {drink}{shop_text}"
    )


@dp.message(Command("delete"))
async def cmd_delete(message: Message) -> None:
    if not message.from_user:
        await message.answer("Не удалось определить пользователя.")
        return

    try:
        expense_id = parse_delete_command(message.text or "")
    except ValueError as error:
        await message.answer(get_delete_error_message(error))
        return

    deleted = delete_user_expense(
        user_id=message.from_user.id,
        expense_id=expense_id,
    )

    if not deleted:
        await message.answer(f"Не нашел трату #{expense_id}")
        return

    await message.answer(f"Удалил трату #{expense_id}")


@dp.message(Command("result"))
async def cmd_result(message: Message) -> None:
    if not message.from_user:
        await message.answer("Не удалось определить пользователя.")
        return

    uid = message.from_user.id

    total = get_user_total_expenses(uid)

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
    expenses = get_user_expenses(uid)

    if not expenses:
        await message.answer("Пока нет трат ☕")
        return

    lines = []

    for expense in expenses:
        lines.append(format_expense_item(expense))

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
