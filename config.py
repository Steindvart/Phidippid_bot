import json
import sqlite3
# from typing import Any
from dataclasses import dataclass

from environs import Env
from aiogram.types import User, Message

import default_val as df

@dataclass
class BotConfig:
    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, newVal):
        if newVal not in self.supportedLocales:
            raise f"{newVal} locale is not supported."
        self._locale = newVal

    # Methods
    def __init__(self) -> None:
        # TODO - find better way to define props
        # Data
        self.state = "main"
        self.supportedLocales = ("ru")
        # self.resources: dict[str, Any]

        # NOTE - Default locale is "ru"
        # DEFECT - Get first locale from supported, no hard-code
        self.locale = "ru"
        env = Env()
        env.read_env()
        self.token: str = env("BOT_TOKEN")

        with open(f"locales/{self.locale}.json", "r", encoding="utf8") as file:
            self.resources = json.load(file)

        # DB init
        with sqlite3.connect(df.DB_PATH) as dbConnect:
            cursor = dbConnect.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_id INTEGER,
                    to_id INTEGER,
                    text TEXT)''')


def get_all_info(botInfo: User, msg: Message) -> dict[str, object]:
    return {
        "bot": json.loads(botInfo.json()),
        "user": json.loads(msg.from_user.json()),
        "chat": json.loads(msg.chat.json())
    }


def get_log_str(source: str, usr: User) -> str:
    return  f"{source} - User_id: {usr.id}, " \
            f"first_name: {usr.first_name}, " \
            f"language_code: {usr.language_code}"
