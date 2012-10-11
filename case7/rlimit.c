/**
 * @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
 * @author LIU Yu <pineapple.liu@gmail.com>
 * @date 2012/10/06
 * 
 * This program source code is part of the OpenJudge Alliance Technical Report
 * (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
 */

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sysexits.h>
#include <sys/resource.h> 
#include <sys/time.h> 
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#ifndef PROG_NAME
#define PROG_NAME "rlimit.exe"
#endif /* PROG_NAME */

/* struct timeval to msec conversion */
static unsigned long
tv2ms(struct timeval tv)
{
    return tv.tv_sec * 1000 + tv.tv_usec / 1000;
}

int 
main (int argc, char* argv[]) 
{
  if (argc < 3)
  {
    fprintf(stderr, "synopsis: rlimit.exe CPU foo/bar.exe [arg1 [...]]\n");
    return EX_USAGE;
  }
  pid_t pid = fork();
  /* child process */
  if (pid == 0)
  {
    /* obtain current CPU limit. */ 
    struct rlimit rl;
    getrlimit(RLIMIT_CPU, &rl); 
    /* set soft CPU limit (which triggers SIGXCPU) */
    rl.rlim_cur = atol(argv[1]);
    setrlimit(RLIMIT_CPU, &rl);
    /* execute till end */
    execve(argv[2], &argv[2], NULL);
    /* execve() does not return unless failed */
    fprintf(stderr, "%s\n", strerror(errno));
    return EX_DATAERR;
  }
  /* supervisor process */
  else if (pid > 0)
  {
    int status = 0;
    struct rusage ru;
    while (waitpid(pid, &status, 0) > 0)
    {
        getrusage(RUSAGE_CHILDREN, &ru);
        if (WIFEXITED(status) || WIFSIGNALED(status))
        {
            break;
        }
    };
    /* verbose statistics */
    double time = tv2ms(ru.ru_utime) + tv2ms(ru.ru_stime);
    fprintf(stderr, "cpu: %.3lf sec\n", time / 1000.);
    return EX_OK;
  }
  else
  {
    fprintf(stderr, "%s\n", strerror(errno));
    return EX_OSERR;
  }
}

