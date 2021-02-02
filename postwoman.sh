#!/bin/bash

file=$(find $path_to_scheduler -type f -name "*.yaml" | dmenu -i -l 35)
outtput=$(python3 $path_to_scheduler $file)
notify-send "$outtput"
nvim "${file/configs/results}"    
