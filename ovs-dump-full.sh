#!/bin/bash

output_file="data/dataset.csv"
switches=("s1" "s2" "s3")

echo "switch,duration,n_packets,n_bytes,dl_src,dl_dst,nw_src,nw_dst,tp_src,tp_dst,actions" > "$output_file"

while true; do
    for switch in "${switches[@]}"; do
        ovs-ofctl dump-flows "$switch" -O OpenFlow13 | while read -r line; do
            duration=$(echo "$line" | grep -oP "duration=\K[0-9\.]+")
            n_packets=$(echo "$line" | grep -oP "n_packets=\K[0-9]+")
            n_bytes=$(echo "$line" | grep -oP "n_bytes=\K[0-9]+")
            dl_src=$(echo "$line" | grep -oP "dl_src=\K[0-9a-fA-F:]+")
            dl_dst=$(echo "$line" | grep -oP "dl_dst=\K[0-9a-fA-F:]+")
            nw_src=$(echo "$line" | grep -oP "nw_src=\K[0-9\.]+")
            nw_dst=$(echo "$line" | grep -oP "nw_dst=\K[0-9\.]+")
            tp_src=$(echo "$line" | grep -oP "tp_src=\K[0-9]+")
            tp_dst=$(echo "$line" | grep -oP "tp_dst=\K[0-9]+")
            actions=$(echo "$line" | grep -oP "actions=\K[^ ]+")

            if [[ -n "$dl_src" && -n "$dl_dst" ]]; then
                echo "$switch,$duration,$n_packets,$n_bytes,$dl_src,$dl_dst,$nw_src,$nw_dst,$tp_src,$tp_dst,$actions" >> "$output_file"
            fi
        done
    done
    sleep 1
done
