class Logger:
    def __init__(self, do_print=True):
        self.messages = []
        self.do_print = do_print

    def log(self, level, message):
        self.messages.append((level, message))
        if self.do_print:
            print(f"[{level}] {message}")

    def info(self, message):
        self.log("info", message)

    def warn(self, message):
        self.log("warn", message)

    def error(self, message):
        self.log("error", message)

    def analyze_log(self):
        pass

    def write_log(self):
        pass
