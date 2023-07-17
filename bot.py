from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fastapi import FastAPI

from caching.redis_client import RedisClient
from config import TOKEN, WEB_SERVICE_URL
from views import CourseTgView
from parsing.async_parsing import async_get_programs

WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_URL = WEB_SERVICE_URL + WEBHOOK_PATH

bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher()

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)


@app.get("/update_cache")
async def bot_webhook():
    programs = await async_get_programs()
    async with RedisClient() as cache:
        await cache.set_programs(programs)
    return {"status": "ok"}


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer("""Привет! 
/programs - получить информацию о программах в СИТУ
    """)


@dp.message(Command(commands=['programs']))
async def process_help_command(message: Message):
    async with RedisClient() as cache:
        programs = await cache.get_program_names_and_hash()
    kb = [
        [InlineKeyboardButton(text=name, callback_data="hash" + hash_)] for (name, hash_) in programs
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Программы в СИТУ:", reply_markup=keyboard)


@dp.callback_query(Text(startswith="hash"))
async def send_random_value(callback: CallbackQuery):
    _, program_hash = callback.data.split("hash")
    async with RedisClient() as cache:
        p = await cache.get_program_by_hash(program_hash)
    n_courses = len(p.courses)
    await callback.answer(
        text=f"Найдено {n_courses} курс{'' if n_courses == 1 else ('а' if 1 < n_courses < 5 else 'ов')}"
    )
    if n_courses > 0:
        await callback.message.answer("☀️☀️☀️☀️☀️☀️☀️☀️☀️")
    for course in p.courses:
        await callback.message.answer(str(CourseTgView(course)))
