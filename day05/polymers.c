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

int react(const char* input, char* output, int input_len, FILE* verbose)
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
    // fprintf(verbose, "copying [%d:%d]\n", 0, reaction_idx);
    for (i = 0; i < reaction_idx; i++) {
        output[opos] = input[i];
        opos++;
    }
    // fprintf(verbose, "copying [%d:%d]\n", reaction_idx + 2, input_len);
    for (i = reaction_idx + 2; i < input_len; i++) {
        output[opos] = input[i];
        opos++;
    }
    postilen = strnlen(input, INPUT_LEN_MAX);
    postolen = strnlen(output, INPUT_LEN_MAX);
    // fprintf(verbose, "opos = %d, input[%d], output[%d]\n", opos, postilen, postolen);
    if (postilen == postolen) {
        fprintf(stderr, "a reaction happened, but the output string length %d equals input string length\n", postilen);
        abort();
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

FILE* open_verbose_output(const int argc, char* argv[])
{
    int i;
    if (argc > 1) {
        for (i = 1; i < argc; i++) {
            if (strncmp(argv[i], "-v", 2) == 0) {
                return stderr;
            }
        }
    }
    return fopen("/dev/null", "r");
}

int main(int argc, char* argv[])
{
    char input[INPUT_LEN_MAX];
    char output[INPUT_LEN_MAX] = {0};
    int nchars;
    int nreactions;
    int retval;
    FILE* verbose;
    FILE* input_file = stdin;
    verbose = open_verbose_output(argc, argv);
    fgets(input, INPUT_LEN_MAX, input_file);
    rstrip(input, INPUT_LEN_MAX);
    nchars = strnlen(input, INPUT_LEN_MAX);
    if (nchars < 0) {
        fprintf(stderr, "failed to read input\n");
        retval = 1;
    } else {
        fprintf(verbose, "read %d bytes from input\n", nchars);
        do {
            nchars = strnlen(input, INPUT_LEN_MAX);
            nreactions = react(input, output, nchars, verbose);
            fprintf(verbose, "%s -> %s\n", input, output);
            memset(input, '\0', INPUT_LEN_MAX);
            strncpy(input, output, nchars);
        } while (nreactions > 0);
        fprintf(stdout, "%s\n", output);
        fclose(input_file);
        retval = 0;
    } 
    return retval;
}