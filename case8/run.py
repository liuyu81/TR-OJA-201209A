#!/usr/bin/env python

from platform import system, machine
from sandbox import *

# check platform type
if system() not in ('Linux', ) or machine() not in ('x86_64', 'i686', ):
    raise AssertionError("Unsupported platform type.\n")

# sandbox with (partial) support for predictive out-of-quota (memory) detection
class PredictiveQuotaSandbox(SandboxPolicy,Sandbox):
    result_name = dict((getattr(Sandbox, 'S_RESULT_%s' % i), i) for i in \
        ('PD', 'OK', 'RF', 'RT', 'TL', 'ML', 'OL', 'AT', 'IE', 'BP'))
    # system calls for memory-allocation
    SC_brk = (12, 0) if machine() == 'x86_64' else (45, 0)
    SC_mmap = (9, 0) if machine() == 'x86_64' else (90, 0)
    SC_mremap = (25, 0) if machine() == 'x86_64' else (163, 0)
    def __init__(self, *args, **kwds):
        # initalize as a polymorphic sandbox-and-policy object
        assert(not 'policy' in kwds)
        SandboxPolicy.__init__(self)
        Sandbox.__init__(self, *args, **kwds)
        self.policy = self
        # initialize table of system call rules
        self.sc_table = {self.SC_brk: self.SYS_brk, self.SC_mmap: \
            self.SYS_mmap, self.SC_mremap: self.SYS_mremap}
        # initialize policy states
        self.data_seg_end = 0 # data segment end address
        self.pending_alloc = 0 # pending memory allocation (kB)
    def probe(self):
        # add custom entries into the probe dict
        d = Sandbox.probe(self, False)
        d['cpu'] = d['cpu_info'][0]
        d['mem'] = (d['mem_info'][1], d['mem_info'][0] + self.pending_alloc)
        d['result'] = self.result_name.get(self.result, 'NA')
        return d
    def __call__(self, e, a):
        # handle SYSCALL/SYSRET events with local rules
        if e.type in (S_EVENT_SYSCALL, S_EVENT_SYSRET):
            sc = (e.data, e.ext0 if machine() == 'x86_64' else 0)
            if sc in self.sc_table:
                return self.sc_table[sc](e, a)
        # bypass other events to base class
        return SandboxPolicy.__call__(self, e, a)
    def MEM_check(self, e, a, incr=0):
        # compare current mem usage (incl. pending alloc) against quota
        self.pending_alloc = incr / 1024
        if max(self.probe()['mem']) * 1024 > self.quota[2]:
            return self._KILL_ML(e, a)
        return self._CONT(e, a)
    def SYS_brk(self, e, a):
        if e.type == S_EVENT_SYSCALL:
            # pending data segment increment
            if e.ext1 > 0:
                incr = e.ext1 - self.data_seg_end
                return self.MEM_check(e, a, incr)
        else:
            # update data segment end address
            self.data_seg_end = e.ext1
        return self.MEM_check(e, a)
    def SYS_mmap(self, e, a):
        PROT_READ = 0x01        # <bits/mman.h>
        PROT_WRITE = 0x02       # <bits/mman.h>
        if e.type == S_EVENT_SYSCALL:
            # pending memory map area size
            if (e.ext1, e.ext3, e.ext4) == (0, PROT_READ | PROT_WRITE, -1):
                return self.MEM_check(e, a, e.ext2)
            return self._KILL_RF(e, a)
        return self.MEM_check(e, a)
    def SYS_mremap(self, e, a):
        # TODO: incr = newsize - oldsize
        return self.MEM_check(e, a)
    def _CONT(self, e, a): # continue
        a.type = S_ACTION_CONT
        return a
    def _KILL_RF(self, e, a): # restricted func.
        a.type, a.data = S_ACTION_KILL, S_RESULT_RF
        return a
    def _KILL_ML(self, e, a): # mem limit exceeded
        a.type, a.data = S_ACTION_KILL, S_RESULT_ML
        return a
    pass

if __name__ == '__main__':
    s = PredictiveQuotaSandbox("./malloc.exe", quota=dict(memory=2**22))
    s.run()
    print("result: %(result)s\ncpu: %(cpu)dms" % s.probe())
    print("mem: %dkB / %dkB" % s.probe()['mem'])
