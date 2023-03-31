import json
import sqlite3
from dataclasses import dataclass

from aiogram import Bot
from environs import Env
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
        self.supportedLocales = ("ru")
        # self.resources: dict[str, Any]

        # NOTE - Default locale is "ru"
        # DEFECT - Get first locale from supported, no hard-code
        self.locale = "ru"

        with open(f"../res/locales/{self.locale}.json", "r", encoding="utf8") as file:
            self.resources = json.load(file)

        # DB init
        with sqlite3.connect(df.DB_PATH) as dbConnect:
            cursor = dbConnect.cursor()
            cursor.execute(df.DB_SCHEMA_MESSAGES)


# Global obj
botConfig: BotConfig = BotConfig()

# TODO - ugly
env = Env()
env.read_env()

bot: Bot = Bot(env("BOT_TOKEN"), parse_mode="HTML")
