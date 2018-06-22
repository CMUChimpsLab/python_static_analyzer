'''
Created on Sep 9, 2012

@author: psachdev
'''
#import manager
import re
import namespaceanalyzer
import permission
import SearchIntents
#import DbManager
import logging
import sys
import datetime
import xmltodict
import collections

from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis.analysis import *

from multiprocessing import Pool, get_logger
import pprint

def handler (signum, sigframe):
    raise Exception ("Killed");


def convert_to_dict(ordered_dict):
    ordered_dict = dict(ordered_dict)
    for key in ordered_dict:
        if type(ordered_dict[key]) == collections.OrderedDict:
            ordered_dict[key] = convert_to_dict(ordered_dict[key])
        elif type(ordered_dict[key]) == list:
            dicts = []
            for item in ordered_dict[key]:
                if type(item) == collections.OrderedDict:
                    dicts.append(convert_to_dict(item))
            ordered_dict[key] = dicts
    return ordered_dict


def update_apk_entry((apkEntry, OUT)):
    fileName = apkEntry["packageName"]
    path = apkEntry["fileDir"]
    filename = path + "/" + fileName
    print filename
    try:
      a = apk.APK(filename, zipmodule=1)
    except:
      a = apk.APK(filename, zipmodule=2)

    vc = a.get_androidversion_name()
    packageName = a.get_package()
    # TODO: define docDict here using playstore-scraper get_doc_apk_details
    isApkUpdated = False
    preDetailsEntry = dbMgr.androidAppDB.apkDetails.find_one(
        {"details.appDetails.packageName":packageName},
        {"updatedTimestamp":0, "_id":0})
    if preDetailsEntry != docDict:
        try:
            isApkUpdated = ((not preDetailsEntry) or 
                (docDict["details"]["appDetails"]["versionCode"] != 
                    preDetailsEntry["details"]["appDetails"]["versionCode"]))
        except KeyError as e:
            isApkUpdated = True
        docDict["updatedTimestamp"] = datetime.datetime.utcnow()
        dbMgr.androidAppDB.apkDetails.update(
            {"details.appDetails.packageName":packageName},
            docDict,
            upsert=True)
    else:
        isApkUpdated = False

    pp.pprint(docDict)
    infoDict = docDict["details"]["appDetails"]

    #isFree = not doc.offer[0]
    isCurrentVersionDownloaded = False
    isSizeExceed = False

    preInfoEntry = dbMgr.androidAppDB.apkInfo.find_one(
        {"packageName":packageName},
        {"isFree":0,
         "isSizeExceed":0,
         "updatedTimeStamp":0,
         "_id":0})
    if preInfoEntry == None:
        preInfoEntry = {}
    preIsDownloaded = preInfoEntry.pop("isDownloaded", False)
    preIsCurrentVersionDownloaded = preInfoEntry.pop("isCurrentVersionDownloaded", False)
    preIsApkUpdated = preInfoEntry.pop("isApkUpdated", False)
    preFileDir = preInfoEntry.pop("fileDir", "")
    
    if (preInfoEntry != infoDict or 
            (preIsCurrentVersionDownloaded == False and 
             isCurrentVersionDownloaded == True)):
        #infoDict["isFree"] = isFree
        infoDict["isDownloaded"] = preIsDownloaded or isCurrentVersionDownloaded
        infoDict["isCurrentVersionDownloaded"] = isCurrentVersionDownloaded
        if preFileDir == "" and isCurrentVersionDownloaded:
            infoDict["fileDir"] = fileDir
        else:
            infoDict["fileDir"] = preFileDir
        infoDict["isApkUpdated"] = (preIsApkUpdated or 
            (isApkUpdated and isCurrentVersionDownloaded) or 
            ((not isApkUpdated) and 
                (preIsCurrentVersionDownloaded == False) and 
                isCurrentVersionDownloaded == True))
        if isSizeExceed != None:
            infoDict["isSizeExceed"] = isSizeExceed
        infoDict["updatedTimestamp"] = datetime.datetime.utcnow()
        db.apkInfo.update({"packageName": packageName}, infoDict, upsert=True)

    return ret


def analyze((apkEntry, OUT)):
    try:
        OUT = OUT + '/'
        fileName = apkEntry['packageName']
        path = apkEntry['fileDir']
        print "FileName Analyzed :"  + fileName
        tokens = namespaceanalyzer.NameSpaceMgr.GetTokensStatic (path, '/')
        category =  tokens [len (tokens) - 1]
        #print category
        filename = path + '/' + fileName
        outFileName = '/package.txt'
        outFileName = OUT + outFileName
        instance = namespaceanalyzer.NameSpaceMgr()
    
        try:
          a = apk.APK(filename, zipmodule=1)
        except:
          a = apk.APK(filename, zipmodule=2)
        d = dvm.DalvikVMFormat (a.get_dex())
        dx = uVMAnalysis (d)
        #remove old db entry in static analysis db
        #dbMgr.deleteEntry(apkEntry['packageName'])
    
        packages = instance.execute (filename, outFileName, None, fileName, category, a, d, dx)
        print(packages)
        outfile_perm = '/permissions.txt'
        outfile_perm = OUT + outfile_perm
        permission.StaticAnalyzer (filename, outfile_perm, packages, None, fileName, a, d, dx)
                
        outfile_links = '/links.txt'
        outfile_links = OUT + outfile_links
        SearchIntents.Intents(filename, outfile_links, packages, None, fileName, a, d, dx);
        #dbMgr.androidAppDB.apkInfo.update({'packageName':apkEntry['packageName']}, {'$set': {'isApkUpdated': False}})
        return apkEntry['packageName']
    except:
        logger.error("\n")
        logger.error("=======================================================================")
        logger.error("\n")
        logger.exception("Main : Exception occured for " + apkEntry['packageName'])
        return ""

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4, width = 1)

    if len(sys.argv) < 3:
      print "Usage: python main_LargeVM.py log_file_dir apk_list_file"
      sys.exit(1)

    OUT = sys.argv[1]
    isParallel = False
    #for parallel running on multiple instances
    apkListFile = None
    if len(sys.argv) > 2:
        apkListFile = sys.argv[2] 
        isParallel = True
    print isParallel
          
    #in case the crawler breaks, append to the list.
    analyzedApkFile = open(OUT + '/' + 'filelist.txt', 'a+')
    '''
    Database Handle used to insert fields
    '''
    # dbMgr = DbManager.DBManagerClass()
    
    '''
    Example of how the various entrie are made into the database
    dbMgr.insert3rdPartyPackageInfo("testpackage", "testfilename", "testexternalpackage")
    dbMgr.insertPermissionInfo('testpackage', 'testfilename', 'testpermission', True, 'testdest', 'testexternalpackagename', 'testsrc')
    dbMgr.insertLinkInfo('testpackage', 'testfilename', 'testlink', True, 'testdest', 'testexternalpackagename')
    '''
    logger = get_logger()
    logFileHandler = logging.FileHandler(OUT + '/exceptions.log')
    logFormat = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
    logFileHandler.setLevel(logging.DEBUG)
    logFileHandler.setFormatter(logFormat)
    logger.addHandler(logFileHandler)
    
    apkList = []
    if isParallel:
        apkList_f = open(apkListFile)
        for line in apkList_f:
            pair = line.rstrip('\n').split(' ')
            apkList.append({'packageName': pair[0], "fileDir": pair[1].replace("/home/lsuper/apk_data", "/home/ubuntu")}) 
        apkList_f.close()
    # else:
    #     apkList = list(dbMgr.androidAppDB.apkInfo.find({'isApkUpdated':True},{"fileDir":1, 'packageName':1}))
    apkList = [(entry, OUT) for entry in apkList]

    print apkList
    for apkFile in apkList:
        # update_apk_entry(apkFile)
        packageName = analyze(apkFile)
        print packageName
        if packageName != "":
            analyzedApkFile.write(packageName + "\n")
            analyzedApkFile.flush()

    #apkList = [({'packageName': line.rstrip('\n').replace(".apk",''), 'fileDir': '../downloads/'}, OUT) for line in open("apkList").readlines()]
    # numberOfProcess = 4
    # pool = Pool(numberOfProcess)
    # for packageName in pool.imap(analyze, apkList):
    #     if packageName != "":
    #         analyzedApkFile.write(packageName + '\n')
    #         analyzedApkFile.flush()
    
