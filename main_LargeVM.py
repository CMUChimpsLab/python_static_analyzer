'''
Created on Sep 9, 2012

@author: psachdev
'''
#import manager
import namespaceanalyzer
import permission
import SearchIntents
import DbManager
import logging
import sys

from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis.analysis import *

from multiprocessing import Pool, get_logger

def handler (signum, sigframe):
    raise Exception ("Killed");


def analyze((apkEntry, OUT)):
    try:
        OUT = OUT + '/'
        fileName = apkEntry['packageName'] + '.apk'
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
        dbMgr.deleteEntry(apkEntry['packageName'])
    
        packages = instance.execute (filename, outFileName, dbMgr, fileName, category, a, d, dx)
                
        outfile_perm = '/permissions.txt'
        outfile_perm = OUT + outfile_perm
        permission.StaticAnalyzer (filename, outfile_perm, packages, dbMgr, fileName, a, d, dx)
                
        outfile_links = '/links.txt'
        outfile_links = OUT + outfile_links
        SearchIntents.Intents(filename, outfile_links, packages, dbMgr, fileName, a, d, dx);
        dbMgr.androidAppDB.apkInfo.update({'packageName':apkEntry['packageName']}, {'$set': {'isApkUpdated': False}})
        return apkEntry['packageName']
    except:
        logger.error("\n")
        logger.error("=======================================================================")
        logger.error("\n")
        logger.exception("Main : Exception occured for " + apkEntry['packageName'])
        return ""

if __name__ == '__main__':
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
          
    #in case the crawler breaks, append to the list.
    analyzedApkFile = open(OUT + '/' + 'filelist.txt', 'a+')
    '''
    Database Handle used to insert fields
    '''
    dbMgr = DbManager.DBManagerClass()
    
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
    else:
        apkList = list(dbMgr.androidAppDB.apkInfo.find({'isApkUpdated':True},{"fileDir":1, 'packageName':1}))
    apkList = [(entry, OUT) for entry in apkList]
    #apkList = [({'packageName': line.rstrip('\n').replace(".apk",''), 'fileDir': '../downloads/'}, OUT) for line in open("apkList").readlines()]
    numberOfProcess = 4
    pool = Pool(numberOfProcess)
    for packageName in pool.imap(analyze, apkList):
        if packageName != "":
            analyzedApkFile.write(packageName + '\n')
            analyzedApkFile.flush()
    
