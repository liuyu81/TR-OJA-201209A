#!/usr/bin/sudo python
from sandbox import *
s = Sandbox(["./foo/fopen.exe", "data.in"], jail="foo", owner="nobody")
s.run()
