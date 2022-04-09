import json

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

__version__ = '1.2'
__author__ = 'Dimka Hopi'
__description__ = (
    "LP модуль позволяет работать приемнику сигналов «IDM» работать в любых чатах."
)

CONFIG_PATH = "config.json"
USE_APP_DATA = False
USE_LOCAL_DB = False


LOGGER_LEVEL = 'INFO'
LOG_TO_PATH = False

BASE_DOMAIN = "https://idmduty.ru"

GITHUB_LINK = "https://github.com/Fuhjscj/DM"
VERSION_REST = "https://raw.githubusercontent.com/Fuhjscj/DM/master/rest/version.json"
ALIASES_REST = "https://raw.githubusercontent.com/Fuhjscj/DM/master/rest/aliases.json"
ROLE_PLAY_COMMANDS_REST = "https://raw.githubusercontent.com/Fuhjscj/Yt/master/rest/role_play_commands.json"

ENABLE_EVAL = False

try:
    with open('lp_dc_config.json', 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
        APP_ID = data.get('app_id', 0)
        APP_SECRET = data.get('app_secret', "public")
except FileNotFoundError:
    APP_ID = 0
    APP_SECRET = "public"

APP_USER_AGENT = f"IDMLP({APP_ID};{APP_SECRET})"

scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))
