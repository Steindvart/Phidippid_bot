import logging
import sqlite3
import asyncio

from aiogram import types, exceptions
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.fsm.context import FSMContext

# DEFECT - using global objects, not good
from bot import bot, botConfig
from states import BotStatesGroup
import utils
import default_val as df

# Alliaces
res = botConfig.resources

# Keyboards
btn_cancel: KeyboardButton = KeyboardButton(text='Отмена')
keyboard_cancel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btn_cancel]])


async def start(message: types.Message) -> None:
    logging.info(utils.get_log_str("start", message.from_user))

    text = res["start"] + "\n\n" + "\n".join(res["mainCommands"].values())
    await message.answer(text)


async def cancel(message: types.Message, state: FSMContext) -> None:
    logging.info(utils.get_log_str("cancel", message.from_user))
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(text='Состояние сброшено', reply_markup=ReplyKeyboardRemove())


async def about(message: types.Message) -> None:
    logging.info(utils.get_log_str("about", message.from_user))

    await message.answer(res["about"])


async def send_message_to_recipient(from_chat: types.message, recipient_id, text):
    # TODO - make better link format, recipient.mention_html() - DON'T WORK!
    link = types.User(id=recipient_id, first_name=str(recipient_id), is_bot=False).url
    try:
        await bot.send_message(chat_id=recipient_id, text=text)
        await from_chat.answer(text=f'✅ Успех: сообщение отправлено получателю {link}.')
    except exceptions.TelegramForbiddenError:
        await from_chat.answer(text=f'❌ Неудача: получатель {link} не активировал или заблокировал бота.')
    except exceptions.TelegramNotFound:
        await from_chat.answer(text=f'❌ Неудача: получатель {link} не существует.')
    except exceptions.TelegramRetryAfter as e:
        # TODO - message about retry
        await asyncio.sleep(e.retry_after)
        await bot.send_message(chat_id=recipient_id, text=text)
    except exceptions.TelegramAPIError:
        await from_chat.answer(text=f'❌ Неудача: сообщение для получателя {link} не доставлено.')


async def send_messages(message: types.Message, state: FSMContext) -> None:
    logging.info(utils.get_log_str("send_messages", message.from_user))

    with sqlite3.connect(df.DB_PATH) as conn:
        cursor = conn.cursor()
        user_id = message.from_user.id
        cursor.execute(f'SELECT to_id, text FROM messages WHERE from_id = {user_id}')
        for (recipient_id, text) in cursor.fetchall():
            await send_message_to_recipient(message, recipient_id, text)


async def set_message(message: types.Message, state: FSMContext) -> None:
    logging.info(utils.get_log_str("set_message", message.from_user))

    await state.set_state(BotStatesGroup.message)
    await message.answer(text='Введите сообщение, которое вы хотите отправить.', reply_markup=keyboard_cancel)


async def proc_message(message: types.Message, state: FSMContext) -> None:
    logging.info(utils.get_log_str("proc_message", message.from_user))

    await state.set_data({'text': message.text})

    await state.set_state(BotStatesGroup.recipient)
    await message.answer(text='Введите user id получателя сообщения.', reply_markup=keyboard_cancel)


async def proc_reсipient(message: types.Message, state: FSMContext) -> None:
    logging.info(utils.get_log_str("proc_reсipient", message.from_user))

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
    await message.answer(text="✅ Сообщение добавлено", reply_markup=ReplyKeyboardRemove())
