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
This module provides: class VAP

@author: Henrique Duarte Moura
@organization: WINET/DCC/UFMG
@copyright: h3dema (c) 2017
@contact: henriquemoura@hotmail.com
@licence: GNU General Public License v2.0
(https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
@since: July 2015
@status: in development
"""

from pox.ethanol.ethanol.device import Device
# from pox.ethanol.ethanol.radio import Radio
# from pox.ethanol.ethanol.ap import AP

from pox.ethanol.ssl_message.msg_association import register_functions
from pox.ethanol.ssl_message.msg_log import log
from pox.ethanol.events import Events


class VAP(Device):
    """represents the logical AP (defined by the SSID it contains)
      inherits DEVICE class"""

    def __init__(self, server, ssid, radio, mac_address):
        ''' constructor:
        '''
        # if not isinstance(ap, AP):
        #   raise ValueError("Parameter is must be a AP class")

        self.__intf_name = radio.wiphy
        log.info("Creating a VAP in %s interface", self.__intf_name)
        super(VAP, self).__init__(server, self.__intf_name)

        self.__server = server  #: saves the reference to server of ap
        self.__mac_address = mac_address  #: virtual ap's mac address
        self.__radio = radio  #: physical radio to which the vap is attached

        log.debug("Registering_functions", self.__mac_address)
        # register the association process for this ap
        register_functions(self.__mac_address, self)

        ''' list of stations connected to this vap '''
        self.__list_of_stations = []

        self.__ssid = ssid  #: setting ssid will configure VAP
        self.__enabled = False
        self.__mgmtFrame = dict()  # keep a list of listeners for each type of mgmt frame received
        log.info("Created VAP with id:%s in interface %s", self.id, self.__intf_name)

    def __del__(self):
        ''' destructor: not implemented yet
        '''
        pass

    def __str__(self):
        ''' vap string representation '''
        return "vap[%s]" % self.__mac_address

    def register_station(self, station=None):
        ''' register a station in the list
            called by station.__init__
        '''
        from pox.ethanol.ethanol.station import Station
        if station is None or not isinstance(station, Station):
            return
        self.__list_of_stations.append(station)

    def unregister_station(self, station):
        ''' register a station in the list
            called by station.__del__
        '''
        # TODO: use an efficient way to find the station
        for i in range(len(self.__list_of_stations)):
            if self.__list_of_stations[i] == station:
                del self.__list_of_stations[i]
                break

    @property
    def stations(self):
        ''' return the stations currently connected to the VAP and to the
        controller (ethanol enabled stations)
        '''
        return self.__list_of_stations

    @property
    def mac_address(self):
        ''' VAP's MAC address '''
        return self.__mac_address

    @property
    def radio(self):
        ''' the radio to which the radio is connected '''
        return self.__radio

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        if self.__ssid is not None:
            self.__enabled = (value is True)
            # TODO: configure physical device
            server = self.__get_connection()

    @property
    def ssid(self):
        return self.__ssid

    @ssid.setter
    def ssid(self, value):
        ''' change the vap's SSID
        '''
        if value is None:
            self.__net.deassociateVirtualAP(self)
        elif value != self.__ssid:  # changing network
            # changing networks (SSIDs)
            self.__net.deassociateVirtualAP(self)
            # new net
            from pox.ethanol.ethanol.network import get_or_create_network_by_ssid
            self.__net = get_or_create_network_by_ssid(ssid)
            self.__net.associateVirtualAP(self)
            self.__ssid = ssid
            self.enabled = False
            # TODO: configure physical device
            server = self.__get_connection()

    @property
    def broadcastSSID(self):
        '''not implemented yet'''
        server = self.__get_connection()
        # TODO: get information from physical device
        pass

    @broadcastSSID.setter
    def broadcastSSID(self, value):
        '''not implemented yet'''
        server = self.__get_connection()
        from pox.ethanol.ssl_message.msg_ap_broadcastssid import get_broadcastssid
        msg, value = get_broadcastssid(server=server, id=self.id, intf_name=self.__intf_name, ssid=self.__ssid)
        return value

    @property
    def fastBSSTransitionEnabled(self):
        '''not implemented yet'''
        server = self.__get_connection()
        # TODO: get information from physical device
        pass

    @property
    def security(self):
        '''not implemented yet'''
        server = self.__get_connection()
        # TODO: get information from physical device
        return None

    @property
    def contention(self):
        '''not implemented yet'''
        server = self.__get_connection()
        # TODO: get information from physical device
        pass

    @property
    def cac(self):
        '''not implemented yet'''
        server = self.__get_connection()
        # TODO: get information from physical device
        pass

    @property
    def frameBurstEnabled(self):
        ''':return if AP has frame burst feature enabled'''
        server = self.__get_connection()
        from pox.ethanol.ssl_message.msg_ap_frameburstenabled import get_ap_frameburstenabled
        msg, value = get_ap_frameburstenabled(server=server, id=self.id, intf_name=self.__intf_name)
        return value

    @property
    def guardInterval(self):
        ''':return Guard Interval'''
        server = self.__get_connection()
        from pox.ethanol.ssl_message.msg_ap_guardinterval import get_ap_guardinterval
        msg, value = get_ap_guardinterval(server=server, id=self.id, intf_name=self.__intf_name)
        return value

    @property
    def dtimInterval(self):
        ''':return DTIM interval'''
        server = self.__get_connection()
        from pox.ethanol.ssl_message.msg_ap_dtiminterval import get_ap_dtiminterval
        msg, value = get_ap_dtiminterval(server=server, id=self.id, intf_name=self.__intf_name)
        return value

    @property
    def ctsProtection_enabled(self):
        '''not implemented yet'''
        server = self.__get_connection()
        from pox.ethanol.ssl_message.msg_ap_ctsprotection_enabled import get_ctsprotection_enabled
        msg, value = get_ctsprotection_enabled(server=server, id=self.id, intf_name=self.__intf_name)
        return value

    @property
    def rtsThreshold(self):
        '''get RTS threshold, if 0 RTS/CTS is not used'''
        server = self.__get_connection()
        from pox.ethanol.ssl_message.msg_ap_rtsthreshold import get_ap_rtsthreshold
        msg, value = get_ap_rtsthreshold(server=server, id=self.id, intf_name=self.__intf_name)
        return value

    def getStationInRange(self):
        '''not implemented yet'''
        server = self.__get_connection()
        # TODO: get information from physical device
        pass

    # default behavior - subclass if you want to change it
    def evUserConnecting(self, mac_station):
        return True

    # default behavior - subclass if you want to change it
    def evUserAssociating(self, mac_station):
        return True

    # default behavior - subclass if you want to change it
    def evUserAuthenticating(self, mac_station):
        return True

    # default behavior - subclass if you want to change it
    def evUserDisassociating(self, mac_station):
        return True

    # default behavior - subclass if you want to change it
    def evUserReassociating(self, mac_station):
        return True

    # default behavior - subclass if you want to change it
    def evUserDisconnecting(self, mac_station):
        return True

    def disassociateUser(self, station):
        '''not implemented yet'''
        pass

    def deauthenticateUser(self):
        '''not implemented yet'''
        pass

    def evFastTransition(self):
        '''not implemented yet'''
        pass

    def evFastReassociation(self):
        '''not implemented yet'''
        pass

    # if Interval is None, will send each probe received
    # else Interval is number > 0 in milisseconds
    def program_ProbeRequest_Interval(self, Interval=None):
        '''not implemented yet'''
        pass

    def evProbeRequestReceived(self):
        '''not implemented yet'''
        pass

    def evMgmtFrameReceived(self, msg_type, msg):
        ''' not implemented yet
            :param msg_type indicates the type of the management frame. definition are in ieee80211.h file:
                    #define IEEE80211_STYPE_ASSOC_REQ   0x0000
                    #define IEEE80211_STYPE_ASSOC_RESP  0x0010
                    #define IEEE80211_STYPE_REASSOC_REQ 0x0020
                    #define IEEE80211_STYPE_REASSOC_RESP    0x0030
                    #define IEEE80211_STYPE_PROBE_REQ   0x0040
                    #define IEEE80211_STYPE_PROBE_RESP  0x0050
                    #define IEEE80211_STYPE_BEACON      0x0080
                    #define IEEE80211_STYPE_ATIM        0x0090
                    #define IEEE80211_STYPE_DISASSOC    0x00A0
                    #define IEEE80211_STYPE_AUTH        0x00B0
                    #define IEEE80211_STYPE_DEAUTH      0x00C0
                    #define IEEE80211_STYPE_ACTION      0x00D0
            :param msg message received
        '''
        if msg_type not in self.__mgmtFrame or len(self.__mgmtFrame[msg_type]) == 0:
            return False
        else:
            self.__mgmtFrame[msg_type].on_change(msg)

    def registerMgmtFrame(self, msg_type, listener):
        server = self.__get_connection()
        if msg_type not in self.__mgmtFrame or len(self.__mgmtFrame[msg_type]) == 0:
            self.__mgmtFrame[msg_type] = Events()
            self.__mgmtFrame[msg_type].on_change += listener
            # register function in the AP
            # register this object in the message processor
        else:
            self.__mgmtFrame[msg_type].add(listener)

    def unregisterMgmtFrame(self, msg_type):
        '''not implemented yet
           inform the AP that it does not need to send information back to the controller about this type of message
        '''
        if msg_type not in self.__mgmtFrame or len(self.__mgmtFrame[msg_type]) == 0:
            return  # nothing to do
        server = self.__get_connection()
        del self.__mgmtFrame[msg_type]

    def connectNewUser(self, station, old_ap):
        '''not implemented yet
            transfer information about a station from old_ap to this ap
        '''
        pass
