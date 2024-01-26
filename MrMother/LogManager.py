import asyncio
import os
from MrMother.Config import delay_in_seconds
from pyfiglet import Figlet
import psutil
from MrMother.PidTracer import PidTracer


class LogManager(PidTracer):
    def __init__(self):
        renderer = Figlet(font='standard')
        self.trace_pid()
        self.program_name = renderer.renderText('MrMother  bot')
        self.stats = self.get_system_stats()
        self.yellow = '\033[33m'
        self.green = '\033[32m'

    def get_system_stats(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory()[2]
        power_metrics = os.popen('istats all').read()
        fan_and_temp = ''
        spaces = '                    '
        for word in power_metrics.splitlines():
            if 'speed' in word or 'temp' in word:
                fan_and_temp += f'  \033[32m{word}\n'
        return f'  CPU:{spaces}{cpu_usage} %\n  RAM:{spaces}{memory_usage} %\n{fan_and_temp}'

    async def show(self, log_message):
        current_progress = 1
        while current_progress <= delay_in_seconds:
            print('\33c')
            message = f'{self.green}{log_message}\n\n{self.stats}'
            print(f'{self.yellow}{self.program_name}')
            print('\r', message, sep='', end='\r')
            await asyncio.sleep(1)
            if current_progress % delay_in_seconds == 0:
                self.stats = self.get_system_stats()
            current_progress += 1
