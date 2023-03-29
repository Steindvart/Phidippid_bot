import json, logging
from datetime import datetime

import requests
from aiogram import types
from aiogram.utils import markdown

# DEFECT - using global objects, not good
from main import bot, botConfig
import config
import default_val as df

# Alliaces
res = botConfig.resources


async def send_welcome(message: types.Message) -> None:

    logging.info(config.get_log_str("send_welcome", message.from_user))

    await message.answer(res["welcome"])

    allCommands = "\n".join(res["mainCommands"].values())

    await message.answer(allCommands)
