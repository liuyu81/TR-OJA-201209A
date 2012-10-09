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

class RelaxMemoryPolicy(SandboxPolicy):
    def __init__(self, sbox, factor):
        assert(isinstance(sbox, Sandbox))
        self.parent = sbox
        self.limit = factor * sbox.quota[2] / 1024
        pass
    def __call__(self, e, a):
        if e.type == S_EVENT_QUOTA and e.data == S_QUOTA_MEMORY:
            vm, vm_peak = self.parent.probe(False)['mem_info'][:2]
            if vm_peak < self.limit:
                return SandboxAction(S_ACTION_CONT)
            return SandboxAction(S_ACTION_KILL, S_RESULT_ML)
        return super(RelaxMemoryPolicy, self).__call__(e, a)
    pass

result_name = dict((getattr(Sandbox, 'S_RESULT_%s' % i), i) for i in \
    ('PD', 'OK', 'RF', 'RT', 'TL', 'ML', 'OL', 'AT', 'IE', 'BP'))

if __name__ == '__main__':
    s = Sandbox("./malloc.exe", quota=dict(memory=2**22))
    s.policy = RelaxMemoryPolicy(s, 2.0)
    s.run()
    print("result: %s" % result_name.get(s.result, 'NA'))

