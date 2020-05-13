#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import io
import sys
import pickle
import copy
import shutil
import commands
import time
from optparse import OptionParser


if sys.getdefaultencoding() != 'gbk':
    reload(sys)
    sys.setdefaultencoding('utf8')

def getInfo(info):
    if info == "mem":
        cmdStr = "free | awk \'{print $3}\' | sed -n \'2p\'"
        status,retdata = commands.getstatusoutput(cmdStr)
    elif info == "io":
        cmdStr = "mpstat | awk \'{print $6}\' | sed -n \'4p\'"
        status,retdata = commands.getstatusoutput(cmdStr)
    elif info == "cpu":
        cmdStr = "mpstat | awk \'{print $12}\' | sed -n \'4p\'"
        status,retdata = commands.getstatusoutput(cmdStr)
    else:
        print "Not support info:" + info
        exit()
    return retdata

def monitor(info, output, timeout):
    track_mem = False
    track_cpu = False
    track_io = False

    if info == "all":
        track_mem = True
        track_io = True
        track_cpu = True
    elif info == "mem":
        track_mem = True
    elif info == "io":
        track_io = True
    elif info == "cpu":
        track_cpu = True
    else:
        print "Not support info:" + info
        exit()

    now = int(time.time())
    if timeout != None:
        endtime = int(now + float(timeout) * 60)
    else:
        endtime = now

    print "start time stamp:", now
    print "timeout stamp:", endtime

    tmp = io.open(output, "w+", encoding="utf-8")
    while timeout == None or now < endtime:
        if track_cpu:
            line = getInfo("cpu")
            usage = 100 - float(line)
            tmp.write("cpu:%s\n" % str(usage).decode("utf-8"))
        if track_io:
            line = getInfo("io")
            tmp.write("iowait:%s\n" % line.decode("utf-8"))
        if track_mem:
            line = getInfo("mem")
            tmp.write("mem:%s\n" % line.decode("utf-8"))
        if timeout != None:
            now = int(time.time())
        time.sleep(3)
    tmp.close()
    print "exit time stamp:", now

def main_function():
    """
    主函数
    """
    parser = OptionParser()
    parser.add_option("--info", "-i", action="store",
                        dest="info", default=False, help="information which will be traced. Eg. -i mem / -i cpu / -i io")
    parser.add_option("--timeout", "-t", action="store",
                        dest="timeout", default=False, help="Record time (minutes). Eg. -t 10")
    parser.add_option("--output", "-o", action="store",
                        dest="output", default=False, help="output data file. Eg. -o data.txt")

    (options, args) = parser.parse_args()
    if len(sys.argv) < 2:
        print parser.print_help()
        return 0

    info = None
    output = None
    timeout = None

    if options.info:
        info = options.info

    if options.output:
        output = options.output
    else:
        output = options.info

    if options.timeout:
        timeout = options.timeout

    monitor(info, output, timeout)

if __name__ == '__main__':
    main_function()
