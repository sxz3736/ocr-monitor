from datetime import datetime

class Logger:
    def __init__(self, widget=None):
        self.widget = widget

    def info(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        text = f"[{ts}] {msg}"
        if self.widget:
            self.widget.append(text)
        else:
            print(text)
