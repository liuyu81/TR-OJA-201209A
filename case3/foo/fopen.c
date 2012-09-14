/**
 * @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
 * @author LIU Yu <pineapple.liu@gmail.com>
 * @date 2012/04/30
 * 
 * This program source code is part of the OpenJudge Alliance Technical Report
 * (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
 */
#include <stdio.h>
#include <string.h>
#include <errno.h>

int main(int argc, char * argv[])
{
  FILE * fp = NULL;
  if (argc > 1)
  {
      const char * path = argv[1];
      fp = fopen(path, "r");
      if (fp == NULL)
      {
        fprintf(stderr, "Failed to open file \"%s\": %s.\n", path, strerror(errno));
        return 2;
      }
  }
  else
  {
      /* fallback to standard input stream */
      fp = stdin;
  }
  char a = '\0';
  int r = fscanf(fp, "%c", &a);
  fclose(fp);
  return (r == 1);
}
