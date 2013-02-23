#!/usr/bin/python

from __future__ import print_function

# XXX: Though I've tried to order things with greatest consistency,
# there are still tons of ways data could be lost or exceptions thrown
# if signals come in at the wrong time. Not sure how to solve this.

import sys
import subprocess
import signal

line_buffered = None
bs = None

ch = None
data = None

def getdata():
    if line_buffered:
        return sys.stdin.readline()
    else:
        return sys.stdin.read(bs)

def catrun_setup():
    global ch
    if not ch:
        ch = subprocess.Popen(sys.argv[1:], stdin=subprocess.PIPE)

def killch():
    global ch
    if ch:
        ch.stdin.close()
        ch.wait()
        ch = None

def catrun():
    global data

    if data == None:
        data = getdata()

    while data:
        ch.stdin.write(data)
        data = None
        sys.stdout.flush()
        data = getdata()

    killch()

# idempotent start
def idemstart():
    catrun_setup()
    catrun()

# idempotent stop
def idemstop():
    killch()
    signal.pause()

def sigusr1(signum, frame):
    idemstart()

def sigusr2(signum, frame):
    idemstop()

# TODO: command line parser:
# If the first argument doesn't start with hyphen, it is the target
# program, followed by zero or more arguments to it.
# Otherwise, these arguments are allowed:
# -p, --paused  Start in the stopped state
# --line-buffered  Process line by line
# --bs  If not using --line-buffered, how many bytes to read/write at each step (default 512)
# --  Everything past this will be the program and its arguments
def main():
    global line_buffered
    global bs
    global ch

    try:
        signal.signal(signal.SIGUSR1, sigusr1)
        signal.signal(signal.SIGUSR2, sigusr2)

        line_buffered = True
        paused = False
        bs = 512

        if paused:
            idemstop()
        else:
            idemstart()

    except KeyboardInterrupt:
        killch()

if __name__ == '__main__':
    main()
