#!/bin/bash

declare -A seen_sizes

while IFS= read -r line; do
    size=$(echo "$line" | grep -oP 'Words: \K\d+')
    if [[ -z "${seen_sizes[$size]}" ]]; then
        echo "$line"
        seen_sizes[$size]=1
    fi
done
