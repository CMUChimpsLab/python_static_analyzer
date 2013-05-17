#!/bin/sh

numapks=`cat /home/ubuntu/out/problemfiles_forLargeVM.txt | wc -l`
apksdone=`awk '{x++}END{ print x}' /home/ubuntu/out/filelist_forLargeVM.txt`
#while test $numapks!=$apksdone:
#do
	returnvalue=$(python /home/ubuntu/code/staticAnalyzer/src/staticanalyzer/main_LargeVM.py $1)
	#echo "---------------------------------" >> jobout.txt
	#echo "number of apks listed :" >> jobout.txt
	echo $numapks
	#echo "apks tested so far :" >> jobout.txt
	echo $apksdone
	#echo "Return value of python script"  >> jobout.txt
	#echo $? >> jobout.txt
	#echo "---------------------------------" >> jobout.txt
	`tail -n 1 /home/ubuntu/out/filelist_forLargeVM.txt >> /home/ubuntu/out/problemfiles.txt`
	#x=0
	apksdone=`awk '{x++}END{ print x}' /home/ubuntu/out/filelist_forLargeVM.txt`
#done
