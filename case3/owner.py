#!/usr/bin/sudo python
from sandbox import *
s = Sandbox(["./foo/fopen.exe", "secret.in"], owner="nobody")
s.run()
