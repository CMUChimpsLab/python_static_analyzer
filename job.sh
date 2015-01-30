#!/bin/sh

# for each round of data updating, you may do multiple rounds of static analysis, so you may not want to use a different name 
Now=$(date +"%Y%m%d%H%M")
outputPath="/home/lsuper/apk_data/log/staticAnalysis/$Now"
mkdir -p $outputPath
python /home/lsuper/projects/privacyGradePipeline/python_static_analyzer/main_LargeVM.py $outputPath 
