import os
import sys


def testcode(value):
    try:
        os.chdir(value)
    except FileNotFoundError:
        print("this directory is not exist", file=sys.stderr)
        exit(1)
