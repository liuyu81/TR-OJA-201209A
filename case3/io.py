#!/usr/bin/sudo python
from sandbox import *
s = Sandbox("./foo/fopen.exe", jail="./foo", owner="nobody", stdin=open("secret.in"))
s.run()
