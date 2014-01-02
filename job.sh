#!/bin/sh

outputPath=$2/$Now
mkdir -p $outputPath
echo $1 > $outputPath/inputDir.txt
touch $outputPath/filelist.txt
#numapks=`find $1 -name "*.apk" | wc -l`
#apksdone=`cat $outputPath/filelist.txt | wc -l`
#while test "$numapks" -gt "$apksdone"
#do
	python main.py $1 $outputPath
	#echo "---------------------------------" >> jobout.txt
	#echo "number of apks listed :" >> jobout.txt
	#echo $numapks >> jobout.txt
	#echo "apks tested so far :" >> jobout.txt
	#echo $apksdone >> jobout.txt
	#echo "Return value of python script"  >> jobout.txt
	#echo $? >> jobout.txt
	#echo "---------------------------------" >> jobout.txt
#	`tail -n 1 $outputPath/filelist.txt >> $outputPath/problemfiles.txt`
#    apksdone=`cat $outputPath/filelist.txt | wc -l`
#    echo $apksdone
#    echo $numapks
#done
