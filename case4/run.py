#!/usr/bin/env python
#
# @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
# @author LIU Yu <pineapple.liu@gmail.com>
# @date 2012/10/06
#
# This program source code is part of the OpenJudge Alliance Technical Report
# (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
#

from sandbox import *

class VerbosePolicy(SandboxPolicy):
    symbol = dict((getattr(SandboxEvent, "S_EVENT_%s" % i), i) \
        for i in ('SYSCALL', 'SYSRET', 'SIGNAL', 'QUOTA', 'EXIT', 'ERROR'))
    def __call__(self, e, a):
        print("event: %s" % VerbosePolicy.symbol[e.type])
        return super(VerbosePolicy, self).__call__(e, a)
    pass

if __name__ == '__main__':
    s = Sandbox("./hello.exe", policy=VerbosePolicy())
    s.run()


