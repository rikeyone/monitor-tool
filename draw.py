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
import re
import matplotlib.pyplot as plt
from optparse import OptionParser

def readFile(tag, filename):
    opErr = True
    for c in ("utf-8", "GB2312", "ISO-8859-2"):
        try:
            fp = io.open(filename, "r", encoding=c)
            opErr = False
            break
        except UnicodeDecodeError, e:
            continue
    if opErr:
        print("open: %s" % e)
        sys.exit(1)

    value = list()
    for line in fp.readlines():
        if tag == None:
            match = re.search("(.*):(.*)", line)
            if match:
                tag = match.group(1)
            else:
                tag = "default"
        else:
            if tag != "default":
                attr = "%s:(\d*\.?\d*).*" % tag
            else:
                attr = ".*?(\d*\.?\d*).*"
            match = re.search(attr, line)
            if match:
                value.append(str(match.group(1)))
    fp.close()
    return tag, value

def drawImage(tag, value, image):
    """
    默认的比例：[6.0,4.0]，dpi为100，因此图片分辨率 600*400
    指定dpi=200，图片分辨率为 1200*800
    指定dpi=300，图片分辨率为 1800*1200
    设置figsize可以在不改变分辨率情况下改变比例
    """

    plt.rcParams['figure.figsize'] = (6.0, 3.0)  #设置figure_size比例尺寸
    plt.rcParams['savefig.dpi'] = 300            #执行savefig操作时，设置的默认dpi
    plt.rcParams['figure.dpi'] = 300             #figure创建时的默认dpi
    fig = plt.figure()
    plt.xlabel("time")
    plt.ylabel("value")
    plt.title(tag)
    plt.plot(value)
    plt.plot(value, 'ro')
    fig.savefig(image, dpi=300)
    plt.show()
    plt.close()

def main():
    """
    主函数
    """
    parser = OptionParser()
    parser.add_option("--file", "-f", action="store",
                        dest="file", default=False, help="Input data file. Eg. -f file_name")
    parser.add_option("--tag", "-t", action="store",
                        dest="tag", default=None, help="Tag of the data, default is the first line before \":\". Eg. -t mem")
    parser.add_option("--output", "-o", action="store",
                        dest="output", default=False, help="output data file. Eg. -o data.png")

    (options, args) = parser.parse_args()
    if len(sys.argv) < 2:
        print parser.print_help()
        return 0

    filename = None
    image = None
    tag = None

    if options.file:
        filename = options.file

    if options.output:
        image = options.output
    else:
        image = options.file + ".png"

    if options.tag:
        tag = options.tag

    ret = readFile(tag, filename)
    print ret[0]
    print ret[1]
    drawImage(ret[0], ret[1], image)

if __name__ == '__main__':
    main()