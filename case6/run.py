#!/usr/bin/env python
#
# @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
# @author LIU Yu <pineapple.liu@gmail.com>
# @date 2012/10/06
#
# This program source code is part of the OpenJudge Alliance Technical Report
# (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
#

from posix import O_RDONLY
from platform import system, machine
from sandbox import *

if system() not in ('Linux', ) or machine() not in ('x86_64', 'i686', ):
    raise AssertionError("Unsupported platform type.\n")

class SelectiveOpenPolicy(SandboxPolicy):
    SC_open = ((2, 0), (5, 1)) if machine() == 'x86_64' else (5, )
    def __init__(self, sbox):
        assert(isinstance(sbox, Sandbox))
        self.sbox = sbox
    def __call__(self, e, a):
        if e.type == S_EVENT_SYSCALL:
            sc = (e.data, e.ext0) if machine() == 'x86_64' else e.data
            if sc in self.SC_open:
                return self.SYS_open(e, a)
        return super(SelectiveOpenPolicy, self).__call__(e, a)
    def SYS_open(self, e, a):
        path, mode = self.sbox.dump(T_STRING, e.ext1), e.ext2
        if path is None:  # e.ext1 is an invalid address
            return SandboxAction(S_ACTION_KILL, S_RESULT_RT)
        if path == b"./data.in" and mode == O_RDONLY:
            return SandboxAction(S_ACTION_CONT)
        return SandboxAction(S_ACTION_KILL, S_RESULT_RF)
    pass

result_name = dict((getattr(Sandbox, 'S_RESULT_%s' % i), i) for i in \
    ('PD', 'OK', 'RF', 'RT', 'TL', 'ML', 'OL', 'AT', 'IE', 'BP'))

if __name__ == '__main__':
    s = Sandbox(["./fopen.exe", "./secret.in"])
    s.policy = SelectiveOpenPolicy(s)
    s.run()
    print("result: %s" % result_name.get(s.result, 'NA'))

