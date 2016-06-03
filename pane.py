import logging


class PaneSet(object):

    def __init__(self, model):
        self.model = model
        self.panes = []

        self.set_panes()

    def refresh(self):
        logging.debug(len(self.panes))
        for pane in self.panes:
            pane.refresh()


class Pane(object):

    view = None
    window = None

    def __init__(self, stdscr, width, height, x=0, y=0):
        self.window = stdscr.subwin(height, width, y, x)

    def set_view(self, view):
        view.set_window(self.window)
        self.view = view

    def refresh(self):
        self.window.noutrefresh()
        self.view.draw()
