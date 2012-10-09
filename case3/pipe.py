#!/usr/bin/sudo python
#
# @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
# @author LIU Yu <pineapple.liu@gmail.com>
# @date 2012/10/06
#
# This program source code is part of the OpenJudge Alliance Technical Report
# (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
#

from os import pipe
from subprocess import Popen
from sandbox import *

f_rd, f_wr = pipe()
p = Popen("/bin/cat", stdin=f_rd)
s = Sandbox("./foo/fopen.exe", jail="./foo", owner="nobody", \
    stdin=open("./data.in", "r"), stdout=f_wr)
s.run()

