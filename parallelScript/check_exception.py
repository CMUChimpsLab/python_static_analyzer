#!/usr/bin/env python

# Script to help scan through parallelLog directories and look for non-empty
# exception files.

import os

BASE_LOG_DIR = "/home/lsuper/apk_data/log/staticAnalysis/parallelLog/201504050619/"

NUM_INSTANCES = 16

for i in xrange(0, NUM_INSTANCES):
  path = BASE_LOG_DIR + "instance-" + str(i) + "/exceptions.log"
  if os.path.getsize(path) > 0:
    print "Instance " + str(i)
