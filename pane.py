

class Pane(object):

    view = None
    window = None

    def __init__(self, stdscr, width, height, x=0, y=0):
        self.window = stdscr.subwin(height, width, y, x)

    def set_view(self, view):
        view.set_window(self.window)
        self.view = view

    def refresh(self):
        self.view.draw()
        self.window.noutrefresh()
