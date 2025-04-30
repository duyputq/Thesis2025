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

if (label == 1):
    # Giả sử bạn chỉ lấy 1 dòng cuối trong CSV (MAC pair cuối)
    dl_src, dl_dst = mac_pairs[-1]

    print("Detected DDOS Traffic", end=" - ")
    # # os.system("echo show us your way")
    # # os.system("ovs-ofctl -O OpenFlow13 add-flow s1 'table=0, priority=10, in_port=s1-eth1, dl_src=22:ac:3e:77:9b:88, dl_dst=96:39:95:49:17:d0, actions=drop'")
    # # s1
    commands = [
    'ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=1, dl_src=A6:B9:DD:9E:05:2C, dl_dst=02:39:04:A9:52:82, actions=drop"',
    'ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=4, dl_src=02:39:04:A9:52:82, dl_dst=A6:B9:DD:9E:05:2C, actions=drop"',
    'ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=3, dl_src=02:39:04:A9:52:82, dl_dst=A6:B9:DD:9E:05:2C, actions=drop"',
    'ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=5, dl_src=A6:B9:DD:9E:05:2C, dl_dst=02:39:04:A9:52:82, actions=drop"',
    ]

    processes = [subprocess.Popen(cmd, shell=True) for cmd in commands]

    command2s = [
    'ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=1, dl_src=A6:B9:DD:9E:05:2C, dl_dst=02:39:04:A9:52:82, actions=drop"',
    'ovs-ofctl -O OpenFlow13 add-flow s1 "table=0, priority=10, in_port=4, dl_src=02:39:04:A9:52:82, dl_dst=A6:B9:DD:9E:05:2C, actions=drop"',
    'ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=3, dl_src=02:39:04:A9:52:82, dl_dst=A6:B9:DD:9E:05:2C, actions=drop"',
    'ovs-ofctl -O OpenFlow13 add-flow s2 "table=0, priority=10, in_port=5, dl_src=A6:B9:DD:9E:05:2C, dl_dst=02:39:04:A9:52:82, actions=drop"',
    ]

    processes2 = [subprocess.Popen(cmd, shell=True) for cmd in command2s]

    print("Mitigated DDOS Traffic Successfully!")
    
    # for p in processes:
    #     p.wait()

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
