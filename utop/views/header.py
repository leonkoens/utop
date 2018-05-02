from utop.view import View
from utop import model


class Header(View):

    def draw(self):
        self.window.erase()
        self.draw_load(1)
        self.draw_cpu(2)
        self.draw_mem(3)
        self.draw_swap(4)

    def draw_load(self, y):
        self.addstr(1, 1, "Load:")
        i = 8
        for load in self.model.load_averages:
            self.addstr(y, i, load)
            i += len(load) + 1

        text = "Running: " + self.model.running_processes
        self.addstr(y, i + 1, text)

    def draw_bar(self, y, percentage, label):
        width = self.model.bar_width
        bar_width = int((float(percentage) / 100.00) * width)
        self.addstr(y, 1, label + '  [')
        self.addstr(y, 7, '|' * bar_width, model.COLOR_GREEN)
        self.addstr(y, 8 + width, '] {:2.0f}%'.format(percentage))

    def draw_cpu(self, y):
        self.draw_bar(y, self.model.cpu_data['busy'], "cpu")

        user = "us {:2.0f}".format(self.model.cpu_data['user'])
        system = "sy {:2.0f}".format(self.model.cpu_data['system'])
        wait = "wa {:2.0f}".format(self.model.cpu_data['wait'])

        self.addstr(y, self.model.bar_width + 16, user)
        self.addstr(y, self.model.bar_width + 22, system)
        self.addstr(y, self.model.bar_width + 28, wait)

    def draw_mem(self, y):
        self.draw_bar(y, self.model.mem_data['mem_percentage'], "mem")

        mem_use = "{:4.0f}M".format(self.model.mem_data['mem_use'] / 1024)
        mem_total = "{:4.0f}M".format(self.model.mem_data['mem_total'] / 1024)

        text = mem_use + " / " + mem_total

        self.addstr(y, self.model.bar_width + 16, text)

    def draw_swap(self, y):
        self.draw_bar(y, self.model.mem_data['swap_percentage'], "swp")

        swap_use = "{:4.0f}M".format(self.model.mem_data['swap_use'] / 1024)
        swap_total = "{:4.0f}M".format(self.model.mem_data['swap_total'] / 1024)

        text = swap_use + " / " + swap_total

        self.addstr(y, self.model.bar_width + 16, text)
