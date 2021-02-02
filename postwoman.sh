#!/bin/bash
path_to_scheduler=$(/home/fux/Documents/programming/postwoman/src/scheduler.py)
path_to_configs=$(/home/fux/Documents/programming/postwoman/configs)

file=$(find $path_to_scheduler -type f -name "*.yaml" | dmenu -i -l 35)
outtput=$(python3 $path_to_scheduler $file)
notify-send "$outtput"
nvim "${file/configs/results}"    
