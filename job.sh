#!/bin/sh

#Now=$(date +"%Y%m%d%H%M")
Now=$1
outputPath="/home/lsuper/apk_data/log/staticAnalysis/$Now"
mkdir -p $outputPath
python /home/lsuper/projects/privacyGradePipeline/python_static_analyzer/main_LargeVM.py $outputPath 
