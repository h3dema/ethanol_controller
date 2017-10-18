#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# ##################################
#
# Copyright 2015 Henrique Moura
#
# This file is part of Ethanol.
#
# ##################################
#

"""  An L2 learning switch
     based on L2 learning example from POX
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import time

log = core.getLogger()

# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.
_flood_delay = 0


class LearningSwitch(object):

    def __init__(self, connection, transparent, idle_timeout=10,
                 hard_timeout=30):
        # We just use this to know when to log a helpful message
        self.hold_down_expired = _flood_delay == 0
        # Switch we'll be adding L2 learning switch capabilities to
        self.connection = connection
        self.transparent = transparent
        self.__idle_timeout = idle_timeout
        self.__hard_timeout = hard_timeout

        # Our table
        self.macToPort = {}

        # We want to hear PacketIn messages, so we listen to the connection
        connection.addListeners(self)

    def __flood(self, message=None):
        """ Floods the packet """
        msg = of.ofp_packet_out()
        if time.time() - self.connection.connect_time >= _flood_delay:
            # Only flood if we've been connected for a little while...

            if self.hold_down_expired is False:
                # Oh yes it is!
                self.hold_down_expired = True
                log.info("%s: Flood hold-down expired -- flooding",
                         dpid_to_str(self.__dpid))

            if message is not None:
                log.debug(message)
            # log.debug("%i: flood %s -> %s", event.dpid,packet.src,packet.dst)

            # OFPP_FLOOD is optional;
            # on some switches you may need to change this to OFPP_ALL.
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        else:
            pass
            # log.info("Holding down flood for %s", dpid_to_str(event.dpid))
        msg.data = self.__data
        msg.in_port = self.__in_port
        self.connection.send(msg)

    """
    Drops this packet and optionally installs a flow to continue
    dropping similar ones for a while
    """
    def __drop(self, duration=None):
        if duration is not None:
            if not isinstance(duration, tuple):
                duration = (duration, duration)
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(self.__packet)
            msg.idle_timeout = duration[0]
            msg.hard_timeout = duration[1]
            msg.buffer_id = self.__data.buffer_id
            self.connection.send(msg)
        elif event.ofp.buffer_id is not None:
            msg = of.ofp_packet_out()
            msg.buffer_id = self.__data.buffer_id
            msg.in_port = self.__in_port
            self.connection.send(msg)

    def _handle_PacketIn(self, event):
        """
        Handle packet in messages from the switch to implement above algorithm.
        """
        self.__dpid = event.dpid
        self.__packet = event.parsed
        self.__data = event.ofp
        self.__in_port = event.port

        self.macToPort[self.__packet.src] = self.__in_port  # 1

        if not self.transparent:  # 2
            if self.__packet.type == self.__packet.LLDP_TYPE or \
                    self.__packet.dst.isBridgeFiltered():
                __drop()  # 2a
                return

        if self.__packet.dst.is_multicast:
            __flood()  # 3a
        else:
            dst = self.__packet.dst
            if dst not in self.macToPort:  # 4
              __flood("Port for %s unknown -- flooding" %(dst,)) # 4a
            else:
                port = self.macToPort[dst]
                if port == self.__in_port:  # 5
                    # 5a
                    log.warning("Same port for packet from %s -> %s on %s.%s.\
                      Drop." %(packet.src, dst, dpid_to_str(self.__dpid),
                                port))
                    __drop(10)
                    return
                # 6
                log.debug("installing flow for %s.%i -> %s.%i" %
                         (packet.src, event.port, packet.dst, port))
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet, event.port)
                msg.idle_timeout = self.__idle_timeout
                msg.hard_timeout = self.__hard_timeout
                msg.actions.append(of.ofp_action_output(port=port))
                msg.data = event.ofp  # 6a
                self.connection.send(msg)


class l2_learning(object):
    """
    Waits for OpenFlow switches to connect and makes them learning switches.
    """
    def __init__(self, transparent):
        core.openflow.addListeners(self)
        self.transparent = transparent

    def _handle_ConnectionUp(self, event):
        log.debug("Connection %s" %(event.connection,))
        LearningSwitch(event.connection, self.transparent)


def launch(transparent=False, hold_down=_flood_delay):
    """
    Starts an L2 learning switch.
    """
    try:
        global _flood_delay
        _flood_delay = int(str(hold_down), 10)
        assert _flood_delay >= 0
    except Exception:
        raise RuntimeError("Expected hold-down to be a number")

    core.registerNew(l2_learning, str_to_bool(transparent))
