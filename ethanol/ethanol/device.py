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
"""
This module provides: class device.Device

It is a superclass for Station and VAP

@author: Henrique Duarte Moura
@organization: WINET/DCC/UFMG
@copyright: h3dema (c) 2017
@contact: henriquemoura@hotmail.com
@licence: GNU General Public License v2.0
(https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
@since: July 2015
@status: in development
"""
import uuid

from pox.ethanol.ssl_message.msg_log import log
from pox.ethanol.ssl_message.msg_sent_received import \
    send_msg_get_bytesreceived, send_msg_get_bytessent
from pox.ethanol.ssl_message.msg_sent_received import \
    send_msg_get_packetsreceived, send_msg_get_packetssent,\
    send_msg_get_packetslost
from pox.ethanol.ssl_message.msg_statistics import send_msg_get_statistics
from pox.ethanol.ssl_message.msg_snr_power import get_snr, get_txpower, \
    set_txpower
from pox.ethanol.ssl_message.msg_enabled import \
    is_fastbsstransition_compatible, is_802_11e_enabled
from pox.ethanol.ssl_message.msg_memcpu import get_cpu_usage, get_memory_usage
from pox.ethanol.ssl_message.msg_ap_in_range import get_ap_in_range
from pox.ethanol.ssl_message.msg_bitrates import get_tx_bitrate
from pox.ethanol.ssl_message.msg_uptime import get_uptime
from pox.ethanol.ssl_message.msg_tos import tos_cleanall, tos_add, tos_replace


class Device(object):
    """
      this superclass provides the attributes and methods
      shared by Station and VAP
    """

    def __init__(self, socket, intf_name):
        """ creates a device object (used by VAP and STATION)
        @param socket: tuple (ip, port_num)
        @param intf_name: name of the wireless interface that this device uses
        """
        log.debug("starting DEVICE constructor")
        self.__id = uuid.uuid4()  # UUID
        self.__socket = socket
        # socket (ip, port) that will be used to connect to this station
        self.__ip, self.__port = socket
        self.__intf_name = intf_name
        self.__mac_address = None
        self.__msg_id = 0
        log.debug("DEVICE id:%s created", self.__id)

    @property
    def id(self):
        """ unique identifier (UUID) for this device """
        return self.__id

    @property
    def get_connection(self):
        """ returns a tuple representing the socket to connection to the
        physical station
        """
        return (self.__ip, self.__port)

    @property
    def msg_id(self):
        """helper function: returns the next message id to be sent.
           increments the message ID by 1
        """
        id = self.__msg_id
        self.__msg_id += 1
        return id

    @property
    def intf_name(self):
        """ wireless interface of this device (set during __init__)
        """
        return self.__intf_name

    @property
    def mac_address(self):
        """ wireless interface's MAC address
        """
        return self.__mac_address

    @property
    def ipv4_address(self):
        """NOT IMPLEMENTED YET -- function in C is ok

           get the device's IP address (version 4)
        """
        pass

    @ipv4_address.setter
    def ipv4_address(self, ip_conf):
        """NOT IMPLEMENTED YET -- function in C is ok

           set IP v4 parameters: ip, netmask, gateway
        """
        pass

    @property
    def ipv6_address(self):
        """NOT IMPLEMENTED YET -- function in C is ok

         get the device's IP address (version 6)
        """
        pass

    @ipv6_address.setter
    def ipv6_address(self, ip_conf):
        """NOT IMPLEMENTED YET -- function in C is ok

           set the device's IP address (version 6)
        """
        pass

    @property
    def _802_11e_enabled(self):
        """ is the device 802.11e compatible?
        @return: bool
        """
        server = self.get_connection
        msg, value = is_802_11e_enabled(server, id=self.msg_id,
                                        intf_name=self.__intf_name)
        return value

    @property
    def fastBSSTransition_compatible(self):
        """connect to ap requesting if it is "Fast BSS Transition" compatible
        """

        # deste jeito esta mandando a mensagem diretamente para a estacao
        server = self.get_connection
        msg, value = \
            is_fastbsstransition_compatible(server, id=self.msg_id,
                                            intf_name=self.__intf_name)
        return value

    @property
    def bytesReceived(self):
        """ number of bytes received on this interface (cumulative value) """
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        msg, value = send_msg_get_bytesreceived(server, id=self.msg_id,
                                                intf_name=self.__intf_name)
        return value

    @property
    def bytesSent(self):
        """ number of bytes sent on this interface (cumulative value) """
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        msg, value = send_msg_get_bytessent(server, id=self.msg_id,
                                            intf_name=self.__intf_name)
        return value

    @property
    def packetsReceived(self):
        """ number of packets received on this interface (cumulative value) """
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        msg, value = send_msg_get_packetsreceived(server, id=self.msg_id,
                                                  intf_name=self.__intf_name)
        return value

    @property
    def packetsSent(self):
        """ number of packets sent on this interface (cumulative value) """
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        msg, value = send_msg_get_packetssent(server, id=self.msg_id,
                                              intf_name=self.__intf_name)
        log.debug('packetSent device %f', value)
        return value

    @property
    def packetsLost(self):
        """ number of packets lost on this interface (cumulative value) """
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        msg, value = send_msg_get_packetslost(server, id=self.msg_id,
                                              intf_name=self.__intf_name)
        log.debug('packetsLost device %f', value)
        return value

    @property
    def jitter(self):
        """NOT IMPLEMENTED YET

            @return: mean jitter measured at the wireless interface
        """
        if self.__intf_name is None:
            return -1

    @property
    def delay(self):
        """NOT IMPLEMENTED YET

            @return: mean delay measured at the wireless interface
        """
        if self.__intf_name is None:
            return -1

    @property
    def retries(self):
        """NOT IMPLEMENTED YET

            @return: number of retries at the wireless interface
        """
        if self.__intf_name is None:
            return -1

    @property
    def failed(self):
        """NOT IMPLEMENTED YET

            @return: total number of failures at the wireless interface
        """
        if self.__intf_name is None:
            return -1

    @property
    def statistics(self):
        """ collect some cumulative statistics --
            rx_packets, rx_bytes, rx_dropped, tx_packets, tx_bytes.
            these values are accumulate since the interface went up.
        """
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        msg, stats = send_msg_get_statistics(server, id=self.msg_id,
                                             intf_name=self.__intf_name)
        # log.debug('Statistics device %d, %d, %d, %d, %d, %s', rx_packets,
        # rx_bytes, rx_dropped, tx_packets, tx_bytes, time_stamp)
        return stats

    @property
    def signalStrength(self):
        """NOT IMPLEMENTED YET"""
        if self.__intf_name is None:
            return -1

    @property
    def SNR(self):
        """ retrieve current SNR """
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        msg, value = get_snr(server, id=self.msg_id,
                             intf_name=self.__intf_name)
        log.debug('SNR %f', value)
        return value

    @property
    def txpower(self):
        """ retrieve the TX power """
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        msg, value = get_txpower(server, id=self.msg_id,
                                 intf_name=self.__intf_name)
        log.debug('get TXPower device %f', value)
        return value

    @txpower.setter
    def txpower(self, new_value):
        """set current tx power"""
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        set_txpower(server, id=self.msg_id, intf_name=self.__intf_name,
                    txpower=new_value)
        log.debug('set TXPower device to %f', new_value)

    def tx_bitrate(self, sta_mac=None):
        """ @return: the last seen tx_bitrate for a given station (in Mbps)
            or a list for each station connected (if sta_mac is None)
        """
        if (self.__intf_name is None) and \
           ((self.__mac_address is None) or (sta_mac is None)):
            return -1
        else:
            server = self.get_connection
            if sta_mac is not None:
                mac = sta_mac
            else:
                mac = self.__mac_address
            msg, value = get_tx_bitrate(server, id=self.msg_id,
                                        intf_name=self.__intf_name,
                                        sta_mac=mac)
            return value

    @property
    def uptime(self):
        """system uptime and idle time in seconds"""
        server = self.get_connection
        msg, uptime, idle = get_uptime(server, id=self.msg_id)
        return uptime, idle

    @property
    def cpu(self):
        """ physical device's CPU usage """
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        msg, value = get_cpu_usage(server, id=self.msg_id)
        log.debug('CPU device %f', value)
        return value

    @property
    def cpu_usage(self):
        """ same as cpu(). to keep model compatibility"""
        return self.cpu

    @property
    def memory(self):
        """ physical device's memory usage """
        if self.__intf_name is None:
            return -1
        server = self.get_connection
        msg, value = get_memory_usage(server, id=self.msg_id)
        log.debug('Memory device %f', value)
        return value

    @property
    def memory_usage(self):
        """ same as memory(). to keep model compatibility"""
        return self.memory

    @property
    def getAPsInRange(self):
        """get aps that are in range.
          @note: this method is not precise, because it relies on the spare
          time the device has to scan all the channels
        """
        if self.__intf_name is None:
            return -1, None
        server = self.get_connection
        msg, num_aps, aps = get_ap_in_range(server, id=self.msg_id,
                                            intf_name=self.__intf_name)
        log.debug('get ap_in_range device %d, %f', num_aps, aps)
        return num_aps, aps

    def clear_mange(self):
        server = self.get_connection
        tos_cleanall(server, id=self.msg_id)

    def add_tos(self, rules):
        server = self.get_connection
        for rule in rules:
            tos_add(server=server, msg_id=self.msg_id,
                    intf_name=rule['intf_name'],
                    proto=rule['proto'],
                    sip=rule['sip'],
                    sport=rule['sport'],
                    dip=rule['dip'],
                    dport=rule['dport'],
                    wmm_class=rule['wmm_class'])

    def replace_tos(self, rules):
        server = self.get_connection
        for rule in rules:
            tos_replace(server=server, msg_id=self.msg_id,
                        rule_id=rule['rule_id'],
                        intf_name=rule['intf_name'],
                        proto=rule['proto'],
                        sip=rule['sip'],
                        sport=rule['sport'],
                        dip=rule['dip'],
                        dport=rule['dport'],
                        wmm_class=rule['wmm_class'])
