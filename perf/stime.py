#!/usr/bin/env python

import os
import sys
from sandbox import *

if len(sys.argv) < 3:
    sys.stderr.write("synopsis: python " + __file__ + " foo/bar.exe CPU [arg1 [...]]\n")
    sys.exit(os.EX_USAGE)

s = Sandbox(sys.argv[2:], stdout=sys.stdout, stderr=sys.stderr, quota=dict(cpu=int(sys.argv[1])))
s.run()

time = float(s.probe()['cpu_info'][0]) / 1000
sys.stdout.write("cpu: %.3f sec\n" % time);

sys.exit(os.EX_OK)

