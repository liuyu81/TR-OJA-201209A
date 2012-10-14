#!/usr/bin/env python
#
# @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
# @author LIU Yu <pineapple.liu@gmail.com>
# @date 2012/10/06
# 
# This program source code is part of the OpenJudge Alliance Technical Report
# (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
#

import os
import sys

if len(sys.argv) < 3:
    sys.stderr.write("python run.py N cmd [arg1 [...]]\n")
    sys.exit(os.EX_USAGE)

REPEAT = int(sys.argv[1])

nfail = 0
for i in range(REPEAT):
    if os.system(" ".join(sys.argv[2:])):
        nfail += 1

if nfail > 0:
    sys.stdout.write("----------\n")
    sys.stdout.write("failed %d cases\n" % nfail)
    sys.exit(nfail)

sys.exit(os.EX_OK)

