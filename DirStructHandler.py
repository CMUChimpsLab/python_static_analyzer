'''
Created on Oct 7, 2012

@author: psachdev
'''

class DirEntry:
    '''
    This structure is used to hold references to subdirectories
    The tree formed in namespackeanalyzer used this structure to hold
    node information
    '''
        
    def __init__(self):
        '''
        Constructor
        '''
        self.DirName = ""
        self.ChildRef = []
        
    def AddDirName (self, name):
        self.DirName = name
    
    def AddChildRef (self, ref):
        self.ChildRef.append(ref)
    
    def IsRefPresent (self, refName):
        for name in self.ChildRef:
            if name.DirName == refName:
                return True
            else:
                return False
    def IsEqual (self, ref):
        if ref.DirName == self.DirName:
            return True
        else :
            return False