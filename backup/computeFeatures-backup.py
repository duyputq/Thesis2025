import numpy as np
import csv
import os

T = 1  # 1s

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
