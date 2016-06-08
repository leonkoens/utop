
from view import View


class Header(View):

    def draw(self):
        self.window.erase()
        self.draw_load(1)
        self.draw_cpu(2)
        self.draw_mem(3)
        self.draw_swap(4)
        self.draw_latest_ticks(6)

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
        self.addstr(y, 7, '|' * bar_width)
        self.addstr(y, 8 + width, '] ' + str(percentage) + '%')

    def draw_cpu(self, y):
        self.draw_bar(y, self.model.cpu_data['busy'], "cpu")

        user = "us " + str(self.model.cpu_data['user'])
        system = "sy " + str(self.model.cpu_data['system'])
        wait = "wa " + str(self.model.cpu_data['wait'])

        self.addstr(y, self.model.bar_width + 16, user)
        self.addstr(y, self.model.bar_width + 22, system)
        self.addstr(y, self.model.bar_width + 28, wait)

    def draw_mem(self, y):
        self.draw_bar(y, self.model.mem_data['mem'], "mem")
        raw = self.model.mem_data_raw
        mem_use = "{:4.0f}M".format(raw['mem_use'] / 1000)
        mem_total = "{:4.0f}M".format(raw['mem_total'] / 1000)
        text = mem_use + " / " + mem_total
        self.addstr(y, self.model.bar_width + 16, text)

    def draw_swap(self, y):
        self.draw_bar(y, self.model.mem_data['swap'], "swp")
        raw = self.model.mem_data_raw
        swap_use = "{:4.0f}M".format(raw['swap_use'] / 1000)
        swap_total = "{:4.0f}M".format(raw['swap_total'] / 1000)
        text = swap_use + " / " + swap_total
        self.addstr(y, self.model.bar_width + 16, text)

    def draw_latest_ticks(self, y):
        self.addstr(y, 4, 'last 5 ticks')
