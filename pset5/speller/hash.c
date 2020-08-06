
/* http://www.cs.yale.edu/homes/aspnes/pinewiki/C(2f)HashTables.html */

#define MULTIPLIER (37)

unsigned long
hash(const char *s)
{
    unsigned long h;
    unsigned const char *us;

    /* cast s to unsigned const char * */
    /* this ensures that elements of s will be treated as having values >= 0 */
    us = (unsigned const char *) s;

    h = 0;
    while (*us != '\0')
    {
        h = h * MULTIPLIER + *us;
        us++;
    }

    return h;
}