from unittest import mock, TestCase

from utop.lib.memory import Memory


class MemoryTest(TestCase):

    def test_memory(self):

        memory = Memory(read_data=False)
        memory._meminfo = """
MemTotal:       16306452 kB   
MemFree:         6011204 kB   
MemAvailable:    8182840 kB   
Buffers:          226304 kB   
Cached:          3172716 kB   
SwapCached:            0 kB   
Active:          5799664 kB   
Inactive:        2305104 kB   
Active(anon):    4708012 kB   
Inactive(anon):  1128212 kB   
Active(file):    1091652 kB   
Inactive(file):  1176892 kB   
Unevictable:          48 kB   
Mlocked:              48 kB   
SwapTotal:      16654332 kB   
SwapFree:       16654332 kB   
Dirty:             20264 kB   
Writeback:             0 kB   
AnonPages:       3796676 kB   
Mapped:          2518428 kB   
Shmem:           1130480 kB   
Slab:             323012 kB   
SReclaimable:     249460 kB   
SUnreclaim:        73552 kB   
KernelStack:       15168 kB   PageTables:        58096 kB   
NFS_Unstable:          0 kB   
Bounce:                0 kB   
WritebackTmp:          0 kB   
CommitLimit:    24807556 kB   
Committed_AS:   13959192 kB   
VmallocTotal:   34359738367 kB
VmallocUsed:           0 kB   
VmallocChunk:          0 kB   
HardwareCorrupted:     0 kB   
AnonHugePages:   1249280 kB   
ShmemHugePages:        0 kB   
ShmemPmdMapped:        0 kB   
CmaTotal:              0 kB   
CmaFree:               0 kB   
HugePages_Total:       0      
HugePages_Free:        0      
HugePages_Rsvd:        0      
HugePages_Surp:        0      
Hugepagesize:       2048 kB   
DirectMap4k:      199616 kB   
DirectMap2M:     9113600 kB   
DirectMap1G:     7340032 kB"""

        memory._parse_meminfo()

        self.assertEqual(memory.mem_total, 16306452)
        self.assertEqual(memory.swap_total, 16654332)

        self.assertEqual(memory.mem_percentage, 64)
        self.assertEqual(memory.swap_percentage, 0)
