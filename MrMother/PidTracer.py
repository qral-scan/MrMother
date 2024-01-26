import os


# To kill process outside (for my voice assistant)
class PidTracer:
    def change_pid(self):
        with open('pid.txt', 'w+') as f:
            f.write(str(os.getpid()))
            f.close()

    def trace_pid(self):
        try:
            with open('pid.txt', 'x') as file:
                file.close()
                self.change_pid()
        except BaseException as exists:
            if exists:
                self.change_pid()
