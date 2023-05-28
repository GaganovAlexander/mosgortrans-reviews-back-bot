from asyncio import run as arun

from tg_bot.create_bot import bot, dp
from tg_bot.handlers import register_handlers, setup_commands


async def start():
    print('Бот запущен')
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_commands(bot)


async def main():
    dp.startup.register(start)

    register_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
