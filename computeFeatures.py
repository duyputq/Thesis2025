import numpy as np
import csv
import os

# Tính SDFP: độ lệch chuẩn số packet
packets_csv = np.genfromtxt('data/packets.csv', delimiter=",")
dt_packets = packets_csv
sdfp = np.std(dt_packets)

# Tính SDFB: độ lệch chuẩn số byte
bytes_csv = np.genfromtxt('data/bytes.csv', delimiter=",")
dt_bytes = bytes_csv
sdfb = np.std(dt_bytes)

# Headers và feature chỉ còn sdfb và sdfp
headers = ["SDFB", "SDFP"]
features = [sdfb, sdfp]

# Ghi vào file CSV
file_exists = os.path.isfile('features-file.csv')
with open('data/features-file.csv', 'a') as f:
    cursor = csv.writer(f, delimiter=",")
    if not file_exists:
        cursor.writerow(headers)
    cursor.writerow(features)

with open('data/realtime.csv', 'w') as f:
    cursor = csv.writer(f, delimiter=",")
    cursor.writerow(headers)
    cursor.writerow(features)
