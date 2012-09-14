#

.PHONY: all clean

TARGETS = case1/hello.exe case2/malloc.exe case3/foo/fopen.exe case5/hello.exe

all: $(TARGETS)
	chmod 0600 case3/secret.in

clean:
	rm -f $(TARGETS)
	rm -rf $(TARGETS:.exe=.exe.dSYM)

%.exe: %.c
	$(CC) -Wall -O1 -ansi -o $(@) $(<)
