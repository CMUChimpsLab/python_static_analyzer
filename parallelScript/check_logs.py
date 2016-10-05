#!/usr/bin/env python

# Script to scan through parallelLog directories and summarize each instance's
# status.

import datetime
import os

timeDir = "201609261725"
dateDir = "20160926"
BASE_LOG_DIR = "/home/lsuper/apk_data/log/staticAnalysis/parallelLog/" +
                timeDir + "/"

NUM_INSTANCES = 14

def file_len(fname):
    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if __name__ == "__main__":
    print str(datetime.datetime.now())

    instanceIPs = []
    with open("job_LargeVM.sh","r") as f:
        for l in f:
            if ("]=" in l) and ("instanceArray[" in l):
                IPStart = l.find('"') + 1
                IP = ""
                while l[IPStart] != '"':
                    IP += l[IPStart]
                    IPStart += 1
                instanceIPs.append(IP)

    for i in xrange(0, NUM_INSTANCES):
        assigned = "notAnalyzed/" + dateDir + "/instance-" + str(i)
        done = BASE_LOG_DIR + "instance-" + str(i) + "/filelist.txt"
        exp = BASE_LOG_DIR + "instance-" + str(i) + "/exceptions.log"

        doneLen = file_len(done)
        assignLen = file_len(assigned)
        progress = float(file_len(done))/float(file_len(assigned)) * 100

        print ("Instance %d: %0.2f%%\n OR %d / %d") % 
            (i, progress, doneLen, assignLen)

        subprocess.call(["bash", "check_screen.sh", instanceIPs[i]])
        for l in open("isRunning.txt", "r"):
            if "No Sockets" in l:
                print "no longer running"
            else:
                print "running"
            break
        subprocess.call(["rm", "isRunning.txt", instanceIPs[i]])

        if os.path.getsize(exp) > 0:
            print " ERROR"
        else:
            print " OK"
