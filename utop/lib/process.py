import os
import subprocess

from utop.lib.dataobject import DataObject


class Process(DataObject):

    def __init__(self, pid, uid, *args, **kwargs):
        """
        Creates a Process object from the data of various files in /proc/<pid>/
        """

        self.pid = pid
        self.uid = uid
        super().__init__(*args, **kwargs)

    def _read_stat(self):
        """
        Read the /proc/<pid>/stat file, holds the status information of the process.
        """
        stat_file = '/proc/{:d}/stat'.format(self.pid)
        with open(stat_file, 'r') as handle:
            self._stat = handle.read()

    def _read_statm(self):
        """
        Read the /proc/<pid>/statm file, provides information about memory usage, measured in pages.
        """
        statm_file = '/proc/{:d}/statm'.format(self.pid)
        with open(statm_file, 'r') as handle:
            self._statm = handle.read()

    def _read_io(self):
        """
        Read the /proc/<pid>/io file, provides information about IO operations.
        """
        io_file = '/proc/{:d}/io'.format(self.pid)
        try:
            with open(io_file, 'r') as handle:
                self._io = handle.read()
        except PermissionError:
            pass

    def _parse_stat(self):
        """
        Parses the data of /proc/<pid>/stat and sets its labels as class variables.
        """
        labels = [
            'pid', 'comm', 'state', 'ppid', 'pgrp', 'session', 'tty_nr', 'tpgid', 'flags',
            'minflt', 'majflt', 'cmajflt', 'utime', 'stime', 'cutime', 'cstime', 'priority',
            'nice', 'num_threads', 'itrealvalue', 'starttime', 'vsize', 'rss', 'rsslim',
            'startcode', 'endcode', 'startstack', 'kstkesp', 'kstkeip', 'signal', 'blocked',
            'sigignore', 'sigcatch', 'wchan', 'nswap', 'cnswap', 'exit_signal', 'processor',
            'rt_priority', 'policy', 'delayacct_blkio_ticks', 'guest_time', 'cguest_time',
        ]

        # Zip the labels and the stats together to create a dict.
        stat = dict(zip(labels, self._stat.split()))

        self.stat = stat

    def _parse_statm(self):
        """
        Parses the data of /proc/<pid>/statm and sets its labels as class variables.
        """

        labels = ['size', 'resident', 'share', 'text', 'lib', 'data', 'dt']

        # Zip the labels and the stats together to create a dict.
        statm = dict(zip(labels, self._statm.split()))

        self.statm = statm

    def _parse_io(self):
        """ Parse the data of /proc/<pid>/io. """

        if not hasattr(self, '_io'):
            self.io = {}
            return

        io = {}

        for line in self._io.split("\n"):
            try:
                label, value = line.split(": ")
                io[label] = value
            except ValueError:
                pass

        self.io = io

    def get_data(self):
        all_data = {'pid': self.pid, 'uid': self.uid}

        try:
            all_data.update(self.stat)
        except AttributeError:
            pass
        try:
            all_data.update(self.statm)
        except AttributeError:
            pass
        try:
            all_data.update(self.io)
        except AttributeError:
            pass

        return all_data


class ProcessList(DataObject):

    def __init__(self, *args, **kwargs):
        """ Create a ProcessList which holds Processes. """

        self._processlist = None
        self.processlist = None
        super().__init__(*args, **kwargs)

    def _read_processlist(self):
        self._processlist = subprocess.check_output(['ps', 'naux']).decode('utf-8')

    def _parse_processlist(self):

        process_list = {}

        for line in self._processlist.split("\n"):
            data = line.split()

            try:
                uid = data[0]
                pid = int(data[1])

                if os.path.exists('/proc/{:d}'.format(pid)):
                    process = Process(pid, uid)

                    process_list[pid] = process.get_data()

            except IndexError:
                continue  # last (empty) line of ps?
            except (KeyError, ValueError):
                # Continue when this is the header line.
                if data[0] == 'USER':
                    continue
            except FileNotFoundError:
                # The Process can't find one of the files, this probably means the process no longer
                # exists.
                continue

        self.processlist = process_list

    def get_data(self):
        return self.processlist
