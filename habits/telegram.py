from aiogram import Bot, Dispatcher, types, Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.filters import Command, CommandStart

from config.settings import BOT_TOKEN, BOT_SERVER

session = AiohttpSession(api=TelegramAPIServer.from_base(BOT_SERVER))
bot = Bot(BOT_TOKEN, session=session)
dp = Dispatcher()
router = Router()


@dp.message(CommandStart())
async def send_welcome_message(message: types.Message):
    print(message)
    await message.answer(f"Hi, {message.from_user.full_name}! I'm your habit-bot.")


@router.message()
async def remind_about_habit(habit_dict):

    for user_id, habits in habit_dict.items():
        await bot.send_message(
            user_id,
            f"I will {habits.action} at {habits.time_to_complete} in {habits.place}",
        )


dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
