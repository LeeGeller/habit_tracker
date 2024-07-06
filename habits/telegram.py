from aiogram import Bot, Dispatcher, types, Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State

from config.settings import BOT_TOKEN, BOT_SERVER

session = AiohttpSession(
    api=TelegramAPIServer.from_base(BOT_SERVER)
)
bot = Bot(BOT_TOKEN, session=session)
dp = Dispatcher()
router = Router()


class Form(StatesGroup):
    username = State()
    password = State()


@dp.message(Command('start'))
async def send_welcome_message(message: types.Message):
    await message.answer(f"Hi, {message.from_user.full_name}! I'm your habit-bot.")


@router.message(Form.username)
async def remind_about_habit(habit_list):
    for habit in habit_list:
        await bot.send_message(habit.owner, f"I will {habit.action} at {habit.time_to_complete} in {habit.place}")


dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
