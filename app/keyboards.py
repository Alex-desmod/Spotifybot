from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import app.endpoints

async def authorize(tg_id):
    auth_link = app.endpoints.get_auth_link(tg_id)
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="🔗 Авторизоваться в Spotify", url=auth_link))
    return kb.as_markup()

# async def start():
#     kb = InlineKeyboardBuilder()
    # for sport in sports.Sports:
    #     kb.add(InlineKeyboardButton(text=sport.value, callback_data=sport.name))

    # return kb.adjust(1).as_markup()


cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True,
    one_time_keyboard=True
)