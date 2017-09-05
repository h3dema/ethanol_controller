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
from pox.ethanol.ethanol.radio import Radio
from pox.ethanol.ethanol.ap import AP

from pox.ethanol.ssl_message.msg_association import register_functions
from pox.ethanol.ssl_message.msg_log import log


class VAP(Device):
  ''' represents the logical AP (defined by the SSID it contains)
      inherits DEVICE class
  '''

  def __init__(self, server, ssid, radio, mac_address):
    ''' constructor:
    '''
    # if not isinstance(ap, AP):
    #   raise ValueError("Parameter is must be a AP class")

    intf_name = radio.wiphy
    log.info("Creating a VAP in %s interface", intf_name)
    super(VAP, self).__init__(server, intf_name)

    self.__server = server #: saves the reference to server of ap
    self.__mac_address = mac_address #: virtual ap's mac address
    self.__radio = radio #: physical radio to which the vap is attached

    log.debug( "Registering_functions", self.__mac_address )
    register_functions(self.__mac_address, self) # register the association process for this ap

    ''' list of stations connected to this vap '''
    self.__list_of_stations = []

    self.__ssid = ssid #: setting ssid will configure VAP
    self.__mgmt_function = {}
    self.__enabled = False

    log.info("Created VAP with id:%s in interface %s", self.id, intf_name)


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

    if station == None or not isinstance(station, Station):
      return
    self.__list_of_stations.append(station)

  def unregister_station(self, station):
    ''' register a station in the list
        called by station.__del__
    '''
    #TODO: use an efficient way to find the station
    for i in range(len(self.__list_of_stations)):
      if self.__list_of_stations[i] == station:
        del self.__list_of_stations[i]
        break

  @property
  def stations(self):
    ''' return the stations currently connected to the VAP and to the controller (ethanol enabled stations) '''
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
    if self.__ssid != None:
      self.__enabled = (value == True)
      # TODO: configure physical device
      server = self.__get_connection()

  @property
  def ssid(self):
    return self.__ssid

  @ssid.setter
  def ssid(self, value):
    ''' change the vap's SSID
    '''
    if value == None:
      self.__net.deassociateVirtualAP(self)
    elif value != self.__ssid: # changing network
      # changing networks (SSIDs)
      self.__net.deassociateVirtualAP(self)
      # new net
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
    # TODO: get information from physical device
    pass

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
    '''not implemented yet'''
    server = self.__get_connection()
    # TODO: get information from physical device
    pass

  @property
  def guardInterval(self):
    '''not implemented yet'''
    server = self.__get_connection()
    # TODO: get information from physical device
    pass

  @property
  def dtimInterval(self):
    '''not implemented yet'''
    server = self.__get_connection()
    # TODO: get information from physical device
    pass

  @property
  def ctsProtection_enabled(self):
    '''not implemented yet'''
    server = self.__get_connection()
    # TODO: get information from physical device
    pass

  @property
  def rtsThreshold(self):
    '''not implemented yet'''
    server = self.__get_connection()
    # TODO: get information from physical device
    pass

  def getStationInRange():
    '''not implemented yet'''
    server = self.__get_connection()
    # TODO: get information from physical device
    pass

  # default behavior - subclass if you want to change it
  def evUserConnecting(mac_station):
    return True

  # default behavior - subclass if you want to change it
  def evUserAssociating(mac_station):
    return True

  # default behavior - subclass if you want to change it
  def evUserAuthenticating(mac_station):
    return True

  # default behavior - subclass if you want to change it
  def evUserDisassociating(mac_station):
    return True

  # default behavior - subclass if you want to change it
  def evUserReassociating(mac_station):
    return True

  # default behavior - subclass if you want to change it
  def evUserDisconnecting(mac_station):
    return True

  def disassociateUser(station):
    '''not implemented yet'''
    pass

  def deauthenticateUser():
    '''not implemented yet'''
    pass

  def evFastTransition():
    '''not implemented yet'''
    pass

  def evFastReassociation():
    '''not implemented yet'''
    pass

  # if Interval is None, will send each probe received
  # else Interval is number > 0 in milisseconds
  def program_ProbeRequest_Interval(self, Interval = None):
    '''not implemented yet'''
    pass

  def evProbeRequestReceived():
    '''not implemented yet'''
    pass

  def evMgmtFrameReceived(msg_type):
    '''not implemented yet'''
    if not msg_type in self.__mgmt_function:
      return true
    else:
      pass

  def registerMgmtFrame(msg_type, func):
    server = self.__get_connection()
    self.__mgmt_function[msg_type] = func
    # register function in the AP
    # register this object in the message processor

  def unregisterMgmtFrame():
    '''not implemented yet'''
    server = self.__get_connection()
    pass

  def connectNewUser(station):
    '''not implemented yet'''
    pass

