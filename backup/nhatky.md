tan congL

hping3 -S --flood -p 80 10.0.0.6

sudo hping3 -S --faster -V -p 80 10.20.0.10 --rand-source

sudo nping --tcp --rate 1000 --source-ip random 10.0.0.6

hping3 -S -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.6

sudo ovs-ofctl -O OpenFlow13 dump-flows s1

sudo ovs-ofctl -O OpenFlow13 del-flows s1
sudo ovs-ofctl -O OpenFlow13 del-flows s2


s2,462.384,2894431,503627574,5e:49:c0:ed:f4:9b,d2:7d:b5:6d:68:0e,,,,,output:4,125966,21918084

 cookie=0x780000fdcd646b, duration=216.877s, table=0, n_packets=8, n_bytes=784, send_flow_rem priority=100,in_port=6,dl_src=d2:7d:b5:6d:68:0e,dl_dst=5e:49:c0:ed:f4:9b actions=output:1
 cookie=0x780000f3c336b6, duration=216.877s, table=0, n_packets=8, n_bytes=784, send_flow_rem priority=100,in_port=1,dl_src=5e:49:c0:ed:f4:9b,dl_dst=d2:7d:b5:6d:68:0e actions=output:6
 cookie=0x780000bbf0a466, duration=892.504s, table=0, n_packets=44, n_bytes=4312, send_flow_rem priority=100,in_port=6,dl_src=5e:49:c0:ed:f4:9b,dl_dst=d2:7d:b5:6d:68:0e actions=output:4
 cookie=0x7800009340583b, duration=892.504s, table=0, n_packets=44, n_bytes=4312, send_flow_rem priority=100,in_port=4,dl_src=d2:7d:b5:6d:68:0e,dl_dst=5e:49:c0:ed:f4:9b actions=output:6


docker compose stop

ONOS CLI commands

    Devices command
    Links command
    Hosts command
    Flows command
    Paths command
    Intent Command

            commands = [
                f'ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=1, dl_src={dl_src}, dl_dst={dl_dst}, actions=drop"',
                f'ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=4, dl_src={dl_dst}, dl_dst={dl_src}, actions=drop"',
                f'ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=3, dl_src={dl_dst}, dl_dst={dl_src}, actions=drop"',
                f'ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=5, dl_src={dl_src}, dl_dst={dl_dst}, actions=drop"',
            ]


cookie=0x890000da70cb83, duration=31.516s, table=0, n_packets=31, n_bytes=3038, send_flow_rem priority=10,in_port="s1-eth4",dl_src=6e:19:2a:0a:47:32,dl_dst=96:aa:47:03:a7:41 actions=output:"s1-eth1"

cookie=0x0, duration=10.903s, table=classifier, n_packets=1, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="6",dl_vlan=58,dl_vlan_pcp=0,dl_src=38:60:77:89:e6:72,dl_dst=38:60:77:89:f1:49,nw_src=10.58.0.6,nw_dst=10.58.0.5,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"5"

cookie=0x890000d427550f, duration=30.560s, table=0, n_packets=30, n_bytes=2940, send_flow_rem priority=10,in_port="s1-eth1",dl_src=96:aa:47:03:a7:41,dl_dst=6e:19:2a:0a:47:32 actions=output:"s1-eth4"

os.system("ovs-ofctl -O OpenFlow13 add-flow s1 'table=0, priority=10, in_port=s1-eth1, dl_src=22:ac:3e:77:9b:88, dl_dst=96:39:95:49:17:d0, actions=drop'")

# code mau chan port:
sudo ovs-ofctl add-flow s2 "table=0, priority=100, in_port=s2-eth1, dl_src=0a:33:f8:53:c5:21, dl_dst=8a:8d:75:e8:31:c8, nw_src=10.0.0.1, nw_dst=10.0.0.2, icmp, icmp_type=8, icmp_code=0, actions=drop"

# code chan port: can thay doi mac

# s1
# chan in_port 1:
ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=1, dl_src=A6:B9:DD:9E:05:2C, dl_dst=02:39:04:A9:52:82, actions=drop"

# chan in_port 4:
ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=4, dl_src=02:39:04:A9:52:82, dl_dst=A6:B9:DD:9E:05:2C, actions=drop"

# chan in_port 3
ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=3, dl_src=02:39:04:A9:52:82, dl_dst=A6:B9:DD:9E:05:2C, actions=drop"

# chan in_port 5
ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=5, dl_src=A6:B9:DD:9E:05:2C, dl_dst=02:39:04:A9:52:82, actions=drop"


ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=1, dl_src=A6:B9:DD:9E:05:2C, dl_dst=02:39:04:A9:52:82, actions=drop" | ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=4, dl_src=02:39:04:A9:52:82, dl_dst=A6:B9:DD:9E:05:2C, actions=drop" | ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=3, dl_src=02:39:04:A9:52:82, dl_dst=A6:B9:DD:9E:05:2C, actions=drop" | ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=5, dl_src=A6:B9:DD:9E:05:2C, dl_dst=02:39:04:A9:52:82, actions=drop" 


ovs-ofctl dump-flows s1 -O OpenFlow13


### tao traffic http
h6:
python3 -m http.server 80 &


h1:
httperf --server 10.0.0.6 --port 80 --num-conns 500 --rate 10

ovs-ofctl add-flow s1 "dl_src={attacker MAC address},actions=drop"



### khai niem MitM
Man-in-the-middle (MitM) hay tấn công xen giữa là kiểu tấn công mạng xảy ra khi kẻ tấn công bí mật chen vào giữa hai bên đang giao tiếp (thường trên trình duyệt web hoặc máy chủ web). Kẻ tấn công sẽ chặn kết nối giữa hai bên, giả danh thành nạn nhân để đánh cắp dữ liệu quan trọng.

### More about MitM
- IP Spoofing (giả mạo địa chỉ IP): Kẻ tấn công sẽ giả mạo địa chỉ IP của nạn nhân, sau đó thay thế nạn nhân để giao tiếp với đối phương. Lúc này, kẻ tấn công có thể đánh cắp toàn bộ thông tin và dữ liệu đang trao đổi.

- DNS spoofing (giả mạo DNS): Kẻ tấn công sẽ thay đổi địa chỉ website trên máy chủ DNS, khiến nạn nhân truy cập vào website giả mạo. Mục tiêu của hình thức này là thủ phạm cần tăng lượng truy cập cho website giả mạo hoặc đánh cắp thông tin đăng nhập của nạn nhân.

- HTTPS spoofing (giả mạo HTTPS): Kẻ tấn công sẽ tạo ra một kết nối HTTPS giả mạo để khiến nạn nhân nghĩ rằng họ đang kết nối với một trang web an toàn. Tuy nhiên, kết nối này thực chất không được mã hóa an toàn, kẻ tấn công sẽ theo dõi tương tác của nạn nhân ở trên website và đánh cắp các thông tin được chia sẻ.

- SSL Hijacking (đánh cắp SSL): Kẻ tấn công chặn các kết nối SSL giữa máy chủ và máy khách, sau đó mã hoá dữ liệu để đánh cắp thông tin.

- Email Hijacking (đánh cắp email): Kẻ tấn công sẽ giả mạo hoặc xâm nhập vào tài khoản email của các tổ chức, đặc biệt là tổ chức tài chính. Sau đó, gửi email cho nạn nhân, lừa nạn nhân cung cấp các thông tin quan trọng.

- WiFi Eavesdropping (nghe lén Wifi): Kẻ tấn công sẽ thiết lập một điểm truy cập Wifi giả mạo để lừa người dùng kết nối. Sau đó, chặn và đánh cắp tất cả dữ liệu được truyền đi thông qua mạng Wifi ảo Hình thức tấn công MitM này thường xảy ra ở những điểm Wifi miễn phí hoặc Wifi công cộng, khi kẻ tấn công truy cập được bộ định tuyến Wifi.

- Stealing Browser Cookies (Ăn cắp trình duyệt cookie): Kẻ tấn công sẽ đánh cắp cookie của trình duyệt - nơi lưu trữ thông tin các phiên trình duyệt của nạn nhân. Thông qua đó, truy cập vào các tài khoản trực tiếp của nạn nhân mà không cần mật khẩu hoặc đánh cắp những thông tin quan trọng khác.

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

T = 1
dst_ip_target = '10.0.0.5'

packets_csv = np.genfromtxt('data/packets.csv', delimiter=",")
sdfp = np.std(packets_csv)

bytes_csv = np.genfromtxt('data/bytes.csv', delimiter=",")
sdfb = np.std(bytes_csv)

#rsip
df = pd.read_csv('data/flows.csv', header=None, names=["timestamp", "srcIP", "dstIP"])
max_time = df["timestamp"].max()
start_time = max_time - T

df_rsip = df[(df["dstIP"] == dst_ip_target) & (df["timestamp"] >= start_time)]
rsip = df_rsip["srcIP"].nunique() / T

#rfes
df_recent = df[df["timestamp"] >= start_time]
rfes = len(df_recent) / T

#rpfes
flows_set = set(zip(df["srcIP"], df["dstIP"]))
reverse_set = set((b, a) for (a, b) in flows_set)
interactive_pairs = flows_set & reverse_set
interactive_ips = set(ip for pair in interactive_pairs for ip in pair)

total_ips = set(df["srcIP"]).union(set(df["dstIP"]))
rpfes = len(interactive_ips) / len(total_ips) if total_ips else 0

######-header-######
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


# back up computeFeatures
```python
import numpy as np
import csv
import os

T = 1  # 1s
w = [[ 3.84717557e-07,  2.21100421e-09, -7.26798815e-14]]
b = [-1.00001757]

# SDFP
packets_csv = np.genfromtxt('data/packets.csv', delimiter=",")
dt_packets = packets_csv
sdfp = np.std(dt_packets)

# SDFB
bytes_csv = np.genfromtxt('data/bytes.csv', delimiter=",")
dt_bytes = bytes_csv
sdfb = np.std(dt_bytes)

# SFE: number of flow entries / time interval (tăng từng cái một)
with open('data/dataset.csv', newline='') as f:
    reader = csv.reader(f)
    flows = list(reader)
n_flows = len(flows)
sfe = n_flows // T

# RPF
# Đọc file và trích dl_src, dl_dst
mac_pairs = []
with open('data/dataset.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dl_src = row["dl_src"]
        dl_dst = row["dl_dst"]
        if dl_src and dl_dst:
            mac_pairs.append((dl_src, dl_dst))

# Tính Pair_Sum
pair_set = set()
pair_sum = 0
for a, b in mac_pairs:
    if (b, a) in pair_set:
        pair_sum += 1
    else:
        pair_set.add((a, b))

# Tính RPF
n_flows = len(mac_pairs)
rpf = (2 * pair_sum) / n_flows if n_flows > 0 else 0

# Headers và feature chỉ còn sdfb, sdfp, và sfe
headers = ["SDFB", "SDFP", "SFE", "RPF"]

# 0 = Normal, 1 = DDoS
x_new = np.array([sdfb, sdfp, rpf])
z = np.dot(w, x_new) + b
label = 1 if z >= 0 else 0

label = 1  # Nếu bạn đang xử lý normal traffic, đổi thành 1 cho DDoS

features = [sdfb, sdfp, sfe, rpf]

# Ghi vào file CSV
file_exists = os.path.isfile('data/features-file.csv')
file_path = {
    0: "datasets/dataset_normal.csv",  # Normal traffic
    1: "datasets/dataset_ddos.csv"    # DDoS traffic
}[label]

# Ghi vào file tương ứng với label
with open(file_path, 'a', newline='') as f:
    cursor = csv.writer(f, delimiter=",")
    if not file_exists:
        cursor.writerow(headers + ["LABEL"])  # Ghi header nếu lần đầu
    cursor.writerow(features + [label])  # Thêm nhãn vào cuối

# Cập nhật realtime.csv với features
with open('data/realtime.csv', 'w') as f:
    cursor = csv.writer(f, delimiter=",")
    cursor.writerow(headers)
    cursor.writerow(features)

```


drop

sudo ovs-ofctl add-flow s2 "table=0, priority=100, in_port=s2-eth1, dl_src=0a:33:f8:53:c5:21, dl_dst=8a:8d:75:e8:31:c8, nw_src=10.0.0.1, nw_dst=10.0.0.2, icmp, icmp_type=8, icmp_code=0, actions=drop"

cookie=0x8900008644c898, duration=28.968s, table=0, n_packets=495629, n_bytes=86237622, send_flow_rem priority=10,in_port="s1-eth1",dl_src=22:ac:3e:77:9b:88,dl_dst=96:39:95:49:17:d0 actions=output:"s1-eth4"

cookie=0x890000a3cd7abf, duration=24.414s, table=0, n_packets=23, n_bytes=2254, send_flow_rem priority=10,in_port="s1-eth4",dl_src=96:39:95:49:17:d0,dl_dst=22:ac:3e:77:9b:88 actions=output:"s1-eth1"

sudo ovs-ofctl -O OpenFlow13 add-flow s1 'table=0, priority=10, in_port=s1-eth1, dl_src=22:ac:3e:77:9b:88, dl_dst=96:39:95:49:17:d0, actions=drop'

cookie=0x8900008644c898, duration=17.213s, table=0, n_packets=3037756, n_bytes=528569544, send_flow_rem priority=10,in_port="s1-eth1",dl_src=22:ac:3e:77:9b:88,dl_dst=96:39:95:49:17:d0 actions=output:"s1-eth4"

chuong 4: 
bieu do trung binh packet , bytes trong 1 thoi gian (khi dang tu normal sang ddos)

bieu thay doi cua ca features

chup anh topo

chup anh before - after

chup anh mitigate thanh cong

chuong 5:
-> bieu do accurency test ai


- nghi cach viet bao cao (Hoi Cuong)
