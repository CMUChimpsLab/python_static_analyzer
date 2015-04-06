#!/usr/bin/env python

# Script to scan through parallelLog directories and summarize each instance's
# status.

import datetime
import os

BASE_LOG_DIR = "/home/lsuper/apk_data/log/staticAnalysis/parallelLog/201504050619/"

NUM_INSTANCES = 16

def file_len(fname):
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i + 1

if __name__ == "__main__":
  print str(datetime.datetime.now())
  for i in xrange(0, NUM_INSTANCES):
    assigned = "notAnalyzed/20150405/instance-" + str(i)
    done = BASE_LOG_DIR + "instance-" + str(i) + "/filelist.txt"
    exp = BASE_LOG_DIR + "instance-" + str(i) + "/exceptions.log"

    progress = float(file_len(done))/float(file_len(assigned)) * 100

    print ("Instance %d: %0.2f%%") % (i, progress),

    if os.path.getsize(exp) > 0:
      print " ERROR"
    else:
      print " OK"
