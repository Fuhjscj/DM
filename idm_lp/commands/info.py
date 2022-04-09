import os

import requests
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp import const
from idm_lp.const import __version__, __author__
from idm_lp.logger import logger_decorator
from idm_lp.database import Database
from idm_lp.utils import edit_message, SemVer

user = Blueprint(
    name='info_blueprint'
)


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> инфо")
@logger_decorator
async def info_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    version_rest = requests.get(const.VERSION_REST).json()

    last_stable = SemVer(version_rest['version'])
    current = SemVer(const.__version__)

    if current < last_stable:
        update_text = (
            f"\n\nДоступно обновление {version_rest['version']}\n"
            f"{version_rest['description']}\n"
            f"{const.GITHUB_LINK}"
        )
        if 'DYNO' in os.environ:
            update_text += (
                "\n\nЧтобы обновить введите !с обновитьлп"
            )
    elif current > last_stable:
        update_text = (
            "\n\n⚠ Обратите внимание! Вы используете экспериментальную не стабильную версию.\n"
            f"Текущая стабильная: {version_rest['version']}"
        )
    else:
        update_text = ""

    text = f"""
    ❤ DML LP 🤤 v{__version__} by {__author__}

    🔴 Ключ рукаптчи: {"&#9989;" if db.ru_captcha_key else "&#10060;"}
    🔴 Удаление уведомлений: {"&#9989;" if db.delete_all_notify else "&#10060;"}
    🔴 Выключение уведомлений: {"&#9989;" if db.disable_notifications else "&#10060;"}

    🟠 В игноре: {len(db.ignored_members)}
    🟠 В глобальном игноре: {len(db.ignored_global_members)}
    🟠 В муте: {len(db.muted_members)}
    🟠 Довов: {len(db.trusted)}
    🟠 Алиасов: {len(db.aliases)}
    🟠 Шаблонов для удаления: {len(db.regex_deleter)}
    🟠 РП-команд: {len(db.role_play_commands)}

    🟡 Выходить из бесед: {"&#9989;" if db.auto_exit_from_chat else "&#10060;"}
    🟡 Удалять диалог: {"&#9989;" if db.auto_exit_from_chat_delete_chat else "&#10060;"}
    🟡 Добавлять пригласившего в ЧС: {"&#9989;" if db.auto_exit_from_chat_add_to_black_list else "&#10060;"}
    
    🟢 Повторялка: {"&#9989;" if db.repeater_active else "&#10060;"}
    🟢 Повторялка | Триггер: {db.repeater_word}

    🔵 Заражение в ответ: {"&#9989;" if db.bio_reply else "&#10060;"}
    
    💠 NoMeta: {"&#9989;" if db.nometa_enable else "&#10060;"}
    💠 NoMeta | Количество секунд: {db.nometa_delay}
    💠 NoMeta | Сообщение: <<{db.nometa_message}>>
    💠 NoMeta | Вложения: {len(db.nometa_attachments)}
        
    🟣 Префикс ДД: {db.dd_prefix}
    🟣 Сервисные префиксы: {' '.join(db.service_prefixes)}
    🟣 Свои префиксы: {' '.join(db.self_prefixes) if db.self_prefixes else ''}
    🟣 Префиксы дежурного: {' '.join(db.duty_prefixes) if db.duty_prefixes else ''}{update_text}
    """.replace('    ', '')
    await edit_message(
        message,
        text
    )
