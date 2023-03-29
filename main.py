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
storage: MemoryStorage = MemoryStorage()

botConfig: config.BotConfig = config.BotConfig()
bot: Bot = Bot(botConfig.token, parse_mode="HTML")

# Main
if __name__ == '__main__':
    dp: Dispatcher = Dispatcher()

    # Commands
    # TODO - move it to separate block
    dp.message.register(cmd.start, Command(commands=['start']))
    dp.message.register(cmd.cancel, Text(text=['Отмена'], ignore_case=True))
    dp.message.register(cmd.set_messages, Command(commands=['setMessages']))
    dp.message.register(cmd.set_message, StateFilter(BotStatesGroup.messages))

    dp.run_polling(bot)
