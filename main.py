import logging
import sys
import random
import asyncio
import time
import threading
from typing import NamedTuple, List, TypeAlias, Tuple, Mapping
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
import pytz
import yaml
from internal.developer.delivery.developer_delivery import developer_delivery
from internal.developer.repository.developer_repository import developer_repository
from internal.developer.usecase.developer_usecase import developer_usecase
from internal.merge_request.delivery.merge_request_delivery import (
    merge_request_delivery,
)
from internal.merge_request.repository.merge_request_repository import (
    merge_request_repository,
)
from internal.merge_request.usecase.merge_request_usecase import merge_request_usecase
from jinja2 import Template
import schedule
from internal.utilities.config import Config

Config("config.yml")
TOKEN = Config().get("telegram_token")
dispatcher = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
bot_command: TypeAlias = Mapping[str, callable]


@dispatcher.message()
async def reply(message: types.Message):
    commands: dict = {}
    merge_request_handler = merge_request_delivery(
        usecase=merge_request_usecase(
            mr_repo=merge_request_repository(), dev_repo=developer_repository()
        )
    )
    developer_handler = developer_delivery(
        usecase=developer_usecase(repository=developer_repository())
    )
    commands = merge_request_handler.setup(commands, message=message)
    commands = developer_handler.setup(commands, message=message)
    try:
        if message.text in commands.keys():
            await commands[message.text]
        elif not message.text.startswith("/"):
            pass
        else:
            await message.answer(f"Command {message.text} wasnt found")
    except Exception as e:
        logging.log(level=logging.ERROR, msg=f"Error {type(e)} occured")
        await message.answer("Error occured")
    finally:
        pass


def read_config(filename):
    with open(filename, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data


async def daily_alert_async():
    chat_id = Config().get("developer_chat_id")
    await bot.send_message(chat_id, "Дейли")


def daily_alert():
    asyncio.create_task(daily_alert_async())


async def check_alert_async():
    chat_id = Config().get("developer_chat_id")
    merge_request_handler = merge_request_delivery(
        usecase=merge_request_usecase(
            mr_repo=merge_request_repository(), dev_repo=developer_repository()
        )
    )
    await merge_request_handler.handle_check_schedule(bot=bot, chat_id=chat_id)


def check_alert():
    asyncio.create_task(check_alert_async())


def create_schedule_events(config):
    msk_timezone = pytz.timezone(config["schedule"]["TIMEZONE"])

    for time_str in config["schedule"]["check"]["time"]:
        for weekday in config["schedule"]["check"]["every"]:
            getattr(schedule.every(), weekday).at(time_str).do(
                check_alert
            ).timezone = msk_timezone

    for time_str in config["schedule"]["daily"]["time"]:
        for weekday in config["schedule"]["daily"]["every"]:
            getattr(schedule.every(), weekday).at(time_str).do(
                daily_alert
            ).timezone = msk_timezone


async def bot_main() -> None:
    await dispatcher.start_polling(bot)


async def main():
    config = read_config("config.yml")
    create_schedule_events(config=config)
    schedule_task = asyncio.create_task(schedule_dispatcher())
    bot_main_task = asyncio.create_task(bot_main())
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await asyncio.gather(schedule_task, bot_main_task)


async def schedule_dispatcher():
    try:
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logging.log(logging.INFO, msg="Stopped schedule")


if __name__ == "__main__":
    asyncio.run(main())
