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
                                    resize_keyboard=True, keyboard=[[btn_cancel]])


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


async def set_message(message: types.Message, state: FSMContext) -> None:
    logging.info(config.get_log_str("set_message", message.from_user))

    await state.set_state(BotStatesGroup.message)
    await message.answer(text='Введите сообщение, которое вы хотите отправить.', reply_markup=keyboard_cancel)


async def proc_message(message: types.Message, state: FSMContext) -> None:
    logging.info(config.get_log_str("proc_message", message.from_user))

    await state.set_data({'text': message.text})

    await state.set_state(BotStatesGroup.recipient)
    await message.answer(text='Введите user id получателя сообщения.', reply_markup=keyboard_cancel)


async def proc_reсipient(message: types.Message, state: FSMContext) -> None:
    logging.info(config.get_log_str("proc_reсipient", message.from_user))

    await state.update_data({'recipient': message.text})
    data = await state.get_data()

    with sqlite3.connect(df.DB_PATH) as conn:
        from_id = message.from_user.id
        to_id = data['recipient']
        text = data['text']

        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (from_id, to_id, text) VALUES (?, ?, ?)',
                       (from_id, to_id, text))

        conn.commit()

    await state.clear()
