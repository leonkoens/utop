
import curses

import model

class View(object):

    def __init__(self, model):
        self.model = model

    def set_window(self, window):
        self.window = window

    def addstr(self, y, x, text, color=None, underline=False):

        if color is None:
            color = model.COLOR_DEFAULT

        color = curses.color_pair(color)

        if underline:
            color = color | curses.A_UNDERLINE

        try:
            self.window.addstr(y, x, text, color)
        except curses.error:
            pass
