import re
import subprocess

from utop.lib.dataobject import DataObject


class Memory(DataObject):

    def _read_meminfo(self):
        """ Read the memory info from /proc/meminfo. """
        with open('/proc/meminfo', 'r') as handle:
            self._meminfo = handle.read()

    def _parse_meminfo(self):
        """ Parse the info from /proc/meminfo. Calculate the free memory and swap. """

        labels = [
            'mem_total', 'mem_free', 'cached', 'buffers', 'swap_total', 'swap_free',
        ]

        regexes = [
            'MemTotal: +(\d+)', 'MemFree: +(\d+)', 'Cached: +(\d+)', 'Buffers: +(\d+)',
            'SwapTotal: +(\d+)', 'SwapFree: +(\d+)',
        ]

        values = []

        for regex in regexes:
            values.append(int(re.search(regex, self._meminfo).group(1)))

        stat = dict(zip(labels, values))

        # mem_free = mem_free + cached + buffers
        percentage = 100 - int(float(stat['mem_free']) / float(stat['mem_total']) * 100)
        stat['mem_percentage'] = percentage
        stat['mem_use'] = stat['mem_total'] - stat['mem_free']

        percentage = 100 - int(float(stat['swap_free']) / float(stat['swap_total']) * 100)
        stat['swap_percentage'] = percentage
        stat['swap_use'] = stat['swap_total'] - stat['swap_free']

        self.meminfo = stat

    def get_data(self):
        return self.meminfo
