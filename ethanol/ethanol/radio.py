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
#
"""
This module provides: class radio.Radio

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

# from pox.ethanol.ethanol.ap import AP

from pox.ethanol.ssl_message.msg_channels import get_channels, \
    get_currentchannel, set_currentchannel
from pox.ethanol.ssl_message.msg_wlan_info import req_wlan_info
from pox.ethanol.ssl_message.msg_enabled import is_fastbsstransition_compatible
from pox.ethanol.ssl_message.msg_preamble import get_preamble, set_preamble
from pox.ethanol.ssl_message.msg_bitrates import get_tx_bitrates
from pox.ethanol.ssl_message.msg_channelinfo import get_channelinfo
from pox.ethanol.ssl_message.msg_acs import get_acs
from pox.ethanol.ssl_message.msg_interfaces import get_interfaces
from pox.ethanol.ssl_message.msg_powersave import \
    set_powersave_mode, get_powersave_mode
from pox.ethanol.ssl_message.msg_log import log
from pox.ethanol.ssl_message.msg_beacon_interval import get_beacon_interval, set_beacon_interval

class Radio(object):
    """
    Radio represents the physical radios attached to an AP

    abstracts the physical radio
    """
    def __init__(self, ap, wiphy_name, ip, port):
        """
          creates an object associated with the "ap"
          must provide the wiphy_name (intf_name)
        """
        # if not isInstance(ap, AP):
        #   raise ValueError("Parameter is must be an AP class")

        self.__id = uuid.uuid4()  #
        self.__ap = ap

        self.__msg_id = 0  # message id used to identify the msg to the device
        self.__wiphy_name = wiphy_name
        self.__ip = ip
        self.__port = port

    @property
    def id(self):
        """Radio UUID"""
        return self.__id

    def __str__(self):
        """returns the ip and port of this device """
        return "Radio TCP %s:%d" % (self.__ip, self.__port)

    @property
    def msg_id(self):
        """handles the radio message id's
          @return: an id to be used in the message
          and increments the current id
        """
        id = self.__msg_id
        self.__msg_id += 1
        return id

    def __get_connection(self):
        """
        @return: tuple (ip, port_num) used for socket connection to the
        device
        """
        return (self.__ip, self.__port)

    @property
    def wiphy(self):
        """
          @return: the wireless interface name
        """
        return self.__wiphy_name

    @property
    def validChannels(self):
        """ informs a list of valid channel numbers, supported by the device
        in its wireless interface

          @return: the list of the channels that can be assigned to this
          interface. Returns [] if an error occurs
        """
        server = self.__get_connection()  # allows to send message to the AP
        msg, value = get_channels(server, id=self.msg_id,
                                  intf_name=self.__wiphy_name)
        return value

    @property
    def currentChannel(self):
        """
          @return: the channel the AP is operating
        """
        if self.__wiphy_name is None:
            return -1
        server = self.__get_connection()  # allows to send message to the AP
        msg, value = get_currentchannel(server, id=self.msg_id,
                                        intf_name=self.__wiphy_name)
        return value

    @currentChannel.setter
    def currentChannel(self, new_channel):
        """
          tries to set the ap channel.
          @note: to confim that the channel was changed, issue currentChannel()
        """
        server = self.__get_connection()  # allows to send message to the AP
        set_currentchannel(server, id=self.msg_id, channel=new_channel,
                           intf_name=self.__wiphy_name)
        log.debug("canal: %d interface: %s tcp: %d:%d", new_channel,
                  self.__wiphy_name, server[0], server[1])

    @property
    def frequency(self):
        """not implemented yet

          same as currentChannel() but returns the frequency instead
        """
        server = self.__get_connection()  # allows to send message to the AP

    @frequency.setter
    def frequency(self, new_frequency):
        """not implemented yet

        same as currentChannel() but uses the frequency instead
        """
        server = self.__get_connection()  # allows to send message to the AP

    @property
    def tx_bitrates(self):
        """ @return: all bit_rates this radio supports
        """
        server = self.__get_connection()  # allows to send message to the AP
        msg, value = get_tx_bitrates(server, id=self.msg_id,
                                     intf_name=self.__wiphy_name)
        return value

    @tx_bitrates.setter
    def tx_bitrates(self, tx_bitrates):
        """not implemented yet"""
        server = self.__get_connection()  # allows to send message to the AP

    @property
    def powerSaveMode(self):
        """
          returns true if the power save mode is enabled
        """
        server = self.__get_connection()  # allows to send message to the AP
        msg, value = get_powersave_mode(server, self.msg_id)
        return value

    @powerSaveMode.setter
    def powerSaveMode(self, new_mode):
        """
          sets the power mode of the ap to (on or off)
        """
        server = self.__get_connection()  # allows to send message to the AP
        set_powersave_mode(server, id=self.msg_id, powersave=new_mode)

    @property
    def fragmentationThreshold(self):
        """not implemented yet"""
        server = self.__get_connection()  # allows to send message to the AP
        return None

    @fragmentationThreshold.setter
    def fragmentationThreshold(self, new_threshold):
        """not implemented yet"""
        server = self.__get_connection()  # allows to send message to the AP

    @property
    def channelBandwitdh(self):
        """not implemented yet"""
        server = self.__get_connection()  # allows to send message to the AP
        return None

    @channelBandwitdh.setter
    def channelBandwitdh(self, new_chbw):
        """not implemented yet"""
        server = self.__get_connection()  # allows to send message to the AP

    @property
    def channelInfo(self):
        """
        uses MSG_GET_CHANNELINFO to get information for each channel available
        for the wireless interface
        @return: a list with channel info -- active_time, busy_time,
        channel_type, extension_channel_busy_time, frequency, in_use,
        noise, receive_time, transmit_time
        """
        # call ap to get information
        if self.__wiphy_name is None:
            return None
        server = self.__get_connection()  # allows to send message to the AP
        msg, value = get_channelinfo(server, id=self.msg_id,
                                     intf_name=self.__wiphy_name,
                                     only_channel_in_use=True)
        return value

    @property
    def wireless_interfaces(self):
        """get a list of all wireless interfaces
        @return: list of interfaces
        """
        server = self.__get_connection()  # allows to send message to the AP
        msg, value = get_interfaces(server, id=self.msg_id)
        return value

    @property
    def fastBSSTransition(self):
        """connect to ap requesting if it is "Fast BSS Transition" compatible
        """
        server = self.__get_connection()
        msg, value = \
            is_fastbsstransition_compatible(server,
                                            id=self.msg_id,
                                            intf_name=self.__wiphy_name)
        return value

    @property
    def _802_11b_Preamble(self):
        """ connect to ap requesting which type of preamble is set"""
        server = self.__get_connection()
        msg, value = get_preamble(server, id=self.msg_id,
                                  intf_name=self.__wiphy_name)
        log.debug("preamble message received with value %d", value)
        return value

    @_802_11b_Preamble.setter
    def _802_11b_Preamble(self, value):
        """
          set new preamble, returns nothing
        """
        server = self.__get_connection()
        set_preamble(server, id=self.msg_id, intf_name=self.__wiphy_name, preamble=value)
        log.debug("preamble set to %d", value)

    @property
    def beaconInterval(self):
        """connect to ap requesting beacon interval value"""
        server = self.__get_connection()
        msg, value = get_beacon_interval(server, id=self.msg_id, intf_name=self.__wiphy_name)
        log.debug("beacon interval: %d", value)
        return value

    @beaconInterval.setter
    def beaconInterval(self, value=100):
        """ connect to AP to set beacon interval value
            returns nothing
        """
        server = self.__get_connection()
        set_beacon_interval(server, value, id=self.msg_id,
                            intf_name=self.__wiphy_name, beacon_interval=value)
        log.debug("beacon interval set to %s", value)

    def getWirelessInterfaceInfo(self):
        """
          call ap to get information about this interface
        """
        server = self.__get_connection()  # allows to send message to the AP
        msg, value = req_wlan_info(server, id=self.msg_id,
                                   intf_name=self.__wiphy_name)
        return value

    def getLinkStatitics(self):
        """not implemented yet"""
        # call ap to get information
        server = self.__get_connection()  # allows to send message to the AP
        return None

    def getACS(self, num_tests=1):
        ''' request that the AP computes the ACS factor for each frequency
        in the intf_name interface
        '''
        server = self.__get_connection()
        msg, num_chan, acs = get_acs(server, id=self.msg_id,
                                     intf_name=self.__wiphy_name,
                                     num_tests=num_tests)
        log.debug("ACS message received with %d channels", num_chan)
        return num_chan, acs
