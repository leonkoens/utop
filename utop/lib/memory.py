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
            'mem_total', 'mem_free', 'cached', 'buffers', 'sreclaimable', 'shmem', 'swap_total',
            'swap_free',
        ]

        regexes = [
            'MemTotal: +(\d+)', 'MemFree: +(\d+)', 'Cached: +(\d+)', 'Buffers: +(\d+)',
            'SReclaimable: +(\d+)', 'Shmem: +(\d+)', 'SwapTotal: +(\d+)', 'SwapFree: +(\d+)',
        ]

        values = []

        for regex in regexes:
            values.append(int(re.search(regex, self._meminfo).group(1)))

        stat = dict(zip(labels, values))

        # Like htop calculates it.
        cached = stat['cached'] + stat['sreclaimable'] - stat['shmem']
        used = stat['mem_total'] - (stat['mem_free'] + stat['buffers'] + cached)

        stat['mem_cached'] = cached
        stat['mem_use'] = used

        stat['swap_use'] = stat['swap_total'] - stat['swap_free']

        self.meminfo = stat

    def get_data(self):
        return self.meminfo
