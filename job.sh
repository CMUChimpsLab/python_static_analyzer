#!/bin/sh

outputPath=$2
touch $outputPath/out/filelist.txt
numapks=`find $1 -name "*.apk" | wc -l`
apksdone=`cat $outputPath/out/filelist.txt | wc -l`
while test "$numapks" -gt "$apksdone"
do
	python main.py $1 $outputPath
	#echo "---------------------------------" >> jobout.txt
	#echo "number of apks listed :" >> jobout.txt
	#echo $numapks >> jobout.txt
	#echo "apks tested so far :" >> jobout.txt
	#echo $apksdone >> jobout.txt
	#echo "Return value of python script"  >> jobout.txt
	#echo $? >> jobout.txt
	#echo "---------------------------------" >> jobout.txt
	`tail -n 1 $outputPath/out/filelist.txt >> $outputPath/out/problemfiles.txt`
    apksdone=`cat $outputPath/out/filelist.txt | wc -l`
    echo $apksdone
    echo $numapks
done
