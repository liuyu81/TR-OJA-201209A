/**
 * @copyright (c) 2012, OpenJudge Alliance <http://openjudge.net>
 * @author LIU Yu <pineapple.liu@gmail.com>
 * @date 2012/10/06
 *
 * This program source code is part of the OpenJudge Alliance Technical Report
 * (TR-OJA-201209A) at <http://openjudge.net/TR/201209A>.
 */

int incr(int i)
{
    return i + 1;
}

int main(int argc, char * argv[])
{
    int i = 0;
    while (1)
    {
        i = incr(i);
    }
    return 0;
}

