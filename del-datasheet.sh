#!/bin/bash

packets_file="data/packets.csv"
bytes_file="data/bytes.csv"
output_file="data/dataset.csv"
feature_file="data/features-file.csv"
mac_src_file="data/mac-src.csv"
duration_file="data/duration.csv"
switches=("s1" "s2" "s3")

> "$output_file"
> "$packets_file"
> "$bytes_file"
> "$feature_file"
> "$mac_src_file"
> "$duration_file"