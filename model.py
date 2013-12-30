import curses
import logging
import re
import subprocess
import traceback

from pane import Pane
from controller import Controller

from views.footer import Footer as FooterView
from views.header import Header as HeaderView
from views.content import Content as ContentView


class Model(object):
    """ Utop, this class acts as the model. """

    bar_width = 25
    columns = {
        'user': {'width': 25, 'title': 'User'},
        'procs': {'width': 12, 'title': 'Processes'},
        'mem': {'width': 8, 'title': 'MEM %'},
        'cpu': {'width': 8, 'title': 'CPU %'},
    }
    cpu_data = {'user': 0, 'system': 0, 'idle': 0, 'wait': 0}
    cpu_data_raw = {}
    load_averages = ()
    maxx = 0
    maxy = 0
    mem_data = {}
    mem_data_raw = {}
    number_of_cpu = 1
    panes = []
    running = True
    running_processes = 0
    sort_by = 'cpu'
    sorted_columns = ('user', 'procs', 'cpu', 'mem')
    sorted_users = []
    uids = {}
    user_data = {}

    def __init__(self, stdscr=None):
        self.stdscr = stdscr
        self.controller = Controller(self)

        self.setup()

        while self.running:
            self.refresh()

    def setup(self):
        """ Do some initial setup thins."""
        self.set_curses()
        self.set_panes()
        self.set_uid_info()
        self.set_number_of_cpu()

    def refresh(self):
        """ Refresh the panes and update the interface. """
        self.set_user_data()
        self.set_sorted_user_list()
        self.set_cpu_data()
        self.set_load()
        self.set_memory_data()

        for pane in self.panes:
            pane.refresh()

        if self.stdscr is not None:
            curses.doupdate()
            self.controller.handle_key(self.stdscr.getch())

    def set_curses(self):
        if self.stdscr is not None:
            curses.cbreak()
            self.stdscr.timeout(500)

    def set_panes(self):
        """ Setup the panes. A header, footer and middle section. """
        try:
            (self.maxy, self.maxx) = self.stdscr.getmaxyx()
        except AttributeError:
            return  # stdscr is not set.

        header = Pane(self.stdscr, self.maxx, 10)
        header.set_view(HeaderView(self))

        content = Pane(self.stdscr, self.maxx, self.maxy - 12, 0, 10)
        content.set_view(ContentView(self))

        footer = Pane(self.stdscr, self.maxx, 2, 0, self.maxy - 2)
        footer.set_view(FooterView(self))

        self.panes.append(header)
        self.panes.append(content)
        self.panes.append(footer)

    def set_uid_info(self):
        """ Retrieve the system users information. """
        passwd = subprocess.check_output(['cat', '/etc/passwd'])

        for line in passwd.split("\n"):
            try:
                data = line.split(":")
                self.uids[data[2]] = data[0]
            except IndexError:
                pass  # Ignore headers

    def set_number_of_cpu(self):
        """ Retrieve the number of cpu's of the system. """
        cat = subprocess.Popen(
            ['cat', '/proc/cpuinfo'],
            stdout=subprocess.PIPE
        )

        self.number_of_cpu = int(subprocess.Popen(
            ['grep', '-c', 'processor'],
            stdin=cat.stdout,
            stdout=subprocess.PIPE
        ).communicate()[0])

    def set_user_data(self):
        """ Retrieve the data of the users. """
        self.user_data = {}
        output = subprocess.check_output(['ps', 'naux'])

        for line in output.split("\n"):
            data = line.split()
            user = None

            try:
                user = self.user_data[data[0]]

            except IndexError:
                continue  # last (empty) line of ps?
            except KeyError:
                if data[0] == 'USER':
                    continue

                user = {'cpu': 0.0, 'mem': 0.0, 'procs': 0}
                self.user_data[data[0]] = user

            user['cpu'] += float(data[2])
            user['mem'] += float(data[3])
            user['procs'] += 1

        for key, value in self.user_data.iteritems():
            cpu = self.user_data[key]['cpu'] / self.number_of_cpu
            self.user_data[key]['rcpu'] = cpu
            self.user_data[key]['user'] = self.uids[key]

    def set_sorted_user_list(self):
        """ Create a sorted list of the users. """
        self.sorted_users = sorted(
            self.user_data,
            cmp=lambda y, x: cmp(
                self.user_data[x][self.sort_by],
                self.user_data[y][self.sort_by]
            )
        )

    def set_cpu_data(self):
        stats = subprocess.check_output(['cat', '/proc/stat'])
        stats = re.split(' +', stats.split('\n')[0])[1:]
        stats = map(int, stats)
        self.cpu_data['busy'] = 0

        """
        0 user: normal processes executing in user mode
        1 nice: niced processes executing in user mode
        2 system: processes executing in kernel mode
        3 idle: twiddling thumbs
        4 iowait: waiting for I/O to complete
        5 irq: servicing interrupts
        6 softirq: servicing softirqs
        7 steal: involuntary wait
        8 guest: running a normal guest
        9 guest_nice: running a niced guest
        """

        prev = self.cpu_data_raw.copy()

        self.cpu_data_raw['user'] = stats[0] + stats[1]
        system = stats[2] + stats[5] + stats[6] + stats[8] + stats[9]
        self.cpu_data_raw['system'] = system
        self.cpu_data_raw['idle'] = stats[3]
        self.cpu_data_raw['wait'] = stats[4] + stats[7]

        try:
            total = 0  # Calculate total for percentages.
            for key, value in self.cpu_data_raw.iteritems():
                new_value = value - prev[key]
                total += new_value
                self.cpu_data[key] = new_value

            for key, value in self.cpu_data.iteritems():
                self.cpu_data[key] = int((float(value) / float(total)) * 100)

            self.cpu_data['busy'] = int(100 - self.cpu_data['idle'])
        except KeyError:
            pass  # First time.

    def set_load(self):
        stats = subprocess.check_output(['cat', '/proc/loadavg'])
        stats = stats.split(' ')

        self.load_averages = stats[:3]
        self.running_processes = stats[3]

    def set_memory_data(self):
        stats = subprocess.check_output(['cat', '/proc/meminfo'])

        mem_total = int(re.search('MemTotal: +(\d+)', stats).group(1))
        mem_free = int(re.search('MemFree: +(\d+)', stats).group(1))
        cached = int(re.search('Cached: +(\d+)', stats).group(1))
        buffers = int(re.search('Buffers: +(\d+)', stats).group(1))

        mem_free = mem_free + cached + buffers

        self.mem_data_raw['mem_total'] = mem_total
        self.mem_data_raw['mem_free'] = mem_free
        self.mem_data_raw['mem_use'] = mem_total - mem_free

        swap_total = int(re.search('SwapTotal: +(\d+)', stats).group(1))
        swap_free = int(re.search('SwapFree: +(\d+)', stats).group(1))

        self.mem_data_raw['swap_total'] = swap_total
        self.mem_data_raw['swap_free'] = swap_free
        self.mem_data_raw['swap_use'] = swap_total - swap_free

        percentage = int(float(mem_free) / float(mem_total) * 100)
        percentage = 100 - percentage
        self.mem_data['mem'] = percentage

        percentage = int(float(swap_free) / float(swap_total) * 100)
        percentage = 100 - percentage
        self.mem_data['swap'] = percentage

