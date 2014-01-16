#!/bin/sh

Now=$(date +"%Y%m%d%H%M")
outputPath="/home/lsuper/apk_data/log/staticAnalysis/parrallelLog/$Now"
mkdir -p $outputPath
touch $outputPath/filelist.txt
python /home/lsuper/projects/python_static_analyzer/main_LargeVM.py $outputPath 
