from pymongo import MongoClient 
from dbConfig import HOSTNAME, USERNAME, PASSWORD

class DBManagerClass:
    '''
    classdocs
    '''
    def __init__(self):
        # self.client = MongoClient(HOSTNAME, 27017)
        self.client = MongoClient("localhost", 27017)
        self.client["admin"].authenticate(USERNAME, PASSWORD)
        self.staticAnalysisDB = self.client['staticAnalysis']
        self.androidAppDB = self.client['androidApp']
        
        #self.staticAnalysisDB = self.client['test']
    
        
    def getManiFestPermissions(self, packagename):
        return self.androidAppDB.apkInfo.find_one({'packageName': packagename}, {'permission':1})['permission']

    def insert3rdPartyPackageInfo (self, packagename, filename, externalpackagename, category):
        self.staticAnalysisDB.Test_3rd_party_packages.insert({'packagename': packagename, 'filename': filename, 'externalpackagename': externalpackagename, 'category': category})
        #print "Rows affected after inserting 3rdpartypackage - " + str (rows_affected)
        
         
    def insertPermissionInfo (self, packagename, filename, permission, is_external, dest, externalpackagename, src):
        self.staticAnalysisDB.Test_permissionlist.insert({'packagename': packagename, 'filename': filename, 'permission': permission, 'is_external': is_external, 'dest': dest, 'externalpackagename': externalpackagename, 'src': src})
        #print "Rows affected after inserting permission - " + str (rows_affected)
        
    def insertLinkInfo (self, packagename, filename, link_url, is_external, triggered_by_code, externalpackagename):
        if type(link_url) != unicode:
            link_url = link_url.decode('UTF-8', 'ignore')
        self.staticAnalysisDB.Test_linkurl.insert({'packagename': packagename, 'filename': filename, 'link_url': link_url, 'is_external': is_external, 'triggered_by_code': triggered_by_code, 'externalpackagename': externalpackagename})
        #print "Rows affected after inserting permission - " + str (rows_affected)
        
    def deleteEntry (self, packagename):
       self.staticAnalysisDB.Test_linkurl.remove({'packagename': packagename})
       self.staticAnalysisDB.Test_permissionlist.remove({'packagename': packagename})
       self.staticAnalysisDB.Test_3rd_party_packages.remove({'packagename': packagename})
        
