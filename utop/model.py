import curses
import importlib
import logging
import subprocess

from utop.controller import Controller
from utop.lib.cpu import CPUList
from utop.lib.memory import Memory
from utop.lib.process import ProcessList
from utop.lib.user import UserList
from utop.period import Period

COLOR_DEFAULT = 0
COLOR_RED = 1
COLOR_GREEN = 2
COLOR_YELLOW = 3
COLOR_BLUE = 4
COLOR_MAGENTA = 5
COLOR_CYAN = 6


class Model(object):
    """ This class holds all the data. """

    bar_width = 25
    columns = {
        'user':     {'width': 25,   'title': 'User',    'format': '{:s}'},
        'procs':    {'width': 8,    'title': 'PROC #',  'format': '{:d}'},
        'mem_percentage':      {'width': 8,    'title': 'MEM %',   'format': '{:2.2f}'},
        'cpu_percentage':      {'width': 8,    'title': 'CPU %',   'format': '{:2.2f}'},
    }
    running = True

    colors = {
        COLOR_RED: (curses.COLOR_RED, -1),
        COLOR_GREEN: (curses.COLOR_GREEN, -1),
        COLOR_YELLOW: (curses.COLOR_YELLOW, -1),
        COLOR_BLUE: (curses.COLOR_BLUE, -1),
        COLOR_MAGENTA: (curses.COLOR_MAGENTA, -1),
        COLOR_CYAN: (curses.COLOR_CYAN, -1),
    }

    def __init__(self, stdscr=None):
        """ Initiate the model and thus utop. Start the controller to handle 
        user input. Call setup to start the interface and get some static info.
        Finally start the refresh loop.
        """

        self.stdscr = stdscr
        self.controller = Controller(self)

        self.mode = 'default'
        self.sort_by = 'cpu_percentage'
        self.sort_order = 'asc'
        self.ticks_max = 5
        self.user_list = None
        self.user_data = {}
        self.sorted_columns = ['user', 'procs', 'mem_percentage', 'cpu_percentage']

        self.cpu_period = Period(self.ticks_max)
        self.process_list_period = Period(self.ticks_max)
        self.memory_period = Period(self.ticks_max)

        self.set_curses()
        self.set_user_list()

        while self.running:
            self.refresh()

    def refresh(self):
        """ Refresh the panes and update the interface. """

        logging.debug("---")
        logging.debug("Current mode is: {}".format(self.mode))

        self.set_paneset()

        self.update_processlist_period()
        self.update_cpu_data_period()
        self.update_memory_period()

        self.set_cpu_data()
        self.set_mem_data()
        self.set_load()
        self.set_user_data()
        self.set_sorted_users()

        self.paneset.refresh()

        if self.stdscr is not None:
            curses.doupdate()
            self.controller.handle_key(self.stdscr.getch())

    def set_curses(self):
        """ Set some curses settings. """
        if self.stdscr is not None:
            curses.cbreak()

            curses.start_color()
            curses.use_default_colors()

            for key, value in self.colors.items():
                curses.init_pair(key, value[0], value[1])

            self.stdscr.timeout(500)

    def set_paneset(self):
        """ Setup the panes. A header, footer and middle section. """

        try:
            self.maxy, self.maxx = self.stdscr.getmaxyx()
        except AttributeError:
            return  # stdscr is not set.

        try:

            paneset_classname = "{}PaneSet".format(self.mode.title())
            lib = importlib.import_module('utop.panesets.{}'.format(self.mode))
            self.paneset = getattr(lib, paneset_classname)(self)

            logging.debug('Set paneset to {}'.format(self.mode))

        except curses.error:
            pass  # Terminal is probably to small.

    def set_user_list(self):
        """ Retrieve the system users information. """
        user_list = UserList()
        self.user_list = user_list.get_data()

    def update_cpu_data_period(self):
        self.cpu_period.add_tick(CPUList())

    def update_processlist_period(self):
        self.process_list_period.add_tick(ProcessList())

    def update_memory_period(self):
        self.memory_period.add_tick(Memory())

    def get_pid_to_uid(self):

        latest = self.process_list_period.ticks[-1]
        latest_data = latest.get_data()

        pid_to_uid = {}

        for latest_key, latest_value in latest_data.items():
            pid_to_uid[latest_key] = latest_value['uid']

        return pid_to_uid

    def set_user_data(self):
        """
        {
            uid: {'cpu': '5%', 'mem': '10%', 'procs': 10},
        }
        """

        if len(self.process_list_period.ticks) < 2:
            return

        user_data = {}
        pid_to_uid = self.get_pid_to_uid()

        process_total = self.process_list_period.get_list_totals(['resident'])
        process_delta = self.process_list_period.get_delta(
            ['utime', 'stime', 'cutime', 'cstime', 'resident'])

        for key, value in process_delta.items():
            try:
                uid = pid_to_uid[key]
            except KeyError:
                # This process no longer exists.
                continue

            try:
                user_data[uid]['cpu'] += value['utime'] + value['stime']
                #user_data[uid]['cpu'] += value['cutime'] + value['cstime']
                user_data[uid]['mem'] += process_total[key]['resident']
                user_data[uid]['procs'] += 1
            except KeyError:
                user_data[uid] = {
                    'cpu': value['utime'] + value['stime'],
                    'mem': process_total[key]['resident'],
                    'procs': 1,
                    'user': self.user_list[uid]['name'],
                }

        cpu_delta = self.cpu_period.get_delta([
            'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal', 'guest',
            'guest_nice'
        ])
        cpu_delta = sum(cpu_delta['cpu'].values())

        for key, value in user_data.items():
            user_data[key]['cpu_percentage'] = (user_data[key]['cpu'] / cpu_delta) * 100
            user_data[key]['mem_percentage'] = (
                                                   (user_data[key]['mem'] / self.ticks_max) /
                                                   self.mem_data['mem_total']) * 100

        logging.debug("Root %CPU  {:f}".format(user_data['0']['cpu_percentage']))

        self.user_data = user_data

    def set_sorted_users(self):
        """ Create a sorted list of the users. """
        self.sorted_users = sorted(
            self.user_data,
            key=lambda user: self.user_data[user][self.sort_by],
            reverse=self.sort_order == 'asc',
        )

    def set_load(self):
        """ Set the load averages. """

        with open('/proc/loadavg', 'r') as handle:
            stats = handle.read()

        stats = stats.split(' ')

        self.load_averages = stats[:3]
        self.running_processes = stats[3]

    def set_cpu_data(self):

        cpu_delta = self.cpu_period.get_delta([
            'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal', 'guest',
            'guest_nice'
        ])['cpu']

        total = sum(cpu_delta.values())

        try:
            self.cpu_data = {
                    'busy': ((total - (cpu_delta['idle'] + cpu_delta['iowait'])) / total) * 100,
                    'user': (cpu_delta['user'] / total) * 100,
                    'system': (cpu_delta['system'] / total) * 100,
                    'wait': (cpu_delta['iowait'] / total) * 100,
                }
        except ZeroDivisionError:
            self.cpu_data = {
                'busy': 0,
                'user': 0,
                'system': 0,
                'wait': 0,
            }

        logging.debug(self.cpu_data)

    def set_mem_data(self):

        mem_data = self.memory_period.get_total(['mem_total', 'mem_use', 'swap_total', 'swap_use'])

        mem_total = mem_data['mem_total'] / len(self.memory_period.ticks)
        mem_use = mem_data['mem_use'] / len(self.memory_period.ticks)

        swap_total = mem_data['swap_total'] / len(self.memory_period.ticks)
        swap_use = mem_data['swap_use'] / len(self.memory_period.ticks)

        self.mem_data = {
            'mem_total': mem_total,
            'mem_use': mem_use,
            'mem_percentage': (mem_use / mem_total) * 100,
            'swap_total': swap_total,
            'swap_use': swap_use,
            'swap_percentage': (swap_use / swap_total) * 100,
        }

        logging.debug(self.mem_data)



