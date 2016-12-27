#! /usr/bin/python
# encoding:utf8

import sys
import subprocess

PYLINT = 'pylint'
FILE_PATH = sys.argv[1]

def run_pylint():
    if FILE_PATH == "":
        return "Please input filename"

    command = [PYLINT, FILE_PATH, "-f", "parseable"]  # 指定输出格式]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        output = err.output
    return output

def main():
    if not FILE_PATH.endswith(".py"):
        print "pylint not support file type"
        return
    output = run_pylint()
    print output

if __name__ == '__main__':
    main()
