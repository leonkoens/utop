
from view import View


class Footer(View):

    def draw(self):
        self.window.erase()
        self.addstr(1, 1, "(H)elp")
