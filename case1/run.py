#!/usr/bin/env python
from sandbox import *
s = Sandbox("./hello.exe")
s.run()
s.result == S_RESULT_OK
s.probe()

