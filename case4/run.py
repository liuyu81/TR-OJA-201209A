#!/usr/bin/env python
from sandbox import *

class VerbosePolicy(SandboxPolicy):
    symbol = dict((getattr(SandboxEvent, "S_EVENT_%s" % i), i) \
        for i in ('SYSCALL', 'SYSRET', 'SIGNAL', 'QUOTA', 'EXIT', 'ERROR'))
    def __call__(self, e, a):
        print("event: %s" % VerbosePolicy.symbol[e.type])
        return super(VerbosePolicy, self).__call__(e, a)
    pass

s = Sandbox("./hello.exe", policy=VerbosePolicy())
s.run()

