import numpy as np
import csv
import pandas as pd
import time
import os
import psutil
HOME = '/home/xp'
time_interval = 1

packets_csv = np.genfromtxt('data/packets.csv', delimiter=",")
dt_packets = packets_csv[:, 0]
sdfp = np.std(dt_packets)

bytes_csv = np.genfromtxt('data/bytes.csv', delimiter=",")
dt_bytes = bytes_csv[:, 0]
sdfb = np.std(dt_bytes)

with open('data/ipsrc.csv', newline='') as f:
    reader = csv.reader(f)
    ipsrc_csv = list(reader)
n_ip = len(np.unique(ipsrc_csv))      

ssip = n_ip 
f.close()

with open('data/flowentries.csv', newline='') as f:
    reader = csv.reader(f)
    flows = list(reader)
n_flows = len(flows)
sfe = n_flows 

fileone = None
filetwo = None

with open('data/ipsrc.csv', 'r') as t1, open('data/ipdst.csv', 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

with open('data/intflow.csv', 'w') as f:
    for line in fileone:
        if line not in filetwo:
            f.write(line)

cpu_percent = psutil.cpu_percent(interval=0.1)

with open('data/intflow.csv') as f:
    reader = csv.reader(f, delimiter=",")
    dt = list(reader)
    row_count_nonint = len(dt)
rfip = abs(float(n_ip - row_count_nonint) / n_ip)

with open('ARP_data/ARP_Reply_flowentries.csv', newline='') as f:
    reader = csv.reader(f)
    ARP_Reply = list(reader)

ARP_Reply = len(ARP_Reply)
with open('ARP_data/ARP_Request_flowentries.csv', newline='') as f1:
    reader = csv.reader(f1)
    ARP_Request = list(reader)

path = HOME + '/Multi-Label-Attacks-Detection/ARP_Broadcast/arp_broadcast.csv'
with open(path, newline='') as f2:
    reader = csv.reader(f2)

    arp_broadcast = list(reader)

arp_broadcast = len(arp_broadcast)
abps = arp_broadcast / time_interval

ARP_Request = len(ARP_Request)
ARP = ARP_Reply + ARP_Request

f.close()
f1.close()
f2.close()

aps = ARP / time_interval
subARP = ARP_Reply - ARP_Request

with open('mismatch.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader = list(reader)

if int(reader[-1][-1]) > 0:
    if subARP >= 1:
        miss_match = 1
    else:
        miss_match = 0
else:
    miss_match = 0

time_stamp = time.strftime("%H:%M:%S", time.localtime())

ddos = 0
slow_rate = 0
mitm = 0
tag_ddos = ''
tag_slow_rate = ''
tag_mitm = ''

if ddos != 0:
    tag_ddos = 'DDOS '
if slow_rate != 0:
    tag_slow_rate = 'Slow Rate '
if mitm != 0:
    tag_mitm = 'MITM '
if ddos == 0 and slow_rate == 0 and mitm == 0:
    tag = 'Normal'
else:
    tag = tag_ddos + tag_slow_rate + tag_mitm

headers = ["SSIP", "SDFP", "SDFB", "SFE", "RFIP",
           "CPU", "APS", "ABPS", "SUBARP", "MISS_MAC"]

features = [ssip, sdfp, sdfb, sfe, rfip, cpu_percent,
            aps, abps, subARP, miss_match]

file_exists = os.path.isfile('features-file.csv')
with open('features-file.csv', 'a') as f:
    cursor = csv.writer(f, delimiter=",")

    if not file_exists:
        cursor.writerow(headers)
    cursor.writerow(features)

with open('realtime.csv', 'w') as f:
    cursor = csv.writer(f, delimiter=",")
    cursor.writerow(headers)
    cursor.writerow(features)

    f.close()