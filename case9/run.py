#!/usr/bin/env python
#
# @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
# @author LIU Yu <pineapple.liu@gmail.com>
# @date 2012/10/06
#
# This program source code is part of the OpenJudge Alliance Technical Report
# (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
#

from ctypes import Structure, sizeof
from ctypes import c_uint32, c_uint64, c_int32, c_int64, c_int
from platform import system, machine
from sandbox import *

# check platform type
if system() not in ('Linux', ) or machine() not in ('x86_64', 'i686', ):
    raise AssertionError("Unsupported platform type.\n")

# sandbox with (partial) support for predictive out-of-quota (output) detection
class PredictiveOutputQuotaSandbox(SandboxPolicy,Sandbox):
    def __init__(self, *args, **kwds):
        # Linux system calls for fd write
        if machine() == 'x86_64': # x86_64 (multiarch) system calls
            x86_64, i686 = 0, 1
            SC_write = ((1, x86_64), (4, i686), )
            SC_pwrite64 = ((18, x86_64), (181, i686), )
            SC_writev = ((20, x86_64), (146, i686), )
            SC_pwritev = ((296, x86_64), (334, i686), )
        else: # i686 system calls
            SC_write = (4, )
            SC_pwrite64 = (181, )
            SC_writev = (146, )
            SC_pwritev = (334, )
        # table of system call rules
        self.sc_table = {}
        for entry, handler in zip((SC_write, SC_pwrite64, SC_writev, SC_pwritev), \
            (self.SYS_write, self.SYS_write, self.SYS_writev, self.SYS_writev)):
            for sc in entry:
                self.sc_table[sc] = handler
        # policy internal states
        self.written_bytes = 0
        self.pending_bytes = 0
        # initalize as a polymorphic sandbox-and-policy object
        SandboxPolicy.__init__(self)
        Sandbox.__init__(self, *args, **kwds)
        self.policy = self
        pass
    def probe(self):
        # add custom entries into the probe dict
        d = Sandbox.probe(self, False)
        d['out'] = (self.written_bytes, self.written_bytes + self.pending_bytes)
        return d
    def __call__(self, e, a):
        # handle SYSCALL/SYSRET events with local rules
        if e.type in (S_EVENT_SYSCALL, S_EVENT_SYSRET):
            sc = (e.data, e.ext0) if machine() == 'x86_64' else e.data
            if sc in self.sc_table:
                return self.sc_table[sc](e, a)
        # bypass other events to base class
        return SandboxPolicy.__call__(self, e, a)
    def SYS_write(self, e, a): # write / pwrite64
        abi64 = (machine() == 'x86_64' and e.ext0 == 0)
        ssize_t, size_t = (c_int64, c_uint64) if abi64 else (c_int32, c_uint32)
        if e.type == S_EVENT_SYSCALL:
            self.pending_bytes = size_t(e.ext3).value
        else:
            if ssize_t(e.ext1).value > 0:
                self.written_bytes += ssize_t(e.ext1).value
            self.pending_bytes = 0
        return self._output_check(e, a)
    def SYS_writev(self, e, a): # writev / pwritev
        abi64 = (machine() == 'x86_64' and e.ext0 == 0)
        ssize_t = c_int64 if abi64 else c_int32
        if e.type == S_EVENT_SYSCALL:
            address, iovcnt = e.ext2, c_int(e.ext3).value
            self.pending_bytes = 0
            for i in range(iovcnt):
                iovec = self._dump_iovec(abi64, address)
                self.pending_bytes += iovec.iov_len
                address += sizeof(iovec)
        else:
            if ssize_t(e.ext1).value > 0:
                self.written_bytes += ssize_t(e.ext1).value
            self.pending_bytes = 0
        return self._output_check(e, a)
    def _dump_iovec(self, abi64, address):
        # dump a struct iovec object from the given address
        typeid = T_ULONG if abi64 else T_UINT
        size_t, char_p = (c_uint64, ) * 2 if abi64 else (c_uint32, ) * 2
        # from manpage writev(2)
        class struct_iovec(Structure):
             _fields_ = [('iov_base', char_p), ('iov_len', size_t), ]
        return struct_iovec(self.dump(typeid, address), \
            self.dump(typeid, address + sizeof(char_p)))
    def _output_check(self, e, a):
        # compare current written + pending bytes against the quota
        if self.written_bytes + self.pending_bytes > self.quota[3]:
            return self._KILL_OL(e, a)
        return self._CONT(e, a)
    def _CONT(self, e, a): # continue
        a.type = S_ACTION_CONT
        return a
    def _KILL_RF(self, e, a): # restricted func.
        a.type, a.data = S_ACTION_KILL, S_RESULT_RF
        return a
    def _KILL_OL(self, e, a): # disk output limit exceeded
        a.type, a.data = S_ACTION_KILL, S_RESULT_OL
        return a
    pass

result_name = dict((getattr(Sandbox, 'S_RESULT_%s' % i), i) for i in \
    ('PD', 'OK', 'RF', 'RT', 'TL', 'ML', 'OL', 'AT', 'IE', 'BP'))

if __name__ == '__main__':
    s = PredictiveOutputQuotaSandbox("./write.exe", quota=dict(disk=64))
    s.run()
    print("result: %s" % result_name.get(s.result, 'NA'))
    print("out: %dB / %dB" % s.probe()['out']) # written / predicted

