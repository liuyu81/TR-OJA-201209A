/**
 * @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
 * @author LIU Yu <pineapple.liu@gmail.com>
 * @date 2012/04/30
 * 
 * This program source code is part of the OpenJudge Alliance Technical Report
 * (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <memory.h>
#include <errno.h>

int main(int argc, char * argv[])
{
  unsigned long long BLOCK_SIZE = 1048586; /* 1MB */
  char * ptr = NULL;
  unsigned long i = 0;
  while (1)
  {
    if ((ptr = (char*)malloc(BLOCK_SIZE)) != NULL)
    {
      fprintf(stderr, "%llu kB\n", (++i) * BLOCK_SIZE / 1024);
      memset(ptr, 0, BLOCK_SIZE);
    }
    else
    {
      fprintf(stderr, "Failed to allocate memory: %s.\n", strerror(errno));
    }
    fflush(stderr);
  }
  return 0;
}
