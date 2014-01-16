'''
Created on Sep 9, 2012

@author: psachdev
'''
#import manager
import namespaceanalyzer
import permission
import SearchIntents
import os
import DbManager
import logging
import signal
import sys

from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis.analysis import *

def handler (signum, sigframe):
    raise Exception ("Killed");


def naiveSearch(aDict, searchString):
    for key in aDict:
        if searchString in key: 
            return 1
    return 0

if __name__ == '__main__':
    OUT = sys.argv[1] + '/'
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
    # Make a global logging object.
    logObject = logging.getLogger("logfile")
    logObject.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    logFileHandler = logging.FileHandler(OUT + 'exceptions.log')
    logFileHandler.setLevel(logging.DEBUG)
    logFormat = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
    logFileHandler.setFormatter(logFormat)
    logObject.addHandler(logFileHandler)
    
    #signal.signal(signal.SIGKILL, handler)

    #DIR = '<Directory-Name-where all apks reside>'
    #OUT = '<Directory-Name where output files are expected>'
    
    filesread = {}
    filelistname = OUT + 'filelist.txt'
    filelisthandle = open (filelistname, 'r+')
    lines = filelisthandle.readlines()
    for filename in lines:
        filesread[filename] = 1
    filelisthandle.close()
    filelisthandle = open (filelistname, 'a')

    for entry in dbMgr.androidAppDB.apkInfo.find({'isApkUpdated':True},{"fileDir":1, 'packageName':1}, timeout=False):
        fileName = entry['packageName'] + '.apk'
        path = entry['fileDir']
        try:
            print "FileName Analyzed :"  + fileName
            tokens = namespaceanalyzer.NameSpaceMgr.GetTokensStatic (path, '/')
            category =  tokens [len (tokens) - 1]
            #print category
            filename = path + '/' + fileName
            if fileName != 'links.txt' and fileName != 'permissions.txt' and fileName != 'packages.txt' and fileName != '.dropbox' and fileName != 'list.csv' and fileName != 'externalpackcntt.csv' and fileName != 'externalpackpopularitycnt.csv' and fileName != 'packages.txt':
                x = naiveSearch (filesread, fileName)
                if x == 0:
                    filelisthandle.write( str(fileName) )
                    filelisthandle.write("\n")
                    filelisthandle.flush()
                else:
                    continue
                outFileName = '/package.txt'
                outFileName = OUT + outFileName
                instance = namespaceanalyzer.NameSpaceMgr()

                a = apk.APK(filename)
                d = dvm.DalvikVMFormat (a.get_dex())
                dx = uVMAnalysis (d)

                packages = instance.execute (filename, outFileName, dbMgr, fileName, category, a, d, dx)
                    
                outfile_perm = '/permissions.txt'
                outfile_perm = OUT + outfile_perm
                x = permission.StaticAnalyzer (filename, outfile_perm, packages, dbMgr, fileName, a, d, dx)
                    
                outfile_links = '/links.txt'
                outfile_links = OUT + outfile_links
                SearchIntents.Intents(filename, outfile_links, packages, dbMgr, fileName, a, d, dx);
                dbMgr.androidAppDB.apkInfo.update({'packageName':entry['packageName']}, {'$set': {'isApkUpdated': False}})
        except:
            logObject.error("\n")
            logObject.error("=======================================================================")
            logObject.error("\n")
            logObject.exception("Main : Exception occured for " + fileName)
                
    filelisthandle.close()    
                
               
            
    
    
