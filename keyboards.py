from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import endpoints

async def authorize(tg_id):
    auth_link = endpoints.get_auth_link(tg_id)
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="🔗 Авторизоваться в Spotify", url=auth_link))
    return kb.as_markup()


async def start():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Top Artists", callback_data="artists"))
    kb.add(InlineKeyboardButton(text="Top Tracks", callback_data="tracks"))
    return kb.adjust(1).as_markup()


cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True,
    one_time_keyboard=True
)