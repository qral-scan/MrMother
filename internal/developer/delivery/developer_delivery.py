from typing import Mapping, TypeAlias

import jinja2
from internal.developer.usecase.developer_usecase import developer_usecase
from aiogram.enums import ParseMode

class developer_delivery:
    usecase: developer_usecase
    build_template: jinja2.environment.Template

    def __init__(self, usecase: developer_usecase):
        self.usecase = usecase
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        self.build_template = templateEnv.get_template("templates/build.html")
        pass

    def setup(self, commands, message):
        commands["/build"] = self.handle_build_command(message)
        return commands

    async def handle_build_command(self, message, **kwargs):
        err = self.usecase.start_build_job()
        if err == None:
            await message.answer(
                text=self.build_template.render(
                    {
                        "html_url": "https://github.com/qral-scan/scout/actions",
                        "workflow_title": "deploy firebase",
                    }
                ),
                parse_mode=ParseMode.HTML,
            )
