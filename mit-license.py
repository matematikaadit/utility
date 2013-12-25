#!/usr/bin/env python3

import sys
import pwd
import os
import datetime

MIT_LICENSE = """
License
-------

The MIT License (MIT)

Copyright (c) {year} {name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


def main():
    if "--help" in sys.argv:
        usage()
        sys.exit(1)

    name = get_name()
    year = get_year()
    print_license(name, year)


def print_license(name, year):
    print(MIT_LICENSE.format(name=name, year=year))


def usage():
    print("usage: {0} [name] [year]".format(sys.argv[0]))


def get_name():
    if len(sys.argv) > 1 and not sys.argv[1].isdigit():
        name = sys.argv[1]
    else:
        name = get_sys_fullname()
    return name


def get_sys_fullname():
    pwstruct = pwd.getpwuid(os.getuid())
    name = pwstruct.pw_gecos.split(',')[0]
    return name


def get_year():
    if len(sys.argv) > 1 and sys.argv[-1].isdigit():
        year = sys.argv[-1]
    else:
        year = get_sys_year()
    return year


def get_sys_year():
    return datetime.date.today().year

if __name__ == "__main__":
    main()
