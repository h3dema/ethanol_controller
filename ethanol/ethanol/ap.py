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
  Defines the AP class.
  It represents the physical access point.

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

from pox.ethanol.ssl_message.msg_common import SERVER_PORT
from pox.ethanol.ssl_message.msg_log import log
from pox.ethanol.ssl_message.msg_ap_ssid import get_ap_ssids
from pox.ethanol.ssl_message.msg_radio_wlans import get_radio_wlans
from pox.ethanol.ssl_message.msg_mean_sta_stats import \
    send_msg_mean_sta_statistics
from pox.ethanol.ssl_message.msg_mean_sta_stats import \
    send_msg_mean_sta_statistics_interface_remove, \
    send_msg_mean_sta_statistics_interface_add
from pox.ethanol.ssl_message.msg_mean_sta_stats import \
    send_msg_mean_sta_statistics_alpha, send_msg_mean_sta_statistics_time
from pox.ethanol.ssl_message.msg_hostapd_conf import \
    get_hostapd_conf, set_hostapd_conf


__list_of_aps = {}
"""
    list of all aps connected to the controller
    mantained by add_ap() and remove_ap().
    __list_of_aps provides a list of all ethanol enabled aps connected
    to the controller
"""


map_openflow_vs_ethanol_ip = {}
""" provides a mapping from the ap's ip address to the ap object
"""


def connected_aps():
    """use this function to get the dictionary that contains all aps
    currently connected to Ethanol controller
      @return: list of ap's objects
    """
    return __list_of_aps


def is_ap_with_ip_connected(ip):
    """
        @note: this is the ip of the AP's interface that sends packets to the
        controller, i.e., normally it is an ethernet interface
        @return: TRUE if an AP with the ip provided as a parameter is connected
    """
    return ip in __list_of_aps


def get_ap_by_ip(ip):
    """
        get the AP object with an IP address (of the connection to the
        controller)
        @return: the AP object that has the provided ip address, or None
        if it doesn't exist
        @param ip: a string with the ip address in dotted format
    """
    return None if ip not in __list_of_aps else __list_of_aps[ip]


def get_vap_by_mac_address(mac_address):
    """
        get a VAP object by its MAC address (BSSID)
        @return: a VAP object that matches the mac_address
          or None if doesn't match
        @param mac_address: MAC address in dotted format of the Virtual AP
        (SSID)
    """
    vap = None
    if (len(__list_of_aps)) > 0:
        for ap_ip in __list_of_aps:
            ap = __list_of_aps[ap_ip]
            fvap = [vp for vp in ap.vaps if vp.mac_address == mac_address]
            if len(fvap) > 0:
                vap = fvap[0]
                log.info(" VAP %s encontrada e anexada" % vap)
                break
    return vap


def add_ap_openflow(ip):
    """
        called at ethanol.server when connectionUp occurs.
        inserts an entry in map_openflow_vs_ethanol_ip with the ip detected
        in pox.openflow.connection.
        when a Hello message arrives, AP.__init__() searchs this mapping and
        assigns self to this entry

        @param ip: a string with the ip address in dotted format
        @type ip: str
    """
    if ip not in map_openflow_vs_ethanol_ip:
        map_openflow_vs_ethanol_ip[ip] = None
        # somente irá determinar na mensagem de hello


def add_ap(client_address):
    """
        Create (and return) an AP object for the the device represented
        by the tuple client_address.
        This function updates a list of these objects.

        used by the Hello message's process

        @param client_address: tuple with (ip, port) used to make a socket
        connection to the AP
        @type client_address: tuple or list
    """
    ip = client_address[0]
    port = client_address[1]

    if not(ip in __list_of_aps):
        # create a new ap

        # comentado porque nao tem todas as funcoes do AP
        __list_of_aps[ip] = AP(ip, port)
        log.info("Adding AP with IP %s to the list of connected aps (size %d)"
                 % (ip, len(__list_of_aps)))
        return __list_of_aps[ip]
    else:
        log.debug('AP %s exists' % ip)
        return None # returns None if no new AP object was created


def remove_ap_byIP(ip):
    """
        removes the ap from the list
        called by AP.__destroy__() or
        when the server receives a "bye message" from such AP
          @param ip: a string with the ip address in dotted format
          @type ip: str
    """

    # is the AP object instantiated ? yes--> destroy it

    # remove from the list
    if ip in __list_of_aps:
        del __list_of_aps[ip]


class AP(object):
    """
    defines the AP class that represents the physical wifi device
    """

    def __init__(self, ip, port=SERVER_PORT):
        """
         constructor
         @param ip: socket IP address to connect to the physical AP
         @param port: socket port to connect to the physical AP
        """
        # import placed here to avoid 'import loop'
        from pox.ethanol.ethanol.radio import Radio
        from pox.ethanol.ethanol.network import Network
        from pox.ethanol.ethanol.network import add_network, get_or_create_network_by_ssid

        self.__id = uuid.uuid4()  #
        # client_address tuple
        self.__ip = ip
        self.__port = port
        self.__msg_id = 0
        self.__radios = {}
        self.__listVAP = []
        server = self.__get_connection()
        self.___wiphys = set()
        map_openflow_vs_ethanol_ip[ip] = self
        self.__stats_msec = -1  # disabled
        self.__stats_alpha = 0.1

        """ retrieve and create radios (represented by the physical
        wifi interfaces)
        """
        msg, wlans = get_radio_wlans(server)
        intf_x_mac = {}

        log.info('wireless interfaces: [%s]' % ",".join([_w['intf_name']
                                                        for _w in wlans if _w is not None and _w.intf_name is not None]))
        if wlans is not None:
            # identify distinct set of phy interfaces
            for wlan in wlans:
                wiphy_idx = wlan.wiphy
                wiphy_name = wlan.intf_name
                intf_x_mac[wlan.intf_name] = wlan.mac_addr
                self.___wiphys.add(wiphy_name)
                # create radio objects belonging to this AP
                radio = Radio(self, wiphy_name, ip, port)
                self.__radios[wiphy_name] = radio

        msg, list_ssids = get_ap_ssids(server)

        if list_ssids is not None and len(list_ssids) > 0:
            # TODO: tratar quando o ssid vem nulo
            log.info("SSIDs in Radio: %s" % ",".join([_ssid['ssid']
                                                      for _ssid in list_ssids if _ssid is not None and _ssid.ssid is not None]))
            for ssid in list_ssids:
                if ssid is None or ssid.ssid is None:
                    log.info("Detected a invalid SSID!!!")
                else:
                    try:
                        net = Network(ssid.ssid)  # create the object. This init also inserts the ssid to a control list
                        log.info('[%s] added to network (SSID) list', ssid.ssid)
                    except ValueError:
                        # exception if network exists
                        log.debug('Network SSID %s already exists', ssid.ssid)
                        net = get_or_create_network_by_ssid(ssid.ssid)  # retrieve the network
                    
            log.info('Creating and association the VAP objects')
            #
            # retrieve configured vaps
            # and create vap objects
            #
            for i in range(len(list_ssids)):
                intf_name = list_ssids[i]['intf_name']
                ssid = list_ssids[i]['ssid']
                if intf_name in self.__radios:
                    # if there is no such ssid in list_of_networks
                    # (network.py) add it
                    vap = \
                        self.createvirtualap_and_insert_listvap(ssid,
                                                                self.__radios[intf_name],
                                                                intf_x_mac[intf_name])
            log.info("Num# of VAPs: %d" % len(self.__listVAP))
        else:
          log.debug("AP returned no SSIDs")
            
        log.info('New AP created - id: %s', self.id)

    @property
    def id(self):
        """
        AP's unique identifier
        @return: AP's uuid.uuid4() value
        """
        return self.__id

    def __del__(self):
        """ Called when the instance is about to be destroyed.
            Removes this ap from the mapping
        """
        if self.__ip in map_openflow_vs_ethanol_ip:
            del map_openflow_vs_ethanol_ip[self.__ip]
        log.info('Removing AP %s from list' % self.__ip)
        remove_ap_byIP(self.__ip)

    def __str__(self):
        """
        string
        @return: the ip and port of this device
        """
        return "ap[%s:%d]" % (self.__ip, self.__port)

    @property
    def radios(self):
        """ get list of AP's radios
        @return: a list of radio objects associated with the AP"""
        return self.__radios.values()

    @property
    def msg_id(self):
        """helper function: returns the next message id to be sent, and
           increments the message ID by 1
           @return: id for the new message
        """
        id = self.__msg_id
        self.__msg_id += 1
        return id

    def __get_connection(self):
        """
          socket address of this AP
          @return: a tuple representing the socket to connection to the
          physical ap
        """
        return (self.__ip, self.__port)

    @property
    def vaps(self):
        """ returns a list of the vaps configured in this AP
          @return: list of VAP objects
        """
        return self.__listVAP

    def createvirtualap_and_insert_listvap(self, ssid, radio, mac_address):
        """ create the VAP based on ssid, radio, and mac_address
           inserts the vap in self.__listVAP list

           @param ssid: BSSID
           @type ssid: str
           @param radio: object RADIO attached to this AP
           @type ssid: radio.Radio
           @param mac_address: MAC address in dotted format
           @type mac_address: str

           @return: the vap created
        """
        from pox.ethanol.ethanol.vap import VAP
        server = (self.__ip, self.__port)
        vap = VAP(server, ssid, radio, mac_address)
        self.__listVAP.append(vap)
        return vap

    def destroyvirtualap(self, vap):
        """ remove a VAP: deactivate it (remove SSID)
          @param vap: a vap object (SSID connected to this AP)
          @type vap: vap.VAP object
        """
        if vap in self.__listVAP:
            self.__listVAP.remove(vap)
            """ destroys the vap """
            vap.__del__()

    def getsupportedinterfacemodes(self, intf_name):
        """ indicates the modes supported
            @return: a list with the supported modes: AP, Station, Mesh, IBSS
        """
        server = self.__get_connection()
        from pox.ethanol.ssl_message.msg_ap_modes import get_ap_supported_intf_modes
        msg, value = get_ap_supported_intf_modes(server, m_id=self.msg_id, intf_name=intf_name)
        return value

    def getinterferencemap(self, intf_name):
        """ NOT IMPLEMENTED YET
            returns the interference map as defined in 802.11/2012
        """
        server = self.__get_connection()
        from pox.ethanol.ssl_message.msg_ap_interferencemap import get_ap_interferenceMap
        msg, value = get_ap_interferenceMap(server, m_id=self.msg_id, intf_name=intf_name)
        return value

    @property
    def listwlan_interfaces(self):
        """ wireless interfaces in this AP
          @return: a list with the names of wireless interfaces in this AP
        """
        server = self.__get_connection()
        msg, value = get_radio_wlans(server, id=self.msg_id)
        return value

    def get_interface_stats(self):
        """ get statistics for all interfaces """
        server = self.__get_connection()
        msg, value = send_msg_mean_sta_statistics(server, id=self.msg_id)
        return value

    def enable_interface_stats(self):
        server = self.__get_connection()
        for interface in self.listwlan_interfaces:
            send_msg_mean_sta_statistics_interface_add(server, id=self.msg_id,
                                                       intf_name=interface['intf_name'])

    def disable_interface_stats(self):
        server = self.__get_connection()
        for interface in self.listwlan_interfaces:
            send_msg_mean_sta_statistics_interface_remove(server, id=self.msg_id,
                                                          intf_name=interface['intf_name'])

    @property
    def statistics_time(self):
        """time between collection of traffic statistics.
        -1 means that data collection is disabled"""
        return self.__stats_msec

    @statistics_time.setter
    def statistics_time(self, new_time):
        """
        @param new_time: set the time of collection in miliseconds.
                         send -1 to disable data collection
        """
        self.__stats_msec = new_time if new_time > 0 else -1
        server = self.__get_connection()
        send_msg_mean_sta_statistics_time(server, id=self.msg_id,
                                          msec=new_time)

    @property
    def statistics_alpha(self):
        return self.__stats_alpha

    @statistics_alpha.setter
    def statistics_alpha(self, alpha):
        """defines alpha value for EWMA"""
        self.__stats_alpha = alpha
        server = self.__get_connection()
        send_msg_mean_sta_statistics_alpha(server, id=self.msg_id, alpha=alpha)

    def read_hostapd_conf_param(self, param):
        """ reads the hostapd.conf, finds the param requested, and returns its value
        """
        server = self.__get_connection()
        msg, value = get_hostapd_conf(server, id=self.msg_id, intf_name=None, conf_param=param)
        return value

    def write_hostapd_conf_param(self, param, value):
        """ reads the hostapd.conf, finds the param requested, and (over)write value to its contents
        """
        server = self.__get_connection()
        set_hostapd_conf(server, id=self.msg_id, intf_name=None, conf_param=param, conf_value=value)
