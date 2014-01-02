#!/bin/bash

Now=$(date +"%Y%m%d%H%M")
instanceArray=()
instanceArray[0]="107.21.81.1"
instanceArray[1]="23.22.186.26"
instanceArray[2]="54.197.37.209"
instanceArray[3]="54.224.161.251"
instanceArray[4]="54.242.65.112"
instanceArray[5]="54.211.186.140"
instanceArray[6]="50.17.83.188"
instanceArray[7]="174.129.138.255"
instanceArray[8]="54.211.90.236"
instanceArray[9]="54.224.13.49"
instanceArray[10]="54.224.63.211"
instanceArray[11]="54.204.206.10"
instanceArray[12]="54.211.92.26"
instanceArray[13]="75.101.177.22"
instanceArray[14]="54.204.236.46"
instanceArray[15]="54.205.35.222"
echo ${instanceArray[*]}
i=0
while [ $i -lt ${#instanceArray[@]} ]; do
  scp -i ~/20121217.pem parallelScript/setup.sh ubuntu@${instanceArray[$i]}:
  ssh -i ~/20121217.pem ubuntu@${instanceArray[$i]} 'sh -x ~/setup.sh'
  let "index = $i % 2 + 1"
  echo $i
  ssh -i ~/20121217.pem ubuntu@${instanceArray[$i]} "sudo mkdir /home/ubuntu/parrallelLog/apk$index/instance-$i-$Now/ "
  ssh -i ~/20121217.pem ubuntu@${instanceArray[$i]} "sudo touch /home/ubuntu/parrallelLog/apk$index/instance-$i-$Now/filelist.txt"
  ssh -f -i ~/20121217.pem ubuntu@${instanceArray[$i]} "screen -dm sudo python /home/ubuntu/python_static_analyzer/main_LargeVM.py /home/ubuntu/apk$index/androidApp/app_201311260117 /home/ubuntu/parrallelLog/apk$index/instance-$i-$Now/ /home/ubuntu/python_static_analyzer/parallelScript/$index-notAnalyzed-$i"
  
  let i=i+1
done

