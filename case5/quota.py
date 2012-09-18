#!/usr/bin/env python
import sys
from sandbox import *

class RelaxMemoryQuota(SandboxPolicy):
    def __init__(self, sbox, limit):
        assert(isinstance(sbox, Sandbox))
        self.parent = sbox
        self.soft_limit = limit / 1024
        pass
    def __call__(self, e, a):
        if e.type == S_EVENT_QUOTA and e.data == S_QUOTA_MEMORY:
            vm, vm_peak = self.parent.probe(False)['mem_info'][:2]
            if vm_peak < self.soft_limit:
                return SandboxAction(S_ACTION_CONT)
            return SandboxAction(S_ACTION_KILL, S_RESULT_ML)
        return super(RelaxMemoryQuota, self).__call__(e, a)
    pass

s = Sandbox("./malloc.exe", quota=dict(memory=2**21))
s.policy=RelaxMemoryQuota(s, 2**23)
s.run()

