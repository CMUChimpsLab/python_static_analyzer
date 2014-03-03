#!/bin/bash

NOW=$(date +"%Y%m%d%H%M")
Today=$(date +"%Y%m%d")
#instanceArray stores all instance public ip
instanceArray=()
instanceArray[0]="54.81.162.94"
instanceArray[1]="54.81.210.176"
instanceArray[2]="54.81.160.59"
instanceArray[3]="54.81.86.161"
instanceArray[4]="54.81.26.126"
instanceArray[5]="54.81.226.79"
instanceArray[6]="23.22.69.238"
instanceArray[7]="54.81.91.112"
instanceArray[8]="50.16.35.192"
instanceArray[9]="54.81.5.106"
instanceArray[10]="54.205.163.87"
instanceArray[11]="54.82.46.135"
instanceArray[12]="54.197.125.2"
instanceArray[13]="54.205.202.32"
instanceArray[14]="54.81.151.110"
instanceArray[15]="54.204.180.148"
echo ${instanceArray[*]}
i=0
while [ $i -lt ${#instanceArray[@]} ]; do
  scp -i ~/20121217.pem setup.sh ubuntu@${instanceArray[$i]}:
  ssh -i ~/20121217.pem ubuntu@${instanceArray[$i]} 'sh -x ~/setup.sh'
  echo $i
  ssh -i ~/20121217.pem ubuntu@${instanceArray[$i]} "sudo mkdir -p /home/ubuntu/parrallelLog/$NOW/instance-$i/ "
  ssh -i ~/20121217.pem ubuntu@${instanceArray[$i]} "sudo touch /home/ubuntu/parrallelLog/$NOW/instance-$i/filelist.txt"
  ssh -f -i ~/20121217.pem ubuntu@${instanceArray[$i]} "screen -dm sudo python /home/ubuntu/python_static_analyzer/main_LargeVM.py /home/ubuntu/parrallelLog/$NOW/instance-$i/ /home/ubuntu/python_static_analyzer/parallelScript/notAnalyzed/$Today/instance-$i"
  let i=i+1
done

