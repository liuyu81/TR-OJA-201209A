#!/usr/bin/env python
from posix import O_RDONLY
from platform import machine as arch
from sandbox import *

if arch() not in ('x86_64', 'i686'):
    raise AssertionError("Unsupported platform type.\n")

symbol = dict((getattr(Sandbox, 'S_RESULT_%s' % i), i) for i in \
    ('PD', 'OK', 'RF', 'RT', 'TL', 'ML', 'OL', 'AT', 'IE', 'BP'))

class PredictiveQuotaPolicy(SandboxPolicy):
    # system calls for memory-allocation
    SC_brk = (12, 0) if arch() == 'x86_64' else (45, 0)
    SC_mmap = (9, 0) if arch() == 'x86_64' else (90, 0)
    SC_mremap = (25, 0) if arch() == 'x86_64' else (163, 0)
    def __init__(self, sbox):
        assert(isinstance(sbox, Sandbox))
        self.sbox = sbox
        self.data_segment_end = 0 # data segment end address
        self.pending_alloc = 0 # pending memory allocation in byte
        self.sc_table = {self.SC_brk: self.SYS_brk, \
            self.SC_mmap: self.SYS_mmap, self.SC_mremap: self.SYS_mremap}
        pass
    def __call__(self, e, a):
        if e.type in (S_EVENT_SYSCALL, S_EVENT_SYSRET):
            sc = (e.data, e.ext0 if arch() == 'x86_64' else 0)
            if sc in self.sc_table:
                return self.sc_table[sc](e, a)
        return super(PredictiveQuotaPolicy, self).__call__(e, a)
    @property
    def mem(self):
        return (self.sbox.probe()['mem_info'][0] * 1024, self.pending_alloc)
    def MEM_audit(self, e, a, incr=0):
        if sum(self.mem) + incr > self.sbox.quota[2]:
            self.pending_alloc = incr
            return SandboxAction(S_ACTION_KILL, S_RESULT_ML)
        return SandboxAction(S_ACTION_CONT)
    def SYS_brk(self, e, a):
        if e.type == S_EVENT_SYSCALL:
            # pending data segment increment
            if e.ext1 > 0:
                incr = e.ext1 - self.data_segment_end
                return self.MEM_audit(e, a, incr)
        else:
            # update data segment end address
            self.data_segment_end = e.ext1
        return SandboxAction(S_ACTION_CONT)
    def SYS_mmap(self, e, a):
        PROT_READ = 0x01        # <bits/mman.h>
        PROT_WRITE = 0x02       # <bits/mman.h>
        if e.type == S_EVENT_SYSCALL:
            # pending memory map area size
            if (e.ext1, e.ext3, e.ext4) == (0, PROT_READ | PROT_WRITE, -1):
                return self.MEM_audit(e, a, e.ext2)
            return SandboxAction(S_ACTION_KILL, S_RESULT_RF)
        return SandboxAction(S_ACTION_CONT)
    def SYS_mremap(self, e, a):
        # 
        return SandboxAction(S_ACTION_KILL, S_RESULT_RF)
    pass

s = Sandbox("./malloc.exe", quota=dict(memory=2**22))
s.policy = PredictiveQuotaPolicy(s)
s.run()

print("result: %s" % symbol.get(s.result, 'NA'))
print("mem: %d kB / %d kB" % (s.policy.mem[0] / 1024, sum(s.policy.mem) / 1024))
