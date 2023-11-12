import random
import requests
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.exceptions import BadRequest
from Config import *
from LogManager import LogManager
from SoundManager import SoundManager
from Texts import *
from TimeTracker import TimeTracker

# Global variables
timeTracker = TimeTracker()
bot = Bot(token=api_bot_token)
dispatcher = Dispatcher(bot)
log_manager = LogManager()
sound_manager = SoundManager()
bot_is_running = False
approved_data = {}
need_approve_data = {}
bot_commands = {}


# Helpers
def get_dev_telegram_name(users_from_description):
    telegram_names = []
    for user in users_from_description:
        name = user.removeprefix('@')
        if name in developers.keys():
            telegram_names.append(developers[name])
        else:
            telegram_names.append(f'{developers["noSuchUser"]} {user}')

    return telegram_names


def get_not_in_draft_mrs():
    response = requests.get(opened_merge_requests_url, headers=headers).text
    opened_merge_requests = json.loads(response)
    return filter(lambda item: item['draft'] is False, opened_merge_requests)


def clear_data():
    need_approve_data.clear()
    approved_data.clear()


def get_approved_developers(mr):
    iid = str(mr['iid'])
    url = merge_requests_url + iid + '/approvals'
    get_approved_mrs = requests.get(url, headers=headers).text
    approved_mrs_dict = json.loads(get_approved_mrs)
    return approved_mrs_dict['approved_by']


def get_users_from_description(mr):
    users_from_description_str = str(mr['description'])
    users_from_description_with_task = users_from_description_str.split()
    users_from_description_filtered = filter(lambda word: '@' in word, users_from_description_with_task)
    return list(users_from_description_filtered)


def load_mr_data():
    not_in_draft = get_not_in_draft_mrs()

    for mr in not_in_draft:
        approved_developers = get_approved_developers(mr)
        assignee = 'none' if mr['assignee'] is None else str((mr['assignee'])['username'])
        assignee_telegram_name = developers[assignee]
        web_url = str(mr['web_url'])
        discussions_resolved = mr['blocking_discussions_resolved']
        discussions_resolved_str = '' if discussions_resolved is True else "\n💥 Нашла замечания"
        need_send_ready_to_merge_message = len(approved_developers) >= required_approves_count and discussions_resolved
        ready_to_merge = f'\n🐢 Assignee: {assignee_telegram_name}, можно вливать 🚀' if need_send_ready_to_merge_message else ''
        key = web_url + discussions_resolved_str + ready_to_merge
        mr_data = {key: approved_developers}
        users_from_description = get_users_from_description(mr)
        to_telegram_names = get_dev_telegram_name(users_from_description)

        if need_send_ready_to_merge_message:
            to_telegram_names = []
        else:
            try:
                to_telegram_names.append(assignee_telegram_name)
            except BaseException as error:
                if error:
                    to_telegram_names.append(f'{developers["noSuchUser"]} {assignee}')

        need_approve_developers = {key: to_telegram_names}
        need_approve_data.update(need_approve_developers)
        approved_data.update(mr_data)


async def send_daily_notification(message, weekday, time):
    if weekday in daily_schedule.keys() and time == daily_schedule[weekday]:
        sound_manager.notify(text='Пора на дейли')
        daily_notification = '🌚 Дейли'
        await bot.send_message(message.chat.id, daily_notification, disable_web_page_preview=True)


async def send(message: types.Message, needNow: bool = None):
    weekday = timeTracker.get_current_weekday()
    time = timeTracker.get_current_time()
    log_message = f'  State: running\n  Server time: {time}'

    # await send_daily_notification(message, weekday, time)

    if weekday in work_days and time in schedule or needNow:
        load_mr_data()
        common_message = ''

        for merge_request in approved_data:
            web_url = str(merge_request)
            all_developers = approved_data[merge_request]
            approved_developers = [developers[user['user']['username']] for user in all_developers]
            need_approve_developers = need_approve_data[merge_request]
            approved_but_not_merged = len(need_approve_developers) == 0
            developers_to_send_message = [] if approved_but_not_merged else list(
                set(need_approve_developers) - set(approved_developers))
            developers_str = '👨‍💻 Z-z-z....' if approved_but_not_merged else ''.join(
                [('👨‍💻 ' + dev + '\n') for dev in developers_to_send_message])
            common_message += f'{developers_str[: -1]}\n➡️ {web_url}\n\n\n'

        found = len(common_message) != 0
        chat_message = f'{common_message} 👮‍Вы арестованы 🚔' if found else 'С мр-ами порядок 💅'

        clear_data()
        sound_manager.notify(found)

        if needNow:
            loading_gif_message_id = message.message_id + 1
            await bot.delete_message(message.chat.id, loading_gif_message_id)
            await message.reply(chat_message, disable_web_page_preview=True)
        else:
            await bot.send_message(message.chat.id, chat_message, disable_web_page_preview=True)
            await log_manager.show(log_message)
    else:
        await log_manager.show(log_message)


# Security
def security_decorator(reply_):
    async def check(message):
        if message.chat.id == dev_chat_id:
            await reply_(message)
        else:
            random_message = random.choice(access_denied_messages)
            await message.reply(f'{random_message}, leck mich am Arsch! 🔒')

    return check


# Commands
@dispatcher.message_handler()
@security_decorator
async def reply(message: types.Message):
    commands = {
        '/study': handle_study_command(message),
        '/help': handle_help_command(message),
        '/start': handle_start_command(message),
        '/check': handle_check_command(message)
    }
    bot_commands.update(commands)
    received_command = message.text in commands

    if received_command:
        try:
            run_received_command = commands[message.text]
            await run_received_command
        finally:
            pass


async def handle_study_command(message):
    await message.reply(study_message)


async def handle_help_command(message):
    available_commands = ', '.join(bot_commands.keys())
    await message.reply(f'💅Натаскана на команды: {available_commands}')


async def handle_start_command(message):
    global bot_is_running

    if bot_is_running:
        await message.reply('Вообще то уже работаю 🧸')
    else:
        random_message = random.choice(start_messages)
        await message.reply(f'{random_message} 💁🏻‍')
        while True:
            bot_is_running = True
            try:
                await send(message)
            except BotBlocked:
                pass
            except BadRequest:
                pass


async def handle_check_command(message):
    await message.reply_animation(animation_url, disable_notification=True)

    try:
        await send(message, True)
    except BotBlocked:
        await message.reply('👮‍Leck mich am Arsch! *** BotBlocked error ***, давай ещё разок чекнем 🧸')
        pass
    except BadRequest:
        await message.reply('👮‍Ein Scheißdreck werde ich tun! *** BadRequest error ***, попробуй ещё 🧸')
        pass


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
