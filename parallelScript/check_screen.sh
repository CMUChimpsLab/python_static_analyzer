name=$1
ssh -i ~/20121217.pem ubuntu@$1 "screen -ls" > "isRunning.txt"