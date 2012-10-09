#!/usr/bin/env python
#
# @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
# @author LIU Yu <pineapple.liu@gmail.com>
# @date 2012/10/06
#
# This program source code is part of the OpenJudge Alliance Technical Report
# (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
#

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
