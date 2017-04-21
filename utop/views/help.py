from utop.view import View


class Help(View):

    def draw(self):
        self.window.erase()

        help_items = {
            'sorting': [
                'c - cpu',
                'p - processes',
                'm - memory',
            ],

        }

        y = 0
        x = 4

        for key in help_items.keys():
            y += 2
            self.addstr(y, x, "{}:".format(key.title()))

            for line in help_items[key]:
                y += 1
                self.addstr(y, x, "\t{}".format(line))
