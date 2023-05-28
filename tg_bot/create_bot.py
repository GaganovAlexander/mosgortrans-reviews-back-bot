from aiogram import Bot, Dispatcher

from configs import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()
