/**
 * @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
 * @author LIU Yu <pineapple.liu@gmail.com>
 * @date 2012/10/06
 * 
 * This program source code is part of the OpenJudge Alliance Technical Report
 * (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
 */

/* check platform type */
#if !defined(__linux__) || (!defined(__x86_64__) && !defined(__i386__))
#error "Unsupported platform type"
#endif /**/

#ifndef PROG_NAME
#define PROG_NAME "slimit.exe"
#endif /* PROG_NAME */

#include <stdio.h>
#include <stdlib.h>
#include <sysexits.h>
#include <unistd.h>
#include <sandbox.h>

typedef enum {P_ELAPSED = 0, P_CPU = 1, P_MEMORY = 2, } probe_t;
res_t probe(const sandbox_t*, probe_t);

int 
main(int argc, const char* argv[])
{
    if (argc < 3)
    {
        fprintf(stderr, "synopsis: " PROG_NAME " foo/bar.exe CPU [arg1 [...]]\n");
        return EX_USAGE;
    }
    /* create and configure a sandbox instance */
    sandbox_t sbox;
    if (sandbox_init(&sbox, &argv[2]) != 0)
    {
        fprintf(stderr, "sandbox initialization failed\n");
        return EX_DATAERR;
    }
    sbox.task.quota[S_QUOTA_CPU] = atol(argv[1]) * 1000;
    /* execute till end */
    if (!sandbox_check(&sbox))
    {
        fprintf(stderr, "sandbox pre-execution state check failed\n");
        return EX_DATAERR;
    }
    sandbox_execute(&sbox);
    /* verbose statistics */
    fprintf(stderr, "cpu: %.3lf ms\n", (double)probe(&sbox, P_CPU) / 1000.);
    /* destroy sandbox instance */
    sandbox_fini(&sbox);
    return EX_OK;
}

/* struct timespec to msec conversion */
static unsigned long
ts2ms(struct timespec ts)
{
    return ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

res_t 
probe(const sandbox_t* psbox, probe_t key)
{
    switch (key)
    {
    case P_ELAPSED:
        return ts2ms(psbox->stat.elapsed);
    case P_CPU:
        return ts2ms(psbox->stat.cpu_info.clock);
    case P_MEMORY:
        return psbox->stat.mem_info.vsize_peak / 1024;
    default:
        break;
    }
    return 0;
}

