from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from caching.redis_client import RedisClient
from config import TOKEN
from views import CourseTgView


bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher()


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


if __name__ == '__main__':
    dp.run_polling(bot)
