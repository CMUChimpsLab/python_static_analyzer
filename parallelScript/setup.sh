
mkdir apk0
mkdir apk1
mkdir apk2
mkdir apk3
mkdir parrallelLog
mkdir python_static_analyzer

sudo mount -t nfs -o addr=54.204.168.124,proto=tcp,port=2049 54.204.168.124:/home/lsuper/apk_data/apk0/ /home/ubuntu/apk0
sudo mount -t nfs -o addr=54.204.168.124,proto=tcp,port=2049 54.204.168.124:/home/lsuper/apk_data/apk1/ /home/ubuntu/apk1
sudo mount -t nfs -o addr=54.204.168.124,proto=tcp,port=2049 54.204.168.124:/home/lsuper/apk_data/apk2/ /home/ubuntu/apk2
sudo mount -t nfs -o addr=54.204.168.124,proto=tcp,port=2049 54.204.168.124:/home/lsuper/apk_data/apk3/ /home/ubuntu/apk3
sudo mount -t nfs -o addr=54.204.168.124,proto=tcp,port=2049 54.204.168.124:/home/lsuper/apk_data/log/staticAnalysis/parrallelLog/ /home/ubuntu/parrallelLog
sudo mount -t nfs -o addr=54.204.168.124,proto=tcp,port=2049 54.204.168.124:/home/lsuper/projects/privacyGradePipeline/python_static_analyzer/ /home/ubuntu/python_static_analyzer

#since we have a root image we do not need these set up
#sudo apt-get  install nfs-common portmap
#sudo apt-get install build-essential python-dev
#sudo apt-get install python-setuptools
#sudo easy_install pymongo
#sudo apt-get install htop
