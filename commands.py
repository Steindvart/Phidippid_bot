import logging
import sqlite3
from datetime import datetime

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext

# DEFECT - using global objects, not good
from main import botConfig
from states import BotStatesGroup
import config
import default_val as df

# Alliaces
res = botConfig.resources

# Keyboards
btn_cancel: KeyboardButton = KeyboardButton(text='Отмена')
keyboard_cancel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[btn_cancel]])

async def start(message: types.Message) -> None:
    logging.info(config.get_log_str("start", message.from_user))

    await message.answer(res["start"])

    allCommands = "\n".join(res["mainCommands"].values())
    await message.answer(allCommands)


async def cancel(message: types.Message, state: FSMContext) -> None:
    logging.info(config.get_log_str("cancel", message.from_user))
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(text='Состояние сброшено', reply_markup=ReplyKeyboardRemove())


async def set_messages(message: types.Message, state: FSMContext) -> None:
    logging.info(config.get_log_str("set_messages", message.from_user))
    await state.set_state(BotStatesGroup.messages)

    await message.answer(text='Включен режим добавления сообщений', reply_markup=keyboard_cancel)

    # TODO - add instructions message
    # await message.answer(res["welcome"])


async def set_message(message: types.Message) -> None:
    logging.info(config.get_log_str("set_message", message.from_user))

    with sqlite3.connect(df.DB_PATH) as conn:
        user_id = message.from_user.id
        text = message.text

        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (user_id, text) VALUES (?, ?)',
                       (user_id, text))

        conn.commit()
