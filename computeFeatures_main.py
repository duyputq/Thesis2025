import numpy as np
import csv
import os
import subprocess
T = 1  # 1s thời gian lấy mẫu


# ==== SDFP: Độ lệch chuẩn số gói ====
packets_csv = np.genfromtxt('data/packets.csv', delimiter=",", dtype=float)
sdfp = float(np.std(packets_csv))

# ==== SDFB: Độ lệch chuẩn số byte ====
bytes_csv = np.genfromtxt('data/bytes.csv', delimiter=",", dtype=float)
sdfb = float(np.std(bytes_csv))

# ==== SFE: Số flow entries / T ====
with open('data/dataset.csv', newline='') as f:
    reader = csv.reader(f)
    flows = list(reader)
n_flows = len(flows)
sfe = n_flows // T  # làm tròn xuống

# ==== RPF: Reverse Pair Frequency ====
mac_pairs = []
with open('data/dataset.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dl_src = row.get("dl_src")
        dl_dst = row.get("dl_dst")
        if dl_src and dl_dst:
            mac_pairs.append((dl_src.strip(), dl_dst.strip()))

# Tính số lượng cặp đảo ngược
pair_set = set()
pair_sum = 0
for a, b in mac_pairs:
    if (b, a) in pair_set:
        pair_sum += 1
    else:
        pair_set.add((a, b))

n_mac_flows = len(mac_pairs)
rpf = (2 * pair_sum) / n_mac_flows if n_mac_flows > 0 else 0


################SVM###########################

# ==== Phân loại thủ công với SVM tuyến tính ====
# x_new = np.array([float(sdfb), float(sdfp), float(rpf)], dtype=float)
# x_new = x_new.astype(float)  # Đảm bảo chắc chắn kiểu float64
w = np.array([[ 3.84717557e-07,  2.21100421e-09, -7.26798815e-14]])
b = -1.00001757

x_new = np.array([sdfb, sdfp, rpf])

z = np.dot(w, x_new) + b
label = 1 if z >= 0 else 0

import subprocess
import re

if label == 1:
    print("Detected DDOS Traffic", end=" - ")
    try:
        # Run command to get flow entries with in_port=1 on switch s1
        cmd = "sudo ovs-ofctl -O OpenFlow13 dump-flows s1 | grep in_port=1"
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        # Extract dl_src and dl_dst using regex
        dl_src_match = re.search(r'dl_src=([0-9a-fA-F:]+)', output)
        dl_dst_match = re.search(r'dl_dst=([0-9a-fA-F:]+)', output)

        if dl_src_match and dl_dst_match:
            dl_src = dl_src_match.group(1)
            dl_dst = dl_dst_match.group(1)

            commands = [
                f'ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=1, dl_src={dl_src}, dl_dst={dl_dst}, actions=drop"',
                f'ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=4, dl_src={dl_dst}, dl_dst={dl_src}, actions=drop"',
                f'ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=3, dl_src={dl_dst}, dl_dst={dl_src}, actions=drop"',
                f'ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=5, dl_src={dl_src}, dl_dst={dl_dst}, actions=drop"',
            ]

            processes = [subprocess.Popen(cmd, shell=True) for cmd in commands]
           
            print("Mitigated DDOS Traffic Successfully!")
        else:
            print("Failed to extract dl_src or dl_dst.")

    except subprocess.CalledProcessError as e:
        print("Error while executing ovs-ofctl command:", e)
else:
    print("Normal Traffic")


# ==== Ghi đặc trưng và nhãn ====
headers = ["SDFB", "SDFP", "SFE", "RPF", "LABEL"]
features = [sdfb, sdfp, sfe, rpf, label]

# Ghi nối vào file features
features_path = 'data/features-file.csv'
file_exists = os.path.isfile(features_path)
with open(features_path, 'a', newline='') as f:
    cursor = csv.writer(f)
    if not file_exists:
        cursor.writerow(headers)
    cursor.writerow(features)

# Ghi dữ liệu hiện tại ra file realtime (đè)
with open('data/realtime.csv', 'w', newline='') as f:
    cursor = csv.writer(f)
    cursor.writerow(headers)
    cursor.writerow(features)
