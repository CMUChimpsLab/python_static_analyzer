#!/bin/sh

numapks=`find $1 -name "*.apk" | wc -l`
apksdone=`awk '{x++}END{ print x}' /home/ubuntu/out/filelist.txt`
while test $numapks!=$apksdone:
do
	returnvalue=$(python /home/ubuntu/code/staticAnalyzer/src/staticanalyzer/main.py $1)
	#echo "---------------------------------" >> jobout.txt
	#echo "number of apks listed :" >> jobout.txt
	#echo $numapks >> jobout.txt
	#echo "apks tested so far :" >> jobout.txt
	#echo $apksdone >> jobout.txt
	#echo "Return value of python script"  >> jobout.txt
	#echo $? >> jobout.txt
	#echo "---------------------------------" >> jobout.txt
	`tail -n 1 /home/ubuntu/out/filelist.txt >> /home/ubuntu/out/problemfiles.txt`
	apksdone=`awk '{x++}END{ print x}' /home/ubuntu/out/filelist.txt`
done
