import random
from GitlabManager import GitlabManager
from GithubManager import GithubManager
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
bot_commands = {}
repo_manager = GithubManager()


async def send_daily_notification(message, weekday, time):
    if weekday in daily_schedule.keys() and time == daily_schedule[weekday]:
        sound_manager.notify(text='Пора на дейли')
        daily_notification = '🌚 Дейли'
        await bot.send_message(message.chat.id, daily_notification, disable_web_page_preview=True)


async def send(message: types.Message, needNow: bool = None):
    weekday = timeTracker.get_current_weekday()
    time = timeTracker.get_current_time()
    log_message = f'  State: running\n  Server time: {time}'

    await send_daily_notification(message, weekday, time)

    if weekday in work_days and time in schedule or needNow:
        chat_message = repo_manager.create_msg()
        found = chat_message != '👮🏻 Уровень преступности в норме, в городе спокойно 💅'
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
