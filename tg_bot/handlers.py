from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from tg_bot.keys import review_inline_keyboard, me_inlines
from tg_bot.utils import level, points_naming
import db


class FSM(StatesGroup):
    changeNick = State()


async def setup_commands(bot: Bot):
    bot_commands = [
        BotCommand(command='start', description='Старт'),
        BotCommand(command='review', description='Оставить отзыв'),
        BotCommand(command='cancel', description='Отмена'),
        BotCommand(command='me', description='Мой профиль'),
        BotCommand(command='rating', description='Топ 10 пользователей')
    ]
    await bot.set_my_commands(bot_commands)


async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.reply('OK')


async def start_command(message: Message):
    user = message.from_user
    username = db.add_user(user.id, user.username)
    if not username:
        username = user.username
    await message.answer(f"Здравствуйте!\n...\nВаш текущий ник: {username}\n...",
                         reply_markup=me_inlines())


async def me_command(message: Message):
    data = db.get_user(message.from_user.id)
    level_ = level(data['points'])
    await message.answer(f"Ваш ник: {data['nickname']}\nВаш уровень: {level_[0]}\nВаши балы: {data['points']}/{level_[1]}",
                         reply_markup=me_inlines())


async def rating_command(message: Message):
    rating = db.get_rating(message.from_user.id)
    rating_str = 'Топ 10 пользователей:\n'
    for i in rating[:-1]:
        rating_str += f"#{i['pos']} {i['nickname']}, {level(i['points'])[0]} уровень, {i['points']} {points_naming(i['points'])}\n"
    rating_str += f"Вы:\n#{rating[-1]['pos']} {rating[-1]['nickname']}, {level(rating[-1]['points'])[0]} уровень, {rating[-1]['points']} {points_naming(rating[-1]['points'])}"
    await message.answer(rating_str)


async def inlines_handler(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    match data[0]:
        case 'changeNick':
            await call.message.answer('Введите новый ник')
            await state.set_state(FSM.changeNick)
            await call.answer()


async def change_nick(message: Message, state: FSMContext):
    db.change_nickname(message.from_user.id, message.text)
    await message.answer(f"Готово, новый ник:\n{message.text}")
    await state.clear()


async def review_command(message: Message):
    await message.answer("Оставьте отзыв, нажмите на кнопку ниже", reply_markup=review_inline_keyboard())


def register_handlers(dp: Dispatcher):
    dp.message.register(cancel_command, Command(commands='cancel'))
    dp.callback_query.register(inlines_handler)
    dp.message.register(change_nick, FSM.changeNick)
    dp.message.register(review_command, Command(commands='review'))
    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(me_command, Command(commands='me'))
    dp.message.register(rating_command, Command(commands='rating'))
