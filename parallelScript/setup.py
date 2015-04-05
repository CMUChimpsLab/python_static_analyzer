# Script to be run on remote machine to set it up for static analysis
# Host refers to where EBS volume is mounted (pdev)
# Remove refers to the remote machine where this script is being run

######## Config for the remote machine ########

# Number of directories storing apk
# apk0, apk1, ..., apk[NUM_APK_DIR - 1]
NUM_APK_DIR = 8

# Base path for directories storing apk on the host
# A number will be appended to the end of this path to complete the path
BASE_APK_DIR = "/home/lsuper/apk_data/apk"

# NFS port
NFS_PORT = 2049

# Path for log directory on the host
LOG_DIR = "/home/lsuper/apk_data/log/staticAnalysis/parallelLog/"

# Path for static analyzer code on the host
ANALYZER_DIR = "/home/lsuper/projects/privacyGradePipeline/python_static_analyzer/"

#where EBS volume is mounted, now is pdev instance
#Do not commit plaintext server ip to github
HOST="XXX.XXX.XXX.XXX"

######## Configuration Script ########

import subprocess 

def mountAPKDir(num):
  cmd = ("sudo mount -t nfs -o addr=%s,proto=tcp,port=%d %s:%s%d/ "
      "/home/ubuntu/apk%d") % (HOST, NFS_PORT, HOST, BASE_APK_DIR, num, num)
  subprocess.check_output(cmd, shell=True)

if __name__ == "__main__":
  # Mount all APK directories on the remote
  print "Mounting apk directories..."
  for i in xrange(0, NUM_APK_DIR):
    subprocess.call(["mkdir", "apk" + str(i)])
    mountAPKDir(i)

  # Mount remote log directory
  print "Mounting log directory..."
  subprocess.call(["mkdir", "parallelLog"])
  cmd = ("sudo mount -t nfs -o addr=%s,proto=tcp,port=%d %s:%s "
      "/home/ubuntu/parallelLog") % (HOST, NFS_PORT, HOST, LOG_DIR)
  subprocess.check_output(cmd, shell=True)

  # Mount remote static analyzer code directory
  print "Mounting static analyzer directory..."
  subprocess.call(["mkdir", "python_static_analyzer"])
  cmd = ("sudo mount -t nfs -o addr=%s,proto=tcp,port=%d %s:%s "
      "/home/ubuntu/python_static_analyzer") % (HOST, NFS_PORT, HOST, ANALYZER_DIR)
  subprocess.check_output(cmd, shell=True)

  #since we have a root image we do not need these set up
  #sudo apt-get  install nfs-common portmap
  #sudo apt-get install build-essential python-dev
  #sudo apt-get install python-setuptools
  #sudo easy_install pymongo
  #sudo apt-get install htop
