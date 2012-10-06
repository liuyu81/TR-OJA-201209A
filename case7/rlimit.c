#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h> 
#include <sys/time.h> 
#include <sys/wait.h>
#include <time.h>
#include <unistd.h> 

int 
main (int argc, char* argv[]) 
{
  if (argc < 3)
  {
    fprintf(stderr, "synopsis: rlimit.exe CPU foo/bar.exe [arg1 [...]]\n");
    return 1;
  }
  pid_t pid = fork();
  if (pid == 0)
  {
    /* Obtain current CPU limit. */ 
    struct rlimit rl;
    getrlimit(RLIMIT_CPU, &rl); 
    /* Set CPU limit. */
    rl.rlim_cur = atol(argv[1]);
    setrlimit(RLIMIT_CPU, &rl);
    execve(argv[2], &argv[2], NULL);
    return 1;
  }
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
    double time = (ru.ru_utime.tv_sec + ru.ru_stime.tv_sec) * 1000 + \
        (ru.ru_utime.tv_usec + ru.ru_stime.tv_usec) / 1000;
    fprintf(stderr, "cpu: %.3lf\n", time / 1000);
    return 0;
  }
  else
  {
    fprintf(stderr, "%s\n", strerror(errno));
    return 2;
  }
}

