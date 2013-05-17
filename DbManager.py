'''
Created on Dec 8, 2012

@author: psachdev
'''
import MySQLdb as db
from MySQLdb.constants import FIELD_TYPE

class DBManagerClass:
    '''
    classdocs
    '''


    def __init__(self):
        self.username = 'root'
        self.password = 'root'
        self.host = '127.0.0.1'
        self.dbname = 'staticanalysisresults'
        self.dbport = 3306
        self.table_externalPackage = '3rd_party_packages'
        self.custom_conv = { FIELD_TYPE.BIT: int }
        self.connectToDb()
        self.createTables()
    
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
        cur = self.dbconn.cursor()
        escape_packagename = str (self.dbconn.escape_string(packagename))
        escape_filename = str (self.dbconn.escape_string(filename))
        escape_externalpackagename = str (self.dbconn.escape_string(externalpackagename))
        escape_category = str (self.dbconn.escape_string(category))
        rows_affected = cur.execute("INSERT INTO Test_3rd_party_packages (packagename, filename, category, 3rd_party_package) VALUES('%s', '%s', '%s', '%s')" % (escape_packagename, escape_filename, escape_category, escape_externalpackagename))
        self.dbconn.commit()
        #print "Rows affected after inserting 3rdpartypackage - " + str (rows_affected)
        
         
    def insertPermissionInfo (self, packagename, filename, permission, is_external, dest, externalpackagename, src):
        cur = self.dbconn.cursor()
        escape_packagename = str (self.dbconn.escape_string(packagename))
        escape_filename = str (self.dbconn.escape_string(filename))
        escape_externalpackagename = str (self.dbconn.escape_string(externalpackagename))
        escape_permission = str (self.dbconn.escape_string(permission))
        escape_dest = str (self.dbconn.escape_string(dest))
        escape_src = str (self.dbconn.escape_string(src))
        
        rows_affected = cur.execute("INSERT INTO Test_permissionlist (packagename, appfilename, permission, is_external, dest, 3rd_party_package, src) VALUES('%s', '%s', '%s', '%i', '%s', '%s', '%s')" % (escape_packagename, escape_filename, escape_permission, is_external, escape_dest, escape_externalpackagename, escape_src))
        self.dbconn.commit()
        #print "Rows affected after inserting permission - " + str (rows_affected)
        
    def insertLinkInfo (self, packagename, filename, link_url, is_external, triggered_by_code, externalpackagename):
        cur = self.dbconn.cursor()
        escape_packagename = str (self.dbconn.escape_string(packagename))
        escape_filename = str (self.dbconn.escape_string(filename))
        escape_triggered_by_code = str (self.dbconn.escape_string( triggered_by_code))
        escape_externalpackagename = str (self.dbconn.escape_string(externalpackagename))
        escape_url = str (self.dbconn.escape_string(link_url))
        rows_affected = cur.execute("INSERT INTO Test_linkurl (packagename, appfilename, link_url, is_external, triggered_by_code, 3rd_party_package) VALUES('%s', '%s', '%s', '%d', '%s', '%s')" % (escape_packagename, escape_filename, escape_url, is_external, escape_triggered_by_code, escape_externalpackagename))
        self.dbconn.commit()
        #print "Rows affected after inserting permission - " + str (rows_affected)
        
    def deleteEntry (self, apkname):
       cur = self.dbconn.cursor()
       escape_apkname = str (self.dbconn.escape_string(apkname))
       rows_affected = cur.execute("DELETE FROM Test_linkurl WHERE packagename='%s'" % (escape_apkname))
       print "Rows affected after deletion - " + str (rows_affected)
       rows_affected = cur.execute("DELETE FROM Test_permissionlist WHERE packagename='%s'" % (escape_apkname))
       print "Rows affected after deletion - " + str (rows_affected)
       rows_affected = cur.execute("DELETE FROM Test_3rd_party_packages WHERE packagename='%s'" % (escape_apkname))
       print "Rows affected after deletion - " + str (rows_affected)
       self.dbconn.commit()
       
        
        
        
