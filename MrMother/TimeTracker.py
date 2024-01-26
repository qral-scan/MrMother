from datetime import datetime


class TimeTracker:
    def get_current_time(self):
        return datetime.now().strftime('%H:%M')

    def get_current_weekday(self):
        return datetime.now().weekday()
