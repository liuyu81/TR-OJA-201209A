#!/usr/bin/env python

import sys
from sandbox import *

if len(sys.argv) < 3:
    sys.stderr.write("synopsis: python slimit.py CPU foo/bar.exe [arg1 [...]]\n")
    sys.exit(1)

cpu = 1000 * int(sys.argv[1])
s = Sandbox(sys.argv[2:], quota={'cpu': cpu})
s.run()

time = float(s.probe()['cpu_info'][0])
sys.stderr.write("cpu: %.3f sec\n" % (time / 1000))
