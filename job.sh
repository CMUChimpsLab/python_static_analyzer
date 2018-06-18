#!/bin/sh

# for each round of data updating, you may do multiple rounds of static analysis, so you may not want to use a different name
Now=$(date +"%Y%m%d%H%M")
outputPath="/home/abraham/new_pipeline/staticAnalysis/$Now"
mkdir -p $outputPath
python2.7 /home/abraham/"Anyone_Analyze_Apps"/python_static_analyzer/main_LargeVM.py \
    $outputPath \
    /home/abraham/new_pipeline/new_apks.txt
