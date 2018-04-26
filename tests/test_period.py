import unittest

from utop.lib.dataobject import DataObject
from utop.lib.process import ProcessList, Process
from utop.period import Period


class PeriodTest(unittest.TestCase):

    def test_tick_size(self):
        """ Check if the ticks in the Period object do not exceed the ticks_max. """

        period = Period(ticks_max=5)

        for i in range(10):
            period.add_tick(i)

        self.assertTrue(len(period.ticks) == 5)

    def test_get_delta(self):
        """ Check if Period can calculate a correct delta of a value. """

        class Foo(DataObject):
            def __init__(self, value):
                self.value = value

            def get_data(self):
                return {'value': self.value}

        period = Period(ticks_max=5)

        for i in range(10):
            foo = Foo(i)
            period.add_tick(foo)

        # Period:
        #     CPUData
        #
        # Period.get_delta -> {'value1': value1, 'value2': value2}
        delta = period.get_delta(['value'])
        self.assertTrue('value' in delta)

        # 5, 6, 7, 8, 9
        # 9 - 5 = 4
        self.assertTrue(delta['value'] == 4)

    def test_get_delta_list(self):

        period = Period(ticks_max=3)

        for i in range(1, 4):
            processlist = ProcessList(read_data=False)
            processlist.processlist = {}

            for j in range(1, 11):
                process = Process(pid=j, uid=1000, read_data=False)
                process.stat = {'value': j * i}

                processlist.processlist[process.pid] = process

            period.add_tick(processlist)

        # Period:
        #     ProcessList:
        #         Process
        #
        # Period.get_delta -> {
        #     '<pid>': {'value1': value1, 'value2': value2}
        #     '<pid>': {'value1': value1, 'value2': value2}
        # }
        delta = period.get_delta(['value'])

        # 2 * 1 - 0 * 1
        self.assertEqual(delta[1]['value'], 2.0)

        # 2 * 8 - 0 * 8
        self.assertEqual(delta[8]['value'], 16.0)

