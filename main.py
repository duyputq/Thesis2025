from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.node import Host
from mininet.cli import CLI
from mininet.log import setLogLevel

def myNetwork():
    setLogLevel('info')
    net = Mininet()

    #ip cua may ca nhan cung la ip cua controller, port 6653 la port danh cho openflow
    c0 = net.addController('c0', controller=RemoteController, ip='192.168.3.200', port=6653) 
    s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')
    s2 = net.addSwitch('s2', cls=OVSSwitch, protocols='OpenFlow13')
    s3 = net.addSwitch('s3', cls=OVSSwitch, protocols='OpenFlow13')
    h1 = net.addHost('h1', ip ='10.0.0.1', bw = 1000, delay = '5ms')
    h2 = net.addHost('h2', ip ='10.0.0.2', bw = 1000, delay = '5ms')
    h3 = net.addHost('h3', ip ='10.0.0.3', bw = 1000, delay = '5ms')
    h4 = net.addHost('h4', ip ='10.0.0.4', bw = 1000, delay = '5ms')
    h5 = net.addHost('h5', ip ='10.0.0.5', bw = 1000, delay = '5ms')
    h6 = net.addHost('h6', ip='10.0.0.6', cpu=0.05, bw=5, delay='100ms')
    h7 = net.addHost('h7', ip='10.0.0.7', bw = 1000, delay = '5ms')
    h8 = net.addHost('h8', ip='10.0.0.8', cpu=0.1, bw=10, delay='50ms')
    h9 = net.addHost('h9', ip='10.0.0.9', bw = 1000, delay = '5ms')
    h10 = net.addHost('h10', ip='10.0.0.10', bw = 1000, delay = '5ms')

    net.addLink(h1, s1)
    net.addLink(h3, s1)
    net.addLink(h2, s1)
    net.addLink(h4, s2)
    net.addLink(h5, s2)
    net.addLink(h6, s2)
    net.addLink(h7, s2)
    net.addLink(h8, s3)
    net.addLink(h9, s3)
    net.addLink(h10, s3)
    net.addLink(s1,s2)
    net.addLink(s2,s3)
    net.addLink(s1,s3)
    net.start()
    CLI(net)

    net.stop()

if __name__ == '__main__':
    myNetwork()
