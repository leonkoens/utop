import subprocess

from utop.lib.dataobject import DataObject


class CPU:

    def __init__(self, line):
        """
        Create a new CPU object which parses the data from the output of /proc/stat.
        """

        labels = [
            'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal', 'guest',
            'guest_nice'
        ]

        data = line.split()
        stat = dict(zip(labels, data[1:]))

        self.__dict__.update(stat)

    def get_data(self):
        return self.__dict__


class CPUList(DataObject):

    def _read_stat(self):
        with open('/proc/stat', 'r') as handle:
            self._stat = handle.read()

    def _parse_stat(self):

        cpu_data = {}

        for line in self._stat.split("\n"):
            data = line.split()

            try:
                key = data[0]

            except IndexError:
                # Last line
                continue

            if 'cpu' in key:
                cpu = CPU(line)
                cpu_data[key] = cpu.get_data()

        self.cpu_data = cpu_data

    def get_data(self):
        return self.cpu_data







