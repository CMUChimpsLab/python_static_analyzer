'''
Created on Sep 9, 2012

@author: psachdev
'''
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis.analysis import *

class StaticAnalyzer:
 
    '''
    Song
    Special Handling for Google SDK
    '''
    def specialHandlingForGoogleSDK(self, class_name):
        #src has "/" as seperator, dst has "."
        class_name = class_name.replace('/', '.')
        if (class_name.startswith('Lcom.google.analytics.') or class_name.startswith('Lcom.google.android.apps.analytics.')):
            #should do something or not for tracking
            pass
        if class_name.startswith('Lcom.google.ads'):
            return 'admob'
        return None

    def findandprint (self, packages, class_name):
        googleLib = self.specialHandlingForGoogleSDK(class_name) 
        if googleLib is not None:
            return googleLib
        for package in packages:
            if package in class_name:
                #self.outHandle.write ("\n    PackageName - ")
                #self.outHandle.write (dst_class_name)
                if len(package) > 250 :
                    pck = (package[:200] + '..')
                else:
                    pck = package
                return pck
        else:
            return "NA"
        
        
    def __init__ (self, fileName, outFileName, packages, dbMgr, noprefixfilename, a, d, dx):
        ###a = apk.APK(fileName)
        ###d = dvm.DalvikVMFormat (a.get_dex())
        ###dx = uVMAnalysis (d)
        analysis = dx.get_vm()
        cm = analysis.get_class_manager()
        
        #self.outHandle = open (outFileName, 'a+')
        '''
        Handle to Database
        '''
        self.dbMgr = dbMgr
        
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
            
        #self.outHandle.write ("\n")
        #self.outHandle.write ("---Package Name---\n")
        #print self.main_package_name
       
        
        #self.outHandle.write (fileName)
        ex3 = re.compile (self.main_package_name)
        
        '''
        Getting the permissions using dalvik analysis
        It reads the permissions from the android-manifest file
        '''
        #manifestPermissions = dbMgr.getManiFestPermissions(self.main_package_name)
        manifestPermissions = a.get_permissions()
        manifestPermissions = [permission.lstrip('android.permission.') for permission in manifestPermissions if permission.startswith('android.permission.')]
        p = dx.get_permissions( manifestPermissions )
        
        #self.outHandle.write ('\n')
        '''
        1. Loop through the permissions
        2. Get the source class & destination class of the permission
            Print the class in which the permission is used and 
            class which calls the above mentioned class
        3. Use the packages array (containing all the package names) and iterate over it to find in which
           package the class exists -- Do this for both destination & source classes
        4. In some cases only destination class will be present -- class where the permission is used and there wont 
           be corresponding source class the destination class will be under main application's directory 
        '''
        for i in p :
            #print i, ":"
            #self.outHandle.write (i)
            for path in p [i] :
                
                #self.outHandle.write ('\n')
                dst, dst_method_name, dst_descriptor = path.get_dst( cm )
                dst = dst.replace('/', '.')
                if len(dst) > 250 :
                    dst_class_name = (dst[:200] + '..')
                else:
                    dst_class_name = dst
                
                '''
                Differentiating whether external class or internal based on the tokens generated from main_package_name
                example 
                class name Lcom/whatsapp/xyzd is internal
                because 
                its under whatsapp directory which a token present the name of apk file
                '''
                """
                 path can be PathVar or PathP, PathVar only have dst, PathP have both dst and src. In my opinion, they are different ASM code, one with two argu, one with one argu
                """
                if isinstance(path, PathVar) :
                    is_external = (ex3.search(dst_class_name) == None)
                    package = self.findandprint (packages, dst_class_name)
                    dbMgr.insertPermissionInfo(self.main_package_name, self.fileName, i, is_external, dst_class_name, package, "NA")
                else:
                    src, src_method_name, src_descriptor = path.get_src( cm )
                    package = self.findandprint(packages, src)
                    if len(src) > 250 :
                        src_class_name = (src[:200] + '..')
                    else:
                        src_class_name = src
                    is_external = (ex3.search(src_class_name) == None)
                    dbMgr.insertPermissionInfo(self.main_package_name, self.fileName, i, is_external, dst_class_name, package, src_class_name)
       
