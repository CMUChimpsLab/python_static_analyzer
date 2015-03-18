"""
This script will do
1. get a full list of apks which has not been analyzed by our static analysis code. 
2. split the list into several small lists for each instance
Remote instance will do analysis for its list
The list format
packagename fileDir
"""

# Number of AWS instances used to run the static analysis
NUM_INSTANCES = 16

from pymongo import MongoClient
import datetime
import os
import errno
import dbConfig
today = str(datetime.date.today()).replace('-','')
outPutPath = "notAnalyzed/" + today + '/'

db = dbConfig.androidAppDB

def getNonAnalyzedApks():
  apkList = []
  for entry in db.apkInfo.find({'isApkUpdated':True}):
    apkList.append((entry['packageName'], entry['fileDir']))
  return apkList

def generateListPerInstance(apkList, numberOfInstances):
  try: 
    os.makedirs(outPutPath)
  except OSError as exc: 
    if exc.errno == errno.EEXIST and os.path.isdir(outPutPath):
        pass
  apkPerInstance = len(apkList)/numberOfInstances + 1
  for index in range(numberOfInstances):
    f = open(outPutPath + "instance-%d"%index, 'w')
    count = 0
    while count < apkPerInstance and len(apkList) > 0:
      count += 1
      entry = apkList.pop()
      print >>f, entry[0], entry[1]
    f.close()
    if len(apkList) == 0:
      return


if __name__ == "__main__":
  apkList = getNonAnalyzedApks()
  generateListPerInstance(apkList, NUM_INSTANCES)
