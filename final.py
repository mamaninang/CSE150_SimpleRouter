#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Create hosts with a default route of the ethernet interface
    h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='10.0.1.101/24', defaultRoute="h1-eth0")
    h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='10.0.2.102/24', defaultRoute="h2-eth0")
    h3 = self.addHost('h3',mac='00:00:00:00:00:03',ip='10.0.3.103/24', defaultRoute="h3-eth0")
    h4 = self.addHost('h4',mac='00:00:00:00:00:04',ip='128.114.50.10/24', defaultRoute="h4-eth0")
    h5 = self.addHost('h5',mac='00:00:00:00:00:05',ip='10.0.4.104/24', defaultRoute="h5-eth0")

    # Create the switches
    s1 = self.addSwitch('s1')   #floor 1 switch
    s2 = self.addSwitch('s2')   #floor 2 switch
    s3 = self.addSwitch('s3')   #floor 3 switch
    s4 = self.addSwitch('s4')   #core switch
    s5 = self.addSwitch('s5')   #data center switch

    # Create the links that will connect a host to a switch, or connect a switch to another switch
    self.addLink(s1,h1, port1=1, port2=0)     #switch 1 port 1 linked to host 1 port 0
    self.addLink(s2,h2, port1=1, port2=0)     #switch 2 port 1 linked to host 2 port 0
    self.addLink(s3,h3, port1=1, port2=0)     #switch 3 port 1 linked to host 3 port 0
    self.addLink(s4,h4, port1=4, port2=0)     #core switch port 4 linked to Untrusted Host port 0
    self.addLink(s5,h5, port1=1, port2=0)     #data center switch port 1 linked to host 1 port 0
    self.addLink(s4,s1, port1=1, port2=2)     #core switch port 1 connected to switch 1 port 2
    self.addLink(s4,s2, port1=2, port2=2)     #core switch port 2 connected to switch 2 port 2
    self.addLink(s4,s3, port1=3, port2=2)     #core switch port 3 connected to switch 3 port 2
    self.addLink(s4,s5, port1=5, port2=2)     #core switch port 5 connected to switch 5 port 2

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
