from aiogram import Dispatcher
from aiogram.filters import Command, Text, StateFilter

import commands as cmd
from states import BotStatesGroup


def register_commands(dp: Dispatcher) -> None:
    dp.message.register(cmd.start, Command(commands=['start']))
    dp.message.register(cmd.cancel, Command(commands=['cancel']))
    dp.message.register(cmd.cancel, Text(text=['Отмена'], ignore_case=True))
    dp.message.register(cmd.send_messages, Command(commands=['send']))
    dp.message.register(cmd.set_message, Command(commands=['setMessage'], ignore_case=True))
    dp.message.register(cmd.about, Command(commands=['about']))


def register_processors(dp: Dispatcher) -> None:
    dp.message.register(cmd.proc_message, StateFilter(BotStatesGroup.message))
    dp.message.register(cmd.proc_reсipient, StateFilter(BotStatesGroup.recipient))
