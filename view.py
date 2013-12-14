
import curses

class View(object):

    def __init__(self, model):
        self.model = model

    def set_window(self, window):
        self.window = window

    def addstr(self, y, x, text):
        try:
            self.window.addstr(y, x, text)
        except curses.error:
            pass
