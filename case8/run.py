#!/usr/bin/env python

from platform import system, machine
from sandbox import *

ostype, arch = system(), machine()
if ostype not in ('Linux', ) or arch not in ('x86_64', 'i686', ):
    raise AssertionError("Unsupported platform type.\n")

symbol = dict((getattr(Sandbox, 'S_RESULT_%s' % i), i) for i in \
    ('PD', 'OK', 'RF', 'RT', 'TL', 'ML', 'OL', 'AT', 'IE', 'BP'))

class PredictiveQuotaSandbox(SandboxPolicy,Sandbox):
    # system calls for memory-allocation
    SC_brk = (12, 0) if arch == 'x86_64' else (45, 0)
    SC_mmap = (9, 0) if arch == 'x86_64' else (90, 0)
    SC_mremap = (25, 0) if arch == 'x86_64' else (163, 0)
    def __init__(self, *args, **kwds):
        # initalize base types
        assert(not 'policy' in kwds)
        SandboxPolicy.__init__(self)
        Sandbox.__init__(self, *args, **kwds)
        self.policy = self
        # initialize members
        self.data_segment_end = 0 # data segment end address
        self.pending_memory = 0 # pending memory allocation (kB)
        self.sc_table = {self.SC_brk: self.SYS_brk, \
            self.SC_mmap: self.SYS_mmap, self.SC_mremap: self.SYS_mremap}
        pass
    def __call__(self, e, a):
        if e.type in (S_EVENT_SYSCALL, S_EVENT_SYSRET):
            sc = (e.data, e.ext0 if arch == 'x86_64' else 0)
            if sc in self.sc_table:
                return self.sc_table[sc](e, a)
        return SandboxPolicy.__call__(self, e, a)
    def probe(self):
        d = Sandbox.probe(self, False)
        mem_info = list(d['mem_info'])
        mem_info.append(self.pending_memory)
        d['mem_info'] = tuple(mem_info)
        return d
    def MEM_audit(self, e, a, incr=0):
        if self.probe()['mem_info'][0] * 1024 + incr > self.quota[2]:
            self.pending_memory = incr / 1024
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

s = PredictiveQuotaSandbox("./malloc.exe", quota=dict(memory=2**22))
s.run()

print("result: %s" % symbol.get(s.result, 'NA'))
m = s.probe()['mem_info']
print("mem: %d kB / %d kB" % (m[0], m[0] + m[-1]))
