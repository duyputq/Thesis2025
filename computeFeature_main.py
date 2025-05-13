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
        switches = ['s1', 's2', 's3']
        commands = []

        def extract_flow_info(output):
            dl_src = re.search(r'dl_src=([0-9a-fA-F:]+)', output)
            dl_dst = re.search(r'dl_dst=([0-9a-fA-F:]+)', output)
            in_port = re.search(r'in_port=(\d+)', output)
            if dl_src and dl_dst and in_port:
                return dl_src.group(1), dl_dst.group(1), in_port.group(1)
            return None, None, None

        for sw in switches:
            for line_num in [1, 2]: 
                cmd = f"""ovs-ofctl -O OpenFlow13 dump-flows {sw} | awk '{{match($0, /n_bytes=([0-9]+)/, b); match($0, /duration=([0-9.]+)/, d); if (b[1] != "" && d[1] != "" && b[1]/d[1] > 10) print $0}}' | grep in_port | sed -n '{line_num}p'"""
                try:
                    output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
                    if output:
                        dl_src, dl_dst, in_port = extract_flow_info(output)
                        if dl_src and dl_dst and in_port:
                            cmd_drop = f'ovs-ofctl -O OpenFlow13 add-flow {sw} "table=0, priority=100, in_port={in_port}, dl_src={dl_src}, dl_dst={dl_dst}, actions=drop"'
                            commands.append(cmd_drop)
                except subprocess.CalledProcessError:
                    continue  

        if commands:
            for cmd in commands:
                subprocess.Popen(cmd, shell=True)
            print("Mitigated DDOS Traffic Successfully!")
        else:
            print("Failed to extract necessary information (in_ports or MACs).")

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
