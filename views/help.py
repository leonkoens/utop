from view import View


class Help(View):

    def draw(self):
        self.window.erase()
        help = {
            'sorting': [
                'c - cpu',
                'p - processes',
                'm - memory',
            ]
                

        }

        y = 4
        x = 4

        def addstr(text):
            self.addstr(y, x, text)
            y += 1

        for key in help.keys():
            addstr("{}:".format(key.title()))

            for line in help[key]:
                addstr("{}:".format(line))
