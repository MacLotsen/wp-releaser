#!/usr/bin/python

import sys, getopt, string

SQL_OUTPUT_LOCATION = 'result.sql'
SQL_PARSED_SCRIPT = ''
SQL_IMPORT_SCRIPT = None
OLD_URL = None
NEW_URL = None

COMMENTING = False
URI_DIFF = None

start_msg = """\
====================
 Wordpress Releaser
====================

Author Erik Nijenhuis
License GNU LGPLv3
"""

help_msg = """\
Usage:  (-s <filename> | --script=<filename>)
        (-n <new_url> | --new-url=<new_url>)
        (-o <old_url> | --old-url=<old_url>)
        (--output=<output_filename>)
"""



def parse_args():
    global SQL_IMPORT_SCRIPT, OLD_URL, NEW_URL, URI_DIFF, SQL_OUTPUT_LOCATION
    opts, args = getopt.getopt(sys.argv[1:], 'hs:n:o:', ['help', 'script=', 'new-url=', 'old-url=', 'output='])
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            print help_msg
            exit(0)
        elif opt in ['-s', '--script']:
            SQL_IMPORT_SCRIPT = open(arg).readlines()
        elif opt in ['-n', '--new-url']:
            NEW_URL = arg
        elif opt in ['-o', '--old-url']:
            OLD_URL = arg
        elif opt == '--output':
            SQL_OUTPUT_LOCATION = arg
    SQL_IMPORT_SCRIPT = SQL_IMPORT_SCRIPT or open(raw_input("Enter sql file location: ")).readlines()
    OLD_URL = OLD_URL or raw_input("Enter old url: ")
    NEW_URL = NEW_URL or raw_input("Enter new url: ")
    URI_DIFF = len(NEW_URL) - len(OLD_URL)


def parse_line(count, value):
    err = Exception("Corrupted stack")
    result = ''
    stack = []
    i = 0
    while i < len(value):
        char = value[i]
        if char in ['(', '{']:
            stack.append([i, char, char])
        else:
            if len(stack) > 0:
                stack[-1][2] += char
            else:
                result += char
            if char in [')', '}']:
                beg, symbol, chunk = stack.pop()
                if not (symbol == '(' and char == ')') and not (symbol == '{' and char == '}'):
                    raise err
                chunk_i = chunk.find(OLD_URL)
                while chunk_i > -1:
                    if symbol == '(':
                        chunk = string.replace(chunk, OLD_URL, NEW_URL, 1)
                    if symbol == '{':
                        tmp_n = ''
                        #find number
                        n_i = chunk_i - 4
                        while chunk[n_i] is not ':':
                            tmp_n = chunk[n_i] + tmp_n
                            n_i -= 1
                        try:
			    n_length = str(int(tmp_n) + URI_DIFF)
                            chunk = chunk[:n_i] + string.replace(chunk[n_i:], tmp_n, n_length, 1)
                            chunk = string.replace(chunk, OLD_URL, NEW_URL, 1)
			except:
			    chunk = string.replace(chunk, OLD_URL, NEW_URL, 1)
                    count -= 1
                    chunk_i = chunk.find(OLD_URL, chunk_i + 1)
                if len(stack) > 0:
                    stack[-1][2] += chunk
                else:
                    result += chunk
        i += 1
    return result + value[i:] + '\n'


def parse_script():
    global SQL_PARSED_SCRIPT
    value_changed_count = 0
    for line in SQL_IMPORT_SCRIPT:
        occurrences = line.count(OLD_URL)
        value_changed_count += occurrences
        if occurrences > 0:
            SQL_PARSED_SCRIPT += parse_line(occurrences, line)
        else:
            SQL_PARSED_SCRIPT += line

    print "%i values have been changed" % value_changed_count


def main():
    print start_msg
    try:
        parse_args()
        parse_script()
    except (KeyboardInterrupt, EOFError):
        print "\nClosing..."
    f = open(SQL_OUTPUT_LOCATION, 'w')
    f.write(SQL_PARSED_SCRIPT)

if __name__ == '__main__':
    main()
