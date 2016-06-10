
import curses

class View(object):

    def __init__(self, model):
        self.model = model

    def set_window(self, window):
        self.window = window

    def addstr(self, y, x, text, color=None):

        if color is None:
            color = self.model.COLOR_DEFAULT

        try:
            self.window.addstr(y, x, text, curses.color_pair(color))
        except curses.error:
            pass
