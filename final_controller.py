# Final Skeleton
#
# Hints/Reminders from Lab 4:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 4:
    #   - port_on_switch represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)

    if packet.find('ipv4'):
      ip = packet.find('ipv4')

      if ip.srcip == IPAddr('128.114.50.10') and ip.dstip == IPAddr('10.0.4.104'):
        #checks if packet comes from Untrusted Host
        #drops packet if packet destination is Server 1 
        self.drop_packet(packet, packet_in)

      elif ip.srcip == IPAddr('128.114.50.10') and packet.find('icmp'):
          #if icmp packet, drop
          self.drop_packet(packet, packet_in)
      else:

        if switch_id!=4:

          if port_on_switch == 1:
            #print "send out to core switch"
            self.send_packet(packet, packet_in, 2)
          else:
            #print "send to host"
            self.send_packet(packet, packet_in, 1)
            #if ip.srcip == IPAddr('128.114.50.10'):
              #print "non-ICMP packet from Untrusted to Host received"
      
        elif switch_id==4:

          if ip.dstip == IPAddr('10.0.1.101'):
            self.send_packet(packet, packet_in, 1)

          elif ip.dstip == IPAddr('10.0.2.102'):
            self.send_packet(packet, packet_in, 2)

          elif ip.dstip == IPAddr('10.0.3.103'):
            self.send_packet(packet, packet_in, 3)

          elif ip.dstip == IPAddr('128.114.50.10'):
            #print "SENDING PACKET TO UNTRUSTED"
            self.send_packet(packet, packet_in, 4)

          elif ip.dstip == IPAddr('10.0.4.104'):
            self.send_packet(packet, packet_in, 5)

    else:
      self.send_packet(packet, packet_in, of.OFPP_FLOOD)

  def send_packet (self, packet, packet_in, port_out):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30
    msg.buffer_id = packet_in.buffer_id
    msg.actions.append(of.ofp_action_output(port = port_out))
    self.connection.send(msg)

  def drop_packet (self, packet, packet_in):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30
    msg.buffer_id = packet_in.buffer_id
    msg.actions = []
    self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
