from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def myNetwork():
    setLogLevel('info')
    net = Mininet()

    # Controller
    c0 = net.addController('c0', controller=RemoteController, ip='192.168.137.203', port=6653)

    # Switches
    s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')
    s2 = net.addSwitch('s2', cls=OVSSwitch, protocols='OpenFlow13')
    s3 = net.addSwitch('s3', cls=OVSSwitch, protocols='OpenFlow13')
    s4 = net.addSwitch('s4', cls=OVSSwitch, protocols='OpenFlow13')
    s5 = net.addSwitch('s5', cls=OVSSwitch, protocols='OpenFlow13')

    # Hosts
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')
    h5 = net.addHost('h5', ip='10.0.0.5')

    h6 = net.addHost('h6', ip='10.0.0.6')
    h7 = net.addHost('h7', ip='10.0.0.7')
    h8 = net.addHost('h8', ip='10.0.0.8')
    h9 = net.addHost('h9', ip='10.0.0.9')
    h10 = net.addHost('h10', ip='10.0.0.10')

    h11 = net.addHost('h11', ip='10.0.0.11')
    h12 = net.addHost('h12', ip='10.0.0.12')
    h13 = net.addHost('h13', ip='10.0.0.13')
    h14 = net.addHost('h14', ip='10.0.0.14')
    h15 = net.addHost('h15', ip='10.0.0.15')

    h16 = net.addHost('h16', ip='10.0.0.16')
    h17 = net.addHost('h17', ip='10.0.0.17')
    h18 = net.addHost('h18', ip='10.0.0.18')
    h19 = net.addHost('h19', ip='10.0.0.19')
    h20 = net.addHost('h20', ip='10.0.0.20')


    # Link hosts to switches
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)
    net.addLink(h5, s1)

    net.addLink(h6, s2)
    net.addLink(h7, s2)
    net.addLink(h8, s2)
    net.addLink(h9, s2)
    net.addLink(h10, s2)

    net.addLink(h11, s3)
    net.addLink(h12, s3)
    net.addLink(h13, s3)
    net.addLink(h14, s3)
    net.addLink(h15, s3)

    net.addLink(h16, s4)
    net.addLink(h17, s4)
    net.addLink(h18, s4)
    net.addLink(h19, s4)
    net.addLink(h20, s4)

    # Kết nối switch theo vòng
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s4)
    net.addLink(s4, s5)
    net.addLink(s5, s1)
    net.addLink(s5, s2)
    net.addLink(s5, s3)

    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    myNetwork()
