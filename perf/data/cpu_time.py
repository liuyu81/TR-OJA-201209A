#!/usr/bin/env python
#
# takes a stime / rtime output file as standard input, and write the
# <id> and <cpu> of each run instance to standard output
#

import os
import sys
import re

CPU_TIME_RE = re.compile(r"(?:cpu:\s)([0-9.]+)(?:.*)")

line = sys.stdin.readline()
while line:
    m = re.match(CPU_TIME_RE, line)
    if m:
        sys.stdout.write(m.group(1))
    sys.stdout.write('\n')
    line = sys.stdin.readline()

