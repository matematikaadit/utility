#!/usr/bin/env python

from __future__ import print_function, with_statement
import sys

IN_HEX = "\x8A\x5B\x5C"
OUT_HEX = "\x90\xB3\x01"


def main():
    guard_arg()

    with open(sys.argv[1], "rb") as f_in:
        with open(sys.argv[2], "wb") as f_out:
            f_out.write(
                f_in.read().replace(IN_HEX, OUT_HEX)
            )


def guard_arg():
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)


def usage():
    print("usage: {} inputfile outputfile\n".format(sys.argv[0]))
    print("Crack Sublime Executable")

if __name__ == "__main__":
    main()
