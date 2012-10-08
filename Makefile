#

.PHONY: all clean

TARGETS = case1/hello.exe case2/malloc.exe case3/foo/fopen.exe case4/hello.exe case5/malloc.exe case6/fopen.exe case7/rlimit.exe case7/loop.exe case8/malloc.exe

all: $(TARGETS)
	chmod 0600 case3/secret.in

clean:
	rm -f $(TARGETS)
	rm -rf $(TARGETS:.exe=.exe.dSYM)

%.exe: %.c
	$(CC) -Wall -O1 -static -o $(@) $(<)
