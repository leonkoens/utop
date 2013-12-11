

class View(object):

    def __init__(self, model):
        self.model = model

    def set_window(self, window):
        self.window = window

    def addstr(self, y, x, text):
        self.window.addstr(y, x, text)
