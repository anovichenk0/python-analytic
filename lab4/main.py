import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

stats = {}

choice_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Камень", callback_data="rock"),
        InlineKeyboardButton(text="Ножницы", callback_data="scissors"),
        InlineKeyboardButton(text="Бумага", callback_data="paper")
    ]
])

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот для игры в 'Камень, ножницы, бумага'.\n"
                         "Команды:\n/play — начать игру\n/stats — ваша статистика")

@dp.message(Command("play"))
async def play_handler(message: types.Message):
    await message.answer("Сделайте свой выбор:", reply_markup=choice_kb)

@dp.message(Command("stats"))
async def stats_handler(message: types.Message):
    user_id = message.from_user.id
    user_stats = stats.get(user_id, {"wins": 0, "losses": 0, "draws": 0})
    await message.answer(f"Ваша статистика:\n"
                         f"Побед: {user_stats['wins']}\n"
                         f"Поражений: {user_stats['losses']}\n"
                         f"Ничьих: {user_stats['draws']}")

@dp.callback_query(F.data.in_({"rock", "scissors", "paper"}))
async def callback_handler(callback: types.CallbackQuery):
    user_choice = callback.data
    bot_choice = random.choice(["rock", "scissors", "paper"])
    result = get_result(user_choice, bot_choice)

    user_id = callback.from_user.id
    stats.setdefault(user_id, {"wins": 0, "losses": 0, "draws": 0})
    if result == "win":
        stats[user_id]["wins"] += 1
        msg = "Вы выиграли! 🎉"
    elif result == "lose":
        stats[user_id]["losses"] += 1
        msg = "Вы проиграли. 😢"
    else:
        stats[user_id]["draws"] += 1
        msg = "Ничья. 🤝"

    await callback.message.answer(
        f"Вы: {translate(user_choice)}\nБот: {translate(bot_choice)}\n{msg}"
    )
    await callback.answer()

def get_result(player, bot):
    if player == bot:
        return "draw"
    elif (player == "rock" and bot == "scissors") or \
         (player == "scissors" and bot == "paper") or \
         (player == "paper" and bot == "rock"):
        return "win"
    else:
        return "lose"

def translate(choice):
    return {"rock": "Камень", "scissors": "Ножницы", "paper": "Бумага"}[choice]

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
