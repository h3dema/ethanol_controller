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
from pox.ethanol.ethanol.ap import get_vap_by_mac_address

from pox.ethanol.ssl_message.msg_sta_link_information import get_sta_link_info
from pox.ethanol.ssl_message.msg_interfaces import get_interfaces
from pox.ethanol.ssl_message.msg_log import log


'''
  list of all stations connected to the controller
  mantained by add_station() and remove_station()
'''
list_of_stations = {}


def add_station(client_address):
    '''
      Create (and return) possibly several objects,
      one for each wireless connections identified by (client_address, interface name).
      This function updates a list of these objects.

      client_address = (ip, port) used by the Hello message's process
    '''
    ip = client_address[0]

    if ip not in list_of_stations:
        log.info("Starting Station object with IP %s", ip)
        msg, intfs = get_interfaces(server=client_address, id=0)
        ''' select only wireless interfaces '''
        intfs = [intf.intf_name for intf in intfs if intf.is_wifi is True]
        log.info("Found %d wireless interface in the device: %s", len(intfs), ",".join(intfs))
        if len(intfs) > 0:
            list_of_stations[ip] = {}
            for intf_name in intfs:
                log.info("Station interface: %s", intf_name)
                station = Station(socket=client_address, intf_name=intf_name)
                list_of_stations[ip][intf_name] = station
    else:
        log.debug("Station with IP %s exists", ip)


def get_station_by_mac_address(mac_address):
    """returns a connected station, provided its mac address"""
    for intf_name in list_of_stations:
        for sta in list_of_stations[intf_name]:
            if sta.mac_address == mac_address:
                return sta
    return None  # didn't find a station


def get_station_by_ip(ip):
    """returns a connected station, provided its ip address"""
    if ip not in list_of_stations:
        return None
    else:
        return list_of_stations[ip]


def is_sta_with_ip_connected(ip):
    """
      @note: this is the ip of the STA's interface that sends packets to the controller, i.e., normally it is an ethernet interface
      @return: TRUE if an STA with the ip provided as a parameter is connected
    """
    return ip in list_of_stations


class Station(Device):
    '''
      This module contains the Station class.
      Its objects represent each user connected to the VAP
      Each station is identified by its ip address and wireless interface name
    '''

    def __init__(self, socket, intf_name='wlan0'):
      ''' constructor:
            creates an object that represents the user connection
            receives an ip/port pair from the hello message
            uses this info to connect to the station
            and retrieve the radio it is connected to
      '''
      log.info('constructor Station (%s,%s)' % socket)
      super(Station, self).__init__(socket, intf_name)

      msg, mac_addr, ssid, freq, intf = get_sta_link_info(socket,id = self.msg_id,intf_name=intf_name)
      log.info("get_sta_link_info - mac:%s ssid:%s freq:%d intf:%s" % (mac_addr, ssid, freq, intf))
      self.__mac_address = mac_addr

      self.__linkando()
      log.info('Station created')

    def __linkando(self):
      self.__vap = get_vap_by_mac_address(self.__mac_address)
      if self.__vap == None:
        self.__radio = None
        log.debug("VAP <<nao encontrada>> na criacao da Station")
      else:
        self.__radio = self.__vap.radio
        self.__vap.register_station(station=self)
        log.debug("VAP <<encontrada>> na criacao da Station")


    def __del__(self):
      ''' destructor '''
      self.__vap.unregister_station(self)

      if self.__ip in list_of_stations and self.intf_name in list_of_stations[self.__id]:
        del list_of_stations[self.__id][self.intf_name]

    @property
    def vap(self):
      ''' the VAP the station is connected to
      '''
      return self.__vap

    @property
    def radio(self):
      ''' this station is connected to radio,
          if radio == None the AP is not ethanol enabled
      '''
      return self.__radio

    @property
    def wireless_interfaces(self):
      ''' returns all wireless enabled interfaces of the device
      '''
      server = self.get_connection
      msg, intfs = get_interfaces(server,id = 0)
      intfs = [intf.intf_name for intf in intfs if intf.is_wifi == True]
      return intfs

    def getInterferenceMap(self):
      ''' not implemented yet '''
      pass

    def getChannelInfo(self):
      ''' not implemented yet '''
      pass

    def getBeaconInfo(self):
      ''' not implemented yet '''
      pass

    def getNoiseInfo(self):
      ''' not implemented yet '''
      pass

    def getLinkMeasurement(self):
      ''' not implemented yet '''
      pass

    def getStatistics(self):
      ''' not implemented yet '''
      pass

    def getLocation(self):
      ''' not implemented yet '''
      pass

    def triggerTransition(self, new_vap):
      '''uses message MSG_TRIGGER_TRANSITION to send to the station a command to change to a new ap

      @param new_ap: MAC address of the new AP
      '''
      server = self.get_connection
      station_trigger_transition(server, self.msg_id, sta_mac=self.mac_address, intf_name=self.intf_name, mac_new_ap=new_vap)

    def __str__(self):
      ''' string representation of this station
      '''
      ip, port = self.get_connection
      return "Station %s %s conn(%s:%d)" % (self.intf_name, self.__mac_address, ip, port)

