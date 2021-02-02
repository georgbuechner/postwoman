#!/bin/bash
path_to_configs=$(/home/fwork/Documents/programming/postwoman/configs)
path_to_configs=$(/home/fwork/Documents/programming/postwoman/configs)

file=$(find $path_to_configs -type f -name "*.yaml" | dmenu -i -l 35)
outtput=$(python3 src/schedular.py $file)
notify-send "$outtput"
nvim "${file/configs/results}"    
