import unittest

from utop.lib.cpu import CPU


class CPUDataTest(unittest.TestCase):

    def test_init(self):

        proc_stat = """
cpu  500836 992 272393 5454178 14582 0 6466 0 0 0
cpu0 128274 228 68444 1362965 3650 0 1537 0 0 0
cpu1 126121 215 67211 1365474 3540 0 1806 0 0 0
cpu2 120735 234 68351 1359295 3622 0 2223 0 0 0
cpu3 125705 313 68385 1366443 3768 0 900 0 0 0
ctxt 65480544
btime 1508485899
processes 12668
procs_running 1
procs_blocked 0
softirq 16145353 1051234 4038531 3005 1664020 0 0 3203553 3893859 0 2291151
"""
        cpu = CPU('cpu  500836 992 272393 5454178 14582 1 6466 2 3 4')

        data = cpu.get_data()

        self.assertEqual(data['user'], '500836')
        self.assertEqual(data['nice'], '992')
        self.assertEqual(data['system'], '272393')
        self.assertEqual(data['idle'], '5454178')
        self.assertEqual(data['iowait'], '14582')
        self.assertEqual(data['irq'], '1')
        self.assertEqual(data['softirq'], '6466')
        self.assertEqual(data['steal'], '2')
        self.assertEqual(data['guest'], '3')
        self.assertEqual(data['guest_nice'], '4')
