from aiogram import Bot, Dispatcher, types, Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.filters import Command, CommandStart

from config.settings import BOT_TOKEN, BOT_SERVER
from users.models import User

session = AiohttpSession(api=TelegramAPIServer.from_base(BOT_SERVER))
bot = Bot(BOT_TOKEN, session=session)
dp = Dispatcher()
router = Router()


@dp.message(CommandStart())
async def send_welcome_message(message: types.Message):
    await message.answer(f"Hi, {message.from_user.full_name}! I'm your habit-bot.")


@router.message()
async def remind_about_habit(user_id, habit):
    await bot.send_message(
        user_id,
        f"I will {habit.action} at {habit.time_to_complete} in {habit.place}",
    )


dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
