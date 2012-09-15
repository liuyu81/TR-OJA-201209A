#!/usr/bin/sudo python
from os import pipe
from subprocess import Popen
from sandbox import *
f_rd, f_wr = pipe()
p = Popen("/bin/cat", stdin=f_rd)
s = Sandbox("./foo/fopen.exe", jail="./foo", owner="nobody", \
    stdin=open("./data.in", "r"), stdout=f_wr)
s.run()

