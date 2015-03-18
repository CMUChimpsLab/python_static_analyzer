#!/bin/bash
NOW=$(date +"%Y%m%d%H%M")
Today=$(date +"%Y%m%d")

#instanceArray stores all instance public ip
instanceArray=()
instanceArray[0]="54.235.49.118"
instanceArray[1]="54.92.183.22"
instanceArray[2]="54.167.30.173"
instanceArray[3]="54.237.223.255"
instanceArray[4]="174.129.94.2"
instanceArray[5]="23.20.91.42"
instanceArray[6]="54.87.16.122"
instanceArray[7]="54.162.130.227"
instanceArray[8]="54.161.119.5"
instanceArray[9]="107.21.190.90"
instanceArray[10]="54.83.226.233"
instanceArray[11]="54.162.5.77"
instanceArray[12]="54.81.70.144"
instanceArray[13]="54.82.3.79"
instanceArray[14]="54.162.63.130"
instanceArray[15]="54.198.136.8"
echo ${instanceArray[*]}

i=0
while [ $i -lt ${#instanceArray[@]} ]; do
  scp -i ~/20121217.pem setup.py ubuntu@${instanceArray[$i]}:
  ssh -i ~/20121217.pem ubuntu@${instanceArray[$i]} "python ~/setup.py"
  echo $i
  ssh -i ~/20121217.pem ubuntu@${instanceArray[$i]} "sudo mkdir -p /home/ubuntu/parallelLog/$NOW/instance-$i/ "
  ssh -i ~/20121217.pem ubuntu@${instanceArray[$i]} "sudo touch /home/ubuntu/parallelLog/$NOW/instance-$i/filelist.txt"
  ssh -f -i ~/20121217.pem ubuntu@${instanceArray[$i]} "screen -dm sudo python /home/ubuntu/python_static_analyzer/main_LargeVM.py /home/ubuntu/parallelLog/$NOW/instance-$i/ /home/ubuntu/python_static_analyzer/parallelScript/notAnalyzed/$Today/instance-$i"
  let i=i+1
done

