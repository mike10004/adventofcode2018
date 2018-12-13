#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define INPUT_LEN_MAX 65536

int is_lower(char ch)
{
    return (ch >= 'a') && (ch <= 'z');
}

int is_upper(char ch)
{
    return (ch >= 'A') && (ch <= 'Z');
}

int is_same_type(char a, char b)
{
    return tolower(a) == tolower(b);
}

int is_same_polarity(char a, char b)
{
    return (is_lower(a) && is_lower(b)) || (is_upper(a) && is_upper(b));
}

int is_reactive(char a, char b)
{
    return is_same_type(a, b) && !is_same_polarity(a, b);
}

int react(const char* input, char* output, int input_len)
{
    int i;
    char a;
    char b;
    int opos = 0;
    int reaction_idx = -1;
    int postilen, postolen;
    memset(output, '\0', INPUT_LEN_MAX);
    for (i = 0; i < (input_len - 1); i++) {
        a = input[i];
        b = input[i + 1];
        if (is_reactive(a, b)) {
            reaction_idx = i;
            break;
        }
    }
    if (reaction_idx == -1) {
        strncpy(output, input, input_len);
        return 0;
    }
    for (i = 0; i < reaction_idx; i++) {
        output[opos] = input[i];
        opos++;
    }
    for (i = reaction_idx + 2; i < input_len; i++) {
        output[opos] = input[i];
        opos++;
    }
    return 1;
}

void rstrip(char* str, const int maxlen)
{
    int i;
    for (i = maxlen - 1; i >= 0; i--) {
        if (str[i] != '\0') {
            if (isspace(str[i])) {
                str[i] = '\0';
            } else {
                break;
            }            
        }
    }
}

int main(int argc, char* argv[])
{
    char input[INPUT_LEN_MAX];
    char output[INPUT_LEN_MAX] = {0};
    int nchars;
    int nreactions;
    int retval;
    FILE* input_file = stdin;
    fgets(input, INPUT_LEN_MAX, input_file);
    rstrip(input, INPUT_LEN_MAX);
    nchars = strnlen(input, INPUT_LEN_MAX);
    if (nchars < 0) {
        fprintf(stderr, "failed to read input\n");
        retval = 1;
    } else {
        fprintf(stderr, "%d chars in input\n", nchars);
        do {
            nchars = strnlen(input, INPUT_LEN_MAX);
            nreactions = react(input, output, nchars);
            memset(input, '\0', INPUT_LEN_MAX);
            strncpy(input, output, nchars);
        } while (nreactions > 0);
        fprintf(stdout, "%s\n", output);
        fprintf(stderr, "%lu chars in output\n", strnlen(output, INPUT_LEN_MAX));
        retval = 0;
    } 
    return retval;
}