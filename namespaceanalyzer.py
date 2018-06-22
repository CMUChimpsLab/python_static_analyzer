'''
Created on Sep 21, 2012

@author: psachdev
'''
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis.analysis import *
import DirStructHandler
import PackageRules
import re

class NameSpaceMgr:
    '''
    1. This class creates a n-tree of the directories present in apk
    2. After creation of the tree it creates a set of static rules for printing external packages
    3. Iterates over the tree structure and prints the directories according to rules
    4. Returns all the packages encountered as it will be used in printing links and permissions 
    '''
        
    def __init__(self):
        '''
        1. Packages contains all the packages encountered while traversing the tree
        '''
        self.packages = []
        '''
        2. Contains alreadyprinted. To take of the noise produced by decompilation
        '''
        self.alreadyPrinted = []
        '''
        3. Tokenized items of the main package name
        '''
        self.main_package_tokens = []
          
    @staticmethod
    def GetTokensStatic (string, delimiter):
           
        tokens = []
        for name in string.split (delimiter):
            tokens.append(name)
                        
        return tokens         
    
    def GetTokens (self, string):
           
        tokens = []
        for name in string.split ('.'):
            tokens.append(name)
                        
        return tokens

    '''
    Song
    Special Handling for Google SDK
    '''
    def specialHandlingForGoogleSDK(self, package_name):
        if "googleAnalytics" not in self.alreadyPrinted and (package_name.startswith('Lcom/google/analytics/') or package_name.startswith('Lcom/google/android/apps/analytics/')):
            #should do something or not for tracking
            pass
        if "admob" not in self.alreadyPrinted and package_name.startswith('Lcom/google/ads'):
            self.dbMgr.insert3rdPartyPackageInfo (self.main_package_name, self.fileName, "admob", self.category)
            self.alreadyPrinted.append ("admob")
            self.packages.append ("admob")

    
    def execute (self, fileName, outFileName, dbMgr, noprefixfilename, category, a, d, dx):
        ###a = apk.APK(fileName)
        ###d = dvm.DalvikVMFormat (a.get_dex())
        ###dx = uVMAnalysis (d)
        #self.outHandle = open (outFileName, 'a+')
        
        '''
        Handle to DataBase 
        '''
        self.dbMgr = dbMgr
        if len(category) > 250 :
            self.category  = (category[:200] + '..')
        else:
            self.category = category
        
        
        self.dirEntries = []
        self.main_package_name = ""
        
        ######self.outHandle.write ("---Package Name---\n")
        '''
        Keeping main package name within range of mysql datatype
        '''
        mpn = a.get_package()
        if len(mpn) > 250 :
            self.main_package_name  = (mpn[:200] + '..')
        else:
            self.main_package_name = mpn
            
        '''
        Keeping main package name within range of mysql datatype
        '''
        if len(noprefixfilename) > 250 :
            self.fileName  = (noprefixfilename[:200] + '..')
        else:
            self.fileName = noprefixfilename
            
        #print self.main_package_name
        
        ###self.outHandle.write(fileName)
        ###self.outHandle.write ('\n')
        self.main_package_tokens = self.GetTokens(self.main_package_name)
        
        
        packages = dx.get_tainted_packages()

        #Filtering out internal packages used for app creation     
        ex1 = re.compile ("Ljava/*")
        ex2 = re.compile ("Landroid/*")
        ex3 = re.compile (self.GetDecompiledPackageName (self.main_package_name))
        ex4 = re.compile("/google/")

        
        package_names = []

               
        
        for _, package_name in packages.get_packages():
            self.specialHandlingForGoogleSDK(package_name)
            if ex3.search (package_name) == None and ex1.search (package_name) == None and ex2.search (package_name) == None and ex4.search (package_name) == None:
                package_names.append (self.GetDirectoryName (package_name))
                #print package_name
        
        ###self.outHandle.write ("--External Packages---\n")
        self.PopulateDirEntries(package_names)
        self.GetPackages ()
        
        #self.outHandle.close()
        return self.alreadyPrinted
        
 
    '''
    Converting names with dots as separator with names with slashes
    '''       
    def GetDecompiledPackageName (self, main_package_name):
        tokens = []
        for string in main_package_name.split ('.'):
            tokens.append(string)
        
        decompiledName = 'L'
        for string in tokens:    
            decompiledName = decompiledName + string
            decompiledName = decompiledName + '/'
            
        
        #print decompiledName
        return decompiledName
    
    '''
    Song
    New method for Removing noisy characters from names
    '''
    def _GetDirectoryName(self, package_name):
        package_name = package_name.replace('/', '.')
        #remove not java characters
        package_name = package_name.translate(re.sub('[^_a-zA-Z$0-9\s\.]', '', package_name))
        return package_name
        
    '''
    Removing noisy characters from the names
    '''
    def GetDirectoryName (self, package_name):
        
        tokens = []
        i=0
        for string in package_name.split ('/'):
            if i==0:
                string = string[1:]
            tokens.append(string)
            i = i + 1
        
        lastToken = tokens.pop()
        lastToken = lastToken[:-1]
        tokens.append(lastToken)
        
        new_package_name = ""
        for string in tokens:
            new_package_name += string
            new_package_name += "."
            
        #print new_package_name
        return new_package_name
    
    def GetTokenizedEntries (self, string):
        
        tokens = []
        for name in string.split ('.'):
            dirEntry = DirStructHandler.DirEntry ()
            dirEntry.AddDirName (name)
            tokens.append(dirEntry)
                        
        return tokens
    
    def GetRootDirIfPresent (self, dirEntry):
        for entry in self.dirEntries:
            if entry.IsEqual (dirEntry) == True:
                return entry
        return None
    
    def InsertIfNotPresent (self, parent, newchild):
        children = parent.ChildRef
        if len (children) == 0:
            parent.AddChildRef (newchild)
            return True
        else:
            found = False
            for child in children :
                if child.DirName == newchild.DirName:
                    found = True
                    break
            if found == False:
                parent.AddChildRef (newchild)
            
    '''
    Creating tree structure for the directories present
    example of structure
    com (parent) dir1 (child-1) dir2 (child-2)
    org (parent) dir1 (child-1) dir2 (child-2) dir3 (child-3)
    google (parent) ...
    '''
    def PopulateDirEntries (self, package_names):
        for entry in package_names:
            #print entry
            tokens = []
            tokens = self.GetTokenizedEntries(entry)
            
            i = 0
            for dirEntryToken in tokens:
                if (len (dirEntryToken.DirName) == 0):
                    continue
                root = self.GetRootDirIfPresent (dirEntryToken)
                if i == 0 and (len(self.dirEntries) == 0 or root == None):
                    self.dirEntries.append(dirEntryToken)
                    parentDirEntry = dirEntryToken
                elif i == 0 and root != None:
                    parentDirEntry = root
                else: 
                    self.InsertIfNotPresent (parentDirEntry, dirEntryToken)
                    parentDirEntry = dirEntryToken
                i = i + 1
    
    '''
    Recursive function to print the package name / directory name based on rules (packageLevel)
    '''
    def PrintPackageNameAtLevel (self, rootEntry, packageLevel):
        if packageLevel == 1:
            self.packages.append (rootEntry.DirName)
            if (len(rootEntry.DirName) <= 3) or rootEntry.DirName.find('$')!=-1 or ('w3c' in rootEntry.DirName) or ('apache' in rootEntry.DirName) or ('xml' in rootEntry.DirName) or ('junit' in rootEntry.DirName) or ('sun' in rootEntry.DirName) or ('android' in rootEntry.DirName) or ('dalvik' in rootEntry.DirName) or ('json' in rootEntry.DirName) :
                return
            if (rootEntry.DirName in self.alreadyPrinted):
                return
            
            ex = re.compile (rootEntry.DirName)
            for maintokens in self.main_package_tokens:
                if (ex.search (maintokens) != None):
                    return
            '''
            Printing into file as well as writing into Database
            '''
            ###self.outHandle.write (str (rootEntry.DirName))
            if len(rootEntry.DirName) > 250 :
                name = (rootEntry.DirName[:200] + '..')
            else:
                name = rootEntry.DirName
            self.dbMgr.insert3rdPartyPackageInfo(self.main_package_name, self.fileName, name, self.category)
            ###self.outHandle.write ("\n")
            self.alreadyPrinted.append (rootEntry.DirName)
            return
        
        packageLevel = packageLevel - 1
        childRef = rootEntry.ChildRef
        for child in childRef:
            self.PrintPackageNameAtLevel(child, packageLevel)
           
    '''
    Before iterating through the directory structure print the top level directories based on static rules
    '''
    def PrintCommonAncestor (self, rootEntry, rules):
        ancestorLevel = rules.packageLevel;
        if ancestorLevel > 1:
            #Descend down that many levels
            self.PrintPackageNameAtLevel (rootEntry, ancestorLevel)
        elif ancestorLevel == -2: #Ignore noise
            return;
        elif ancestorLevel == 3:
            ###self.outHandle.write (str ("titanium"))
            self.dbMgr.insert3rdPartyPackageInfo (self.main_package_name, self.fileName, "titanium", self.category)
            self.alreadyPrinted.append ("titanium")
        elif ancestorLevel == 1:
            self.packages.append (rootEntry.DirName)
            '''Rule added to PackageRules'''
#            if (len(rootEntry.DirName) <= 2) or ('w3c' in rootEntry.DirName) or ('apache' in rootEntry.DirName) or ('xml' in rootEntry.DirName) or ('L' in rootEntry.DirName) or ('junit' in rootEntry.DirName) or ('sun' in rootEntry.DirName) or ('android' in rootEntry.DirName) or ('dalvik' in rootEntry.DirName) or ('json' in rootEntry.DirName) :
#                    return
            ###self.outHandle.write (str (rootEntry.DirName))
            if len(rootEntry.DirName) > 250 :
                name = (rootEntry.DirName[:200] + '..')
            else:
                name = rootEntry.DirName
            self.dbMgr.insert3rdPartyPackageInfo (self.main_package_name, self.fileName, name, self.category)
            ###self.outHandle.write ("\n")
            self.alreadyPrinted.append (rootEntry.DirName)
        else:
            #google package
            self.packages.append (self.main_package_name)
            '''Rule added to PackageRules'''
#            if (len(rootEntry.DirName) <= 2) or ('w3c' in rootEntry.DirName) or ('apache' in rootEntry.DirName) or ('xml' in rootEntry.DirName) or ('L' in rootEntry.DirName) or ('junit' in rootEntry.DirName) or ('sun' in rootEntry.DirName) or ('android' in rootEntry.DirName) or ('dalvik' in rootEntry.DirName) or ('json' in rootEntry.DirName) :
#                    return
            ###self.outHandle.write (str (self.main_package_name))
            ###self.outHandle.write ("\n")
            self.PrintPackageNameAtLevel (rootEntry, 2)
            
    def SetRules (self, rootEntry):
        rules = PackageRules.Rules (rootEntry, self.main_package_name);
        return rules
    
    '''
    Iterate through all the top level directories and print the package names
    '''
    def GetPackages (self):
        
        i = 0
        for rootEntry in self.dirEntries:
            rules = self.SetRules (rootEntry)
            self.PrintCommonAncestor (rootEntry, rules)
            
