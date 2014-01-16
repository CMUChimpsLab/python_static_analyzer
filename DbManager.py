'''
Created on Dec 8, 2012

@author: psachdev
'''
from pymongo import MongoClient 

class DBManagerClass:
    '''
    classdocs
    '''


    def __init__(self):
        """
        self.username = 'root'
        self.password = 'root'
        self.host = '127.0.0.1'
        self.dbname = 'staticanalysisresults'
        self.dbport = 3306
        self.table_externalPackage = '3rd_party_packages'
        self.custom_conv = { FIELD_TYPE.BIT: int }
        self.connectToDb()
        self.createTables()
        """
        self.db = MongoClient("54.204.168.124", 27017)['staticAnalysis']
        #self.db = MongoClient("localhost", 27017)['test']
    
    def connectToDb (self):
        self.dbconn = db.Connect(self.host, self.username, self.password, self.dbname, self.dbport, conv=self.custom_conv)
        
    def createTables (self):
        cur = self.dbconn.cursor ()
        cur.execute("CREATE TABLE IF NOT EXISTS \
        Test_3rd_party_packages (Id INT PRIMARY KEY AUTO_INCREMENT, packagename VARCHAR(255), filename VARCHAR(255), category VARCHAR(255), 3rd_party_package VARCHAR(255))")
        cur.execute("CREATE TABLE IF NOT EXISTS \
        Test_permissionlist (Id INT PRIMARY KEY AUTO_INCREMENT, packagename VARCHAR(255), appfilename VARCHAR(255), permission VARCHAR(255), is_external INT, dest VARCHAR(255), 3rd_party_package VARCHAR(255), src VARCHAR(255))")
        cur.execute("CREATE TABLE IF NOT EXISTS \
        Test_linkurl (Id INT PRIMARY KEY AUTO_INCREMENT, packagename VARCHAR(255), appfilename VARCHAR(255), link_url VARCHAR(255), is_external INT, triggered_by_code VARCHAR(255), 3rd_party_package VARCHAR(255))")
        
    def insert3rdPartyPackageInfo (self, packagename, filename, externalpackagename, category):
        self.db.Test_3rd_party_packages.insert({'packagename': packagename, 'filename': filename, 'externalpackagename': externalpackagename, 'category': category})
        #print "Rows affected after inserting 3rdpartypackage - " + str (rows_affected)
        
         
    def insertPermissionInfo (self, packagename, filename, permission, is_external, dest, externalpackagename, src):
        self.db.Test_permissionlist.insert({'packagename': packagename, 'filename': filename, 'permission': permission, 'is_external': is_external, 'dest': dest, 'externalpackagename': externalpackagename, 'src': src})
        #print "Rows affected after inserting permission - " + str (rows_affected)
        
    def insertLinkInfo (self, packagename, filename, link_url, is_external, triggered_by_code, externalpackagename):
        self.db.Test_linkurl.insert({'packagename': packagename, 'filename': filename, 'link_url': link_url, 'is_external': is_external, 'triggered_by_code': triggered_by_code, 'externalpackagename': externalpackagename})
        #print "Rows affected after inserting permission - " + str (rows_affected)
        
    def deleteEntry (self, packagename):
       self.db.Test_linkurl.remove({'packagename': packagename})
       self.db.Test_permissionlist.remove({'packagename': packagename})
       self.db.Test_3rd_party_packages.remove({'packagename': packagename})
       
        
        
        