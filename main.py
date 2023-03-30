import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage

import config
import commands as cmd
from states import BotStatesGroup


# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s - %(message)s')

# Global obj
botConfig: config.BotConfig = config.BotConfig()
bot: Bot = Bot(botConfig.token, parse_mode="HTML")

# Main
if __name__ == '__main__':
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    # Commands
    # TODO - move it to separate block
    dp.message.register(cmd.start, Command(commands=['start']))
    dp.message.register(cmd.cancel, Text(text=['Отмена'], ignore_case=True))
    dp.message.register(cmd.send_messages, Command(commands=['send']))
    dp.message.register(cmd.set_message, Command(commands=['setMessage']))
    dp.message.register(cmd.proc_message, StateFilter(BotStatesGroup.message))
    dp.message.register(cmd.proc_reсipient, StateFilter(BotStatesGroup.recipient))

    dp.run_polling(bot)
