#
# @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
# @author LIU Yu <pineapple.liu@gmail.com>
# @date 2012/10/06
#
# This program source code is part of the OpenJudge Alliance Technical Report
# (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
#

.PHONY: all clean

TARGETS = case1/hello.exe case2/malloc.exe case3/foo/fopen.exe case4/hello.exe case5/malloc.exe case6/fopen.exe case7/malloc.exe case8/write.exe perf/rlimit.exe perf/slimit.exe perf/loop.exe

all: $(TARGETS)
	chmod 0600 case3/secret.in

clean:
	rm -f $(TARGETS)
	rm -rf $(TARGETS:.exe=.exe.dSYM)

perf/slimit.exe: perf/slimit.c
	$(CC) -Wall -O1 -o $(@) $(<) -lsandbox

%.exe: %.c
	$(CC) -Wall -Wno-unused-result -O1 -static -o $(@) $(<)
