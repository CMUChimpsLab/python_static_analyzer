'''
Created on Oct 7, 2012

@author: psachdev
'''
import DirStructHandler

class Rules:
    '''
    This class is used to create static rules. Following are rules
    All the directories starting with org or com are assigned number 2 means to be read recursively
    All the directories starting with google are assigned -1 means they shouldn't be printed
    All the directories with name length < 4 are treated as noise and are assigned number -2 (number based on analysis)
    Remaining are assigned number 1
    '''
            
    def __init__(self, rootEntry, main_package_name):
        '''
        Constructor
        '''
        self.rootName = rootEntry.DirName
        self.main_package_name = main_package_name
        self.packageLevel = 0
        self.FormRule ()
    
    def GetTokens (self, string):
           
        tokens = []
        for name in string.split ('.'):
            tokens.append(name)
                        
        return tokens
    
    def FormRule (self):
        if self.rootName == "org" or self.rootName == "Lorg":
            self.packageLevel = 2 #org.apache.*
            return
        elif self.rootName == "com" or self.rootName == "Lcom":
            tokens = self.GetTokens(self.main_package_name)
            if len(tokens) > 1 and tokens [1] == "google":
                self.packageLevel = -1 #indicating its google_apk
            else:
                self.packageLevel = 2 #com.bayview.*or com.googlex.*
        else:
            if self.rootName == "ti" or self.rootName == "Lti":
                self.packageLevel = 3
            elif self.rootName.find(';')!=-1 or self.rootName.find('$')!=-1 or (len(self.rootName) <= 3) or ('w3c' in self.rootName) or ('apache' in self.rootName) or ('xml' in self.rootName) or ('junit' in self.rootName) or ('sun' in self.rootName) or ('android' in self.rootName) or ('dalvik' in self.rootName) or ('json' in self.rootName) :
                self.packageLevel = -2 #noise
            else:
                self.packageLevel = 1
