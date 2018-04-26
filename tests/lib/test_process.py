from unittest import mock, TestCase

from utop.lib.process import Process, ProcessList


class ProcessTest(TestCase):

    def get_process(self):

        with mock.patch.object(Process, '_read_stat'), \
                mock.patch.object(Process, '_read_statm'), \
                mock.patch.object(Process, '_read_io'):

            process = Process(11890, 1000, read_data=False)
            process._stat = "11890 (java) S 11831 2009 2009 1026 2009 1077936128 167555 289864 230 28 70018 1609 1040 92 20 0 45 0 1356829 4780576768 213525 18446744073709551615 4194304 4196492 140734514749312 0 0 0 0 4096 16796879 0 0 0 17 0 0 0 0 0 0 6293648 6294284 25358336 140734514758302 140734514759805 140734514759805 140734514761631 0"
            process._statm = "1168418 224312 9493 1 0 260810 0"
            process._io = """rchar: 205876817
wchar: 33927871
syscr: 73070
syscw: 8319
read_bytes: 251510784
write_bytes: 31617024
cancelled_write_bytes: 8192"""

            return process

    def test_parse_stat(self):
        process = self.get_process()

        process._parse_stat()
        data = process.get_data()

        self.assertEqual(data['pid'], '11890')
        self.assertEqual(data['state'], 'S')

    def test_parse_statm(self):
        process = self.get_process()

        process._parse_statm()
        data = process.get_data()

        self.assertEqual(data['size'], '1168418')
        self.assertEqual(data['resident'], '224312')

    def test_parse_io(self):
        process = self.get_process()

        process._parse_io()
        data = process.get_data()


        self.assertEqual(data['rchar'], '205876817')
        self.assertEqual(data['read_bytes'], '251510784')


#class ProcessListTest(TestCase):
#
#    def test_get_dataobjects(self):
#        processlist = ProcessList()
#        import pdb;pdb.set_trace()


