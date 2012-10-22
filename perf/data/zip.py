#!/usr/bin/env python
import os
import os.path
import sys
from subprocess import Popen, PIPE
import glob
import urllib

if len(sys.argv) < 2:
    sys.stderr.write("synopsis: python " + __file__ + " filter file1 [...]\n")
    sys.exit(os.EX_USAGE)

DAT = {}

for regex in sorted(sys.argv[2:]):
    for fn in sorted(glob.glob(regex)):
        if not fn in DAT:
            DAT[fn] = []
        p = Popen(sys.argv[1], stdin=open(fn), stdout=PIPE)
        f = p.stdout
        line = f.readline()
        while line.strip():
            tup = line.split(" ")
            v = tup[0] if isinstance(tup, tuple) and len(tup) == 1 \
                else (str(i).strip() for i in tup)
            DAT[fn].append(v)
            line = f.readline()

def fn2label(fn):
    return urllib.quote('.'.join(os.path.basename(fn).split('.')[:-1]))

prefix = os.path.commonprefix(DAT.keys()) if len(DAT) > 1 else ''
head = map(lambda x: fn2label(x.lstrip(prefix)), DAT.keys())

sys.stdout.write(' '.join(head))
sys.stdout.write('\n')

for vect in zip(*DAT.values()):
    for tup in vect:
        for item in tup:
            sys.stdout.write(str(item))
            sys.stdout.write(' ')
    sys.stdout.write('\n')
