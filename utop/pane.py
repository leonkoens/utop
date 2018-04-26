import logging


class PaneSet:

    def __init__(self, model):
        self.model = model
        self.panes = []

        self.set_panes()

    def set_panes(self):
        raise NotImplementedError()

    def refresh(self):
        logging.debug("Number of panes: {:d}".format(len(self.panes)))
        for pane in self.panes:
            pane.refresh()


class Pane:

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
