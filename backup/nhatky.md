tan congL

hping3 -S --flood -p 80 10.0.0.5






ovs-ofctl dump-flows s1 -O OpenFlow13






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

