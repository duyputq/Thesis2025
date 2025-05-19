#!/bin/bash

packets_file="data/packets.csv"
bytes_file="data/bytes.csv"
output_file="data/dataset.csv"
feature_file="data/features-file.csv"
mac_src_file="data/mac-src.csv"
duration_file="data/duration.csv"
switches=("s1" "s2" "s3" "s4" "s5" "s6" "s7" "s8")

> "$output_file"
> "$packets_file"
> "$bytes_file"
> "$feature_file"
> "$mac_src_file"
> "$duration_file"

declare -A prev_packets
declare -A prev_bytes

echo "switch,duration,n_packets,n_bytes,dl_src,dl_dst,nw_src,nw_dst,tp_src,tp_dst,actions,packets_per_s,bytes_per_s" > "$output_file"

while true; do
    for switch in "${switches[@]}"; do
        while read -r line; do
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
               
                flow_key="${dl_src}_${dl_dst}_${nw_src}_${nw_dst}_${tp_src}_${tp_dst}_${actions}"
                prev_p=${prev_packets["${switch}_$flow_key"]}
                prev_b=${prev_bytes["${switch}_$flow_key"]}

                if [[ -n "$prev_p" && -n "$prev_b" ]]; then
                    packets_per_s=$(( n_packets - prev_p ))
                    bytes_per_s=$(( n_bytes - prev_b ))
                    ((packets_per_s < 0)) && packets_per_s=0
                    ((bytes_per_s < 0)) && bytes_per_s=0
                else
                    packets_per_s=$n_packets
                    bytes_per_s=$n_bytes
                fi

                echo "$switch,$duration,$n_packets,$n_bytes,$dl_src,$dl_dst,$nw_src,$nw_dst,$tp_src,$tp_dst,$actions,$packets_per_s,$bytes_per_s" >> "$output_file"
                echo "$packets_per_s" >> "$packets_file"
                echo "$bytes_per_s" >> "$bytes_file"
                echo "$dl_src" >> "$mac_src_file"
                echo "$duration" >> "$duration_file"

                prev_packets["${switch}_$flow_key"]=$n_packets
                prev_bytes["${switch}_$flow_key"]=$n_bytes
            fi
        done < <(ovs-ofctl dump-flows "$switch" -O OpenFlow13)
    done
    
    # python3 computeFeatures_scale.py
    python3 test-scale.py

    sleep 0.0001
done
