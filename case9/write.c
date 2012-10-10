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
#include <sys/uio.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
  const char buff[] = "Hello World!\n";
  struct iovec vect[] = {
    (struct iovec){&buff, strlen(buff)},
    (struct iovec){&buff, strlen(buff)},
    (struct iovec){&buff, strlen(buff)},
  };
  printf("Hello World!\n");
  write(STDOUT_FILENO, buff, strlen(buff));
  writev(STDERR_FILENO, &vect[0], sizeof(vect) / sizeof(struct iovec));
  return 0;
}