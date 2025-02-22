import json
import logging
from email.policy import default

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

import keyboards as kb
import db.requests as rq


router = Router(name=__name__)

logger = logging.getLogger(__name__)

with open("messages.json", "r", encoding="utf-8") as file:
    messages = json.load(file)


#Defining the state for feedback
class FeedbackState(StatesGroup):
    waiting_for_feedback = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.first_name)
    access_token = await rq.get_valid_access_token(message.from_user.id)
    if not access_token:
        await message.answer(f'Привет, {message.from_user.first_name} 😊\n{messages[0]["start"]}',
                         reply_markup=await kb.authorize(message.from_user.id))
    else:
        await message.answer("Твои топы",
                             reply_markup=await kb.start())


@router.callback_query(F.data == "artists")
async def artists(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Топ по группам и исполнителям. Выбери временной интервал.",
                                  reply_markup=await kb.times(callback.data))


@router.callback_query(F.data == "tracks")
async def tracks(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Топ треков. Выбери временной интервал.",
                                  reply_markup=await kb.times(callback.data))


@router.callback_query(F.data.endswith("_term"))
async def numbers(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Выбери количество",
                                  reply_markup=await kb.limits(callback.data))


@router.callback_query(F.data.endswith(".10")|F.data.endswith(".20")|F.data.endswith(".50"))
async def charts(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Здесь будут чарты",
                                  reply_markup=await kb.start())



@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Long live rock-n-roll",
                                  reply_markup=await kb.start())


@router.message(Command("feedback"))
async def ask_feedback(message: Message, state: FSMContext):
    await message.answer(messages[0]["feedback"],
                         reply_markup=kb.cancel_kb
                         )
    await state.set_state(FeedbackState.waiting_for_feedback)


@router.message(FeedbackState.waiting_for_feedback, F.text != "❌ Отмена")
async def forward_feedback(message: Message, bot: Bot, state: FSMContext):
    admins = await rq.get_admins()

    for admin in admins:
        logger.info(admin.tg_id)
        await bot.send_message(
            admin.tg_id,
            f"📩 Новое сообщение от @{message.from_user.username or message.from_user.id}:\n\n{message.text}"
        )
    await message.answer(messages[0]["send"], reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(FeedbackState.waiting_for_feedback, F.text == "❌ Отмена")
async def cancel_feedback(message: Message, state: FSMContext):
    await message.answer(messages[0]["canceled"], reply_markup=ReplyKeyboardRemove())
    await state.clear()


# @router.message()
# async def catch_all_messages(message: Message):
#     await message.answer(messages[0]["sorry"],
#                          reply_markup=await kb.start())