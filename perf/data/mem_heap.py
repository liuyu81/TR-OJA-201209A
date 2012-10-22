#!/usr/bin/env python
#
# takes a Valgrind massif output file as standard input, and write the
# <mem_heap> of each snapshot to standard output
#

import os
import sys
from msparser import parse

d = parse(sys.stdin)
print(d)
for s in d['snapshots']:
    sys.stdout.write('%(mem_heap)d\n' % s)

