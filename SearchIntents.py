'''
Created on Oct 24, 2012

@author: psachdev
'''
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis.analysis import *

class Intents:
    '''
    1. Create a regular expression to filter out http links
    2. Get the list of the tainted strings used in apk using dalvik analysis
    3. Apply the filter to every entry read if it matched the regular expression then print it in file
    4. Using the package array containing list of all packages found in apk print the corresponding package in which link is formed
       This is using Path Variable analysis
       When you read the tainted string you also the address at which its present 
       Use that address to get the class name
       and then see under which package that class name belongs
    '''

    def findandprint (self, packages, dst_class_name):
        for package in packages:
            if package in dst_class_name:
                ###self.outHandle.write ("\n    PackageName - ")
                ###self.outHandle.write (package)
                return package
        return "NA"
                
    def __init__(self, infile, outfile, packages, dbMgr, noprefixfilename, a, d, dx):
        '''
        Constructor
        '''
        ###a = apk.APK(infile)
        ###d = dvm.DalvikVMFormat (a.get_dex())
        ###dx = uVMAnalysis (d)
        
        #self.outHandle = open (outfile, 'a+')
        
        ex1 = re.compile ("http://")
        mpn = a.get_package()
        '''
        Keeping main package name within range of mysql datatype
        '''
        if len(mpn) > 250 :
            self.main_package_name  = (mpn[:200] + '..')
        else:
            self.main_package_name = mpn
                                        
        
        ###self.outHandle.write ("\n")
        ###self.outHandle.write ("---Package Name---\n")
        #print self.main_package_name
        
        
        '''
        Keeping main package name within range of mysql datatype
        '''
        if len(noprefixfilename) > 250 :
            self.fileName  = (noprefixfilename[:200] + '..')
        else:
            self.fileName = noprefixfilename
        
        ###self.outHandle.write(infile)
        ex3 = re.compile (self.main_package_name)
        
        self.dbMgr = dbMgr
        #print 'URL - '
        x = dx.get_tainted_variables().get_strings()
        analysis = dx.get_vm()
        #cm = analysis.get_class_manager()
        ###self.outHandle.write ('\n')
        
        for full in x:
            s,_ = full
            string = repr(s.get_info())
            if ex1.search (string) != None:
                paths = s.get_paths()
               
                for path in paths:
                    m_idx = path[1]
                    method = analysis.get_cm_method( m_idx )
                    ###self.outHandle.write ("   %s->%s %s" % (method[0], method[1], method[2][0] + method[2][1]))
                    
                    '''
                    Keeping external package within range of mysql datatype
                    '''
                    xpackage = self.findandprint (packages, method[0])
                    if len(xpackage) > 250 :
                            xpck = (xpackage[:200] + '..')
                    else:
                            xpck = xpackage
                        
    
                    '''
                    Keeping destination class within range of mysql datatype
   		              '''                 
                    if len(method[0]) > 250 :
                            dst = (method[0][:200] + '..')
                    elif method[0].find('$')!=-1 :
                            dst = "NA"
                    else:
                            dst = method[0]
                    
                                    
                    #print method
                    if ex3.search(method[0]) != None:
                        _,linkStr = full
                        #print " APP - ", link
                        for link in re.findall("http://[\S]+", linkStr):
                            if ('.png' in link)  or ('127.0.0.1' in link) or ('www.w3.org' in link):
                                continue
                            ###self.outHandle.write ("   APP - ")
                            ###self.outHandle.write (link)
                            ###self.outHandle.write ('\n')
                            if len(link) > 250 :
                                strlink = (link[:200] + '..')
                            else:
                                strlink = link
                                
                            self.dbMgr.insertLinkInfo(self.main_package_name, self.fileName, strlink, False, dst, xpck)
                    else:
                        _,linkStr = full
                        #print "EXTERNAL - ", link
                        for link in re.findall("http://[\S]+", linkStr):
                            if ('.png' in link)  or ('127.0.0.1' in link) or ('www.w3.org' in link):
                                continue
                            ###self.outHandle.write ("   EXTERNAL - ")
                            ###self.outHandle.write (link)
                            ###self.outHandle.write ('\n')
                            if len(link) > 250 :
                                strlink = (link[:200] + '..')
                            else:
                                strlink = link      
                                                   
                            self.dbMgr.insertLinkInfo(self.main_package_name, self.fileName, strlink, True, dst, xpck)
                            
                    #access, idx = path[0]    
                    ###self.outHandle.write ('\n\n')
        #self.outHandle.close()
        
