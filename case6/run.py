#!/usr/bin/env python
from posix import O_RDONLY
from platform import machine
from sandbox import *

if machine() not in ('x86_64', 'i686'):
    raise AssertionError("Unsupported platform type.\n")

symbol = dict((getattr(Sandbox, 'S_RESULT_%s' % i), i) for i in \
    ('PD', 'OK', 'RF', 'RT', 'TL', 'ML', 'OL', 'AT', 'IE', 'BP'))

class SelectiveOpen(SandboxPolicy):
    SC_open = (2, 0) if machine() == 'x86_64' else (5, 0)
    def __init__(self, sbox):
        assert(isinstance(sbox, Sandbox))
        self.sbox = sbox
    def __call__(self, e, a):
        if e.type == S_EVENT_SYSCALL:
            if (e.data, e.ext0) == self.SC_open:
                return self.SYS_open(e, a)
        return super(SelectiveOpen, self).__call__(e, a)
    def SYS_open(self, e, a):
        path, mode = self.sbox.dump(T_STRING, e.ext1), e.ext2
        if path == b"./data.in" and mode == O_RDONLY:
            return SandboxAction(S_ACTION_CONT)
        return SandboxAction(S_ACTION_KILL, S_RESULT_RF)
    pass

s = Sandbox(["./fopen.exe", "./data.in"])
s.policy = SelectiveOpen(s)
s.run()

print("result: %s" % symbol.get(s.result, 'NA'))

