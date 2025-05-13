sudo ovs-ofctl -O OpenFlow13 add-flow s1 'table=0, priority=10, in_port=s1-eth1, dl_src=22:ac:3e:77:9b:88, dl_dst=96:39:95:49:17:d0, actions=drop'



ovs-ofctl -O OpenFlow13 dump-flows s1 | awk -F"[=, ]+" '/n_bytes/ { for (i=1;i<=NF;i++) if ($i=="n_bytes" && $(i+1)>1000) print $0 }' | grep in_port
