#!/usr/bin/env python
from sandbox import *
s = Sandbox("./malloc.exe", quota=dict(cpu=3000, memory=2**23))
s.run()
s.result == S_RESULT_ML

