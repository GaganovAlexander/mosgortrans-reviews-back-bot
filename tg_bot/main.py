from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from tg_bot import bot, dp
from tg_bot.handlers import register_handlers, setup_commands
from configs import STANDART_URL



async def on_startup():
    await bot.set_webhook(f'{STANDART_URL}/bot/mosgortrans', drop_pending_updates=True)
    await setup_commands(bot)
    print('Бот запущен')

async def on_shutdown():
    await bot.delete_webhook(drop_pending_updates=True)


def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp['base_url'] = STANDART_URL

    register_handlers(dp)

    app = Application()
    app["bot"] = bot

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path="/bot/mosgortrans")
    setup_application(app, dp, bot=bot)

    run_app(app, host="127.0.0.1", port=8002)


if __name__ == "__main__":
    main()