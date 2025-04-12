tan congL

hping3 -S --flood -p 80 10.0.0.5






ovs-ofctl dump-flows s1 -O OpenFlow13


### tao traffic http
h6:
python3 -m http.server 80 &


h1:
httperf --server 10.0.0.6 --port 80 --num-conns 500 --rate 10



### ovs-dump.sh

```bash
#!/bin/bash

output_file="data/dump-flows.csv"
switches=("s1" "s2" "s3")

# Ghi header vào file CSV
echo "switch,duration,n_packets,n_bytes,dl_src,dl_dst" > "$output_file"

while true; do
    for switch in "${switches[@]}"; do
        # Dump flows từ switch và lọc thông tin cần thiết
        ovs-ofctl dump-flows "$switch" -O OpenFlow13 | grep "dl_src=" | while read -r line; do
            duration=$(echo "$line" | grep -oP "duration=\K[0-9\.]+")
            n_packets=$(echo "$line" | grep -oP "n_packets=\K[0-9]+")
            n_bytes=$(echo "$line" | grep -oP "n_bytes=\K[0-9]+")
            dl_src=$(echo "$line" | grep -oP "dl_src=\K[0-9a-fA-F:]+")
            dl_dst=$(echo "$line" | grep -oP "dl_dst=\K[0-9a-fA-F:]+")

            # Chỉ ghi lại nếu cả dl_src và dl_dst tồn tại
            if [[ -n "$dl_src" && -n "$dl_dst" ]]; then
                echo "$switch,$duration,$n_packets,$n_bytes,$dl_src,$dl_dst" >> "$output_file"
            fi
        done
    done
    sleep 1
done
```


### ovs-dump2.sh
```bash
#!/bin/bash

output_file="data/dataset.csv"
switches=("s1" "s2" "s3")

echo "switch,duration,n_packets,n_bytes,dl_src,dl_dst,nw_src,nw_dst,tp_src,tp_dst,actions,packets_per_s,bytes_per_s" > "$output_file"

# Lưu giá trị trước đó
declare -A prev_packets
declare -A prev_bytes

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
                # Khóa định danh flow
                flow_key="${switch}_${dl_src}_${dl_dst}_${nw_src}_${nw_dst}_${tp_src}_${tp_dst}_${actions}"

                # Lấy giá trị trước
                prev_p=${prev_packets["$flow_key"]}
                prev_b=${prev_bytes["$flow_key"]}

                # Tính toán
                if [[ -n "$prev_p" && -n "$prev_b" ]]; then
                    packets_per_s=$(( n_packets - prev_p ))
                    bytes_per_s=$(( n_bytes - prev_b ))
                    ((packets_per_s < 0)) && packets_per_s=0
                    ((bytes_per_s < 0)) && bytes_per_s=0
                else
                    packets_per_s=$n_packets
                    bytes_per_s=$n_bytes
                fi

                # Ghi dòng dữ liệu
                echo "$switch,$duration,$n_packets,$n_bytes,$dl_src,$dl_dst,$nw_src,$nw_dst,$tp_src,$tp_dst,$actions,$packets_per_s,$bytes_per_s" >> "$output_file"

                # Lưu lại
                prev_packets["$flow_key"]=$n_packets
                prev_bytes["$flow_key"]=$n_bytes
            fi
        done < <(ovs-ofctl dump-flows "$switch" -O OpenFlow13)
    done
    sleep 1
done

```

doc cai nay

```python
import numpy as np
import pandas as pd
import csv
import os

T = 10
dst_ip_target = '10.0.0.5'

packets_csv = np.genfromtxt('data/packets.csv', delimiter=",")
sdfp = np.std(packets_csv)

bytes_csv = np.genfromtxt('data/bytes.csv', delimiter=",")
sdfb = np.std(bytes_csv)

df = pd.read_csv('data/flows.csv', header=None, names=["timestamp", "srcIP", "dstIP"])
max_time = df["timestamp"].max()
start_time = max_time - T

df_rsip = df[(df["dstIP"] == dst_ip_target) & (df["timestamp"] >= start_time)]
rsip = df_rsip["srcIP"].nunique() / T

df_recent = df[df["timestamp"] >= start_time]
rfes = len(df_recent) / T

flows_set = set(zip(df["srcIP"], df["dstIP"]))
reverse_set = set((b, a) for (a, b) in flows_set)
interactive_pairs = flows_set & reverse_set
interactive_ips = set(ip for pair in interactive_pairs for ip in pair)

total_ips = set(df["srcIP"]).union(set(df["dstIP"]))
rpfes = len(interactive_ips) / len(total_ips) if total_ips else 0

headers = ["SDFB", "SDFP", "RSIP", "RFES", "RPFES"]
features = [sdfb, sdfp, rsip, rfes, rpfes]

output_file = 'data/features-file.csv'
file_exists = os.path.isfile(output_file)

with open(output_file, 'a') as f:
    cursor = csv.writer(f, delimiter=",")
    if not file_exists:
        cursor.writerow(headers)
    cursor.writerow(features)

with open('data/realtime.csv', 'w') as f:
    cursor = csv.writer(f, delimiter=",")
    cursor.writerow(headers)
    cursor.writerow(features)

print("Features computed and saved successfully.")
```