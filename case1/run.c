/*
 * @copyright (c) 2013, OpenJudge Alliance <http://openjudge.net>
 * @author LIU Yu <pineapple.liu@gmail.com>
 * @date 2013/01/29
 *
 * This program source code is part of the OpenJudge Alliance Technical Report
 * (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
 */

#include <stdio.h>
#include <assert.h>
#include <sandbox.h>

void sandbox_probe(sandbox_t *);

int
main(void)
{
    const char * comm[] = {"./hello.exe", NULL, };
    sandbox_t sbox;
    sandbox_init(&sbox, comm);
    sandbox_execute(&sbox);
    sandbox_probe(&sbox);
    sandbox_fini(&sbox);
    return 0;
}

void
sandbox_probe(sandbox_t * psbox)
{
    assert(psbox);
    printf("result: %s\n", (psbox->result == S_RESULT_OK) ? "OK" : "N/A");
}

