#!/usr/bin/python                                                                            

# sudo mn --controller remote,ip='192.168.0.55' --switch ovs,protocols=OpenFlow13

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import Controller 
from mininet.node import OVSSwitch, RemoteController


c1 = RemoteController( 'c1', ip='192.168.3.203', port=6653 )

cmap = { 's1': c1, 's2': c1, 's3': c1}

class MultiSwitch( OVSSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."

    def build(self, n=2):
        switch = self.addSwitch('s1')
        switch1 = self.addSwitch('s2')
        switch2 = self.addSwitch('s3')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)
        for h in range(n):
            host = self.addHost('h%s' % (h+1))
            self.addLink(host, switch1)
        for h in range(n):
            host = self.addHost('h%s' % (h+1))
            self.addLink(host, switch2)

def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo=topo, switch=MultiSwitch, build=False )
    net.addController(c1)
    net.build()
    net.start()
    dumpNodeConnections(net.hosts)
    CLI(net)
    net.stop()

#ham main 
if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()