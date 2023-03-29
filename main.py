import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text

import config
import commands as cmd


# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s - %(message)s')

# Global obj
botConfig: config.BotConfig = config.BotConfig()
bot: Bot = Bot(botConfig.token, parse_mode="HTML")


# Main
if __name__ == '__main__':
    dp: Dispatcher = Dispatcher()

    # Commands
    # TODO - move it to separate block
    dp.message.register(cmd.send_welcome, Command(commands=['start', 'help']))

    dp.run_polling(bot)
