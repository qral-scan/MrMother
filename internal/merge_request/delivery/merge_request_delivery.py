from multiprocessing.spawn import get_command_line
from typing import Mapping, Tuple, TypeAlias
from aiogram import html
from internal.merge_request.usecase.merge_request_usecase import merge_request_usecase
from aiogram.enums import ParseMode
import jinja2

class merge_request_delivery:
    usecase: merge_request_usecase
    checktemplate: jinja2.environment.Template

    def __init__(self, usecase: merge_request_usecase):
        self.usecase = usecase
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "templates/check.html"
        self.checktemplate = templateEnv.get_template(TEMPLATE_FILE)
        pass

    def setup(self, commands, message):
        commands["/check"] = self.handle_check_command(message)
        return commands

    async def handle_check_schedule(self, bot, chat_id):
        err, prs, rd, asgn = self.usecase.check_pull_requests()
        context = {"prs": prs, "rd": rd, "asgn": asgn}
        await bot.send_message(
            chat_id=chat_id,
            text=self.checktemplate.render(context),
            parse_mode=ParseMode.HTML,
        )

    async def handle_check_command(self, message, **kwargs):
        err, prs, rd, asgn = self.usecase.check_pull_requests()
        context = {"prs": prs, "rd": rd, "asgn": asgn}
        await message.answer(
            text=self.checktemplate.render(context), parse_mode=ParseMode.HTML
        )
