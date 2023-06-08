from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo


def review_inline_keyboard() -> InlineKeyboardMarkup:
    inline = InlineKeyboardBuilder()
    inline.add(InlineKeyboardButton(
        text='Оставить отзыв', web_app=WebAppInfo(url='https://fedor.su/index')))
    inline.adjust()
    return inline.as_markup()


def me_inlines() -> InlineKeyboardMarkup:
    inline = InlineKeyboardBuilder()
    inline.button(text='Изменить никнейм',
                  callback_data=f"changeNick")
    inline.adjust()
    return inline.as_markup()
