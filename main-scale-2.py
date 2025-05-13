from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

def myNetwork():
    setLogLevel('info')
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)

    # Remote Controller
    c0 = net.addController('c0', ip='192.168.37.203', port=6653)

    # Switches
    switches = []
    for i in range(1, 9):  # s1 to s8
        switches.append(net.addSwitch(f's{i}', protocols='OpenFlow13'))

    # Hosts (25 host)
    hosts = []
    for i in range(1, 26):
        hosts.append(net.addHost(f'h{i}', ip=f'10.0.0.{i}'))

    sw_host_map = {
        0: [0, 1, 2],
        1: [3, 4, 5],
        2: [6, 7, 8],
        3: [9, 10, 11],
        4: [12, 13, 14],
        5: [15, 16, 17],
        6: [18, 19, 20],
        7: [21, 22, 23, 24],
    }

    for sw_index, host_indices in sw_host_map.items():
        for h_index in host_indices:
            net.addLink(hosts[h_index], switches[sw_index])


    net.addLink(switches[0], switches[1])
    net.addLink(switches[1], switches[2])
    net.addLink(switches[2], switches[3])
    net.addLink(switches[3], switches[4])
    net.addLink(switches[4], switches[5])
    net.addLink(switches[5], switches[6])
    net.addLink(switches[6], switches[7])
    net.addLink(switches[7], switches[0])  

    net.addLink(switches[0], switches[2])
    net.addLink(switches[1], switches[3])
    net.addLink(switches[2], switches[4])
    net.addLink(switches[3], switches[5])
    net.addLink(switches[4], switches[6])
    net.addLink(switches[5], switches[7])
    net.addLink(switches[1], switches[6]) 

    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    myNetwork()
