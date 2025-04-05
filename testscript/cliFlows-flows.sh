#! /usr/bin/expect

set timeout -1
set output_file "data/dump-flows.csv"
spawn /opt/onos/bin/onos -l onos
expect "(onos@localhost) Password:"
send "rocks\r"

set fileId [open $output_file "w"]
puts $fileId "bytes, packets, priority, selector"

while {1} {
    expect "onos@root >"
    send "flows -s\r"
    set result $expect_out(buffer)
    set cleaned_result [string trim $result "onos@root >"]
    
    foreach line [split $cleaned_result "\n"] {
        if {[regexp {bytes=([0-9]+), packets=([0-9]+),.*priority=([0-9]+), selector=\[(.*?)\]} $line match bytes packets priority selector]} {
            if {[regexp {IN_PORT:[0-9]+} $selector]} {
                puts $fileId "$bytes, $packets, $priority, $selector"
                flush $fileId
            }
        }
    }
    sleep 3
}

close $fileId