#!/bin/sh

# for each round of data updating, you may do multiple rounds of static analysis, so you may not want to use a different name 
Now=$(date +"%Y%m%d%H%M")

if [ $# -lt 2 ]; then
    echo 1>&2 "$0: not enough arguments, need output path for filelist.txt"
    exit 2
fi

outputPath="$1"
if [ ! -d $outputPath ]; then
    echo 1>&2 "incorrect path provided for filelist.txt directory, should create path first"
    exit 2
fi
apkPath="$2"
if [ ! -f $apkPath ]; then
    echo 1>&2 "incorrect path provided for new_apks.txt, file should have already existed "
    exit 2
fi
echo $(pwd)
python $(pwd)/main_LargeVM.py $outputPath $apkPath
