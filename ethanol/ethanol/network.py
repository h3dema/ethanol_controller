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
defines the Network class that represents the SSIDs controlled by
the Ethanol Controller

This module provides:

1) add_network(net)

2) del_network(net)

3) get_or_create_network_by_ssid(ssid)

4) class Network

@author: Henrique Duarte Moura
@organization: WINET/DCC/UFMG
@copyright: h3dema (c) 2017
@contact: henriquemoura@hotmail.com
@licence: GNU General Public License v2.0
(https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
@since: July 2015
@status: in development
"""

from uuid import uuid4

from pox.ethanol.ethanol.vap import VAP
from pox.ethanol.ethanol.station import Station
from pox.ethanol.ssl_message.msg_log import log

__list_of_networks = {}
""" list of all SSID's controlled by our ethanol controller
"""


def list_of_networks():
    global __list_of_networks
    return __list_of_networks


def add_network(ssid, net):
    """ returns True if successfully added the network to the set.
      False if the SSID of the network provided already exists.
      net is also not added to the set
    """
    # ssid = net.__SSID
    global __list_of_networks
    search_ssid = [i for i in __list_of_networks.keys() if i == ssid]
    if len(search_ssid) > 0:
        # duvida: atualizar a rede???
        return False

    __list_of_networks[ssid] = net
    return True


def del_network(net):
    """ delete this network.
      disconfigures all vaps associated to this network
    """
    global __list_of_networks
    if isinstance(net, Network):
        ssid = net.__SSID
        if ssid in __list_of_networks:
            net = __list_of_networks[ssid]
            net.releaseResources()  # release resources
            del __list_of_networks[ssid]


def get_or_create_network_by_ssid(ssid):
    """ returns a Network object representing the ssid.
                if none exists, a new one is created
    """
    global __list_of_networks
    if ssid in __list_of_networks:
        return __list_of_networks[ssid]
    else:
        net = Network(ssid)
        add_network(net)
        return net


class Network(object):
    """
    handle a network - a network is a set of VAPs that share the same SSID
    """

    def __init__(self, ssid):
        """
          create a network with ESSID = ssid
        """
        for i in list_of_networks():
            if i[0] == ssid:
                raise ValueError("SSID %s already exists!" % self.__SSID)

        if ssid in list_of_networks():
            log.debuf('ssid %s already exists in ')

        self.__id = uuid4()  # random UUID

        self.__SSID = ssid
        self.__listVAP = []
        self.__msg_id = 0  # message id used to identify the msg to the device
        log.info('SSID: %s', self.__SSID)
        add_network(self.__SSID, self)
        log.info('constructor Network %s ended', self.__SSID)

    def __del__(self):
        """
          class destructor
          Called when the instance is about to be destroyed.

        """
        self.releaseResources()
        self.__listVAP = None

    def releaseResources(self):
        """ deconfigure vap's SSID """
        for vap in self.__listVAP:
            vap.ssid = None

    def __get_msg_id(self):
        """ returns the current ID number to be used in the message and
        increment this id by 1
        """
        id = self.__msg_id
        self.__msg_id += 1
        return id

    @property
    def id(self):
        """ returns the network's internal class ID
        """
        return self.__id

    @property
    def vaps(self):
        """ returns VAPs associated to this network
        """
        return self.__listVAP

    @property
    def SSID(self):
        """ returns the SSID of this network
        """
        return self.__SSID

    @SSID.setter
    def SSID(self, newSSID, keepenabled=False):
        """ change the SSID of the network
        """
        # this newSSID already exists in some network?
        if newSSID in list_of_networks():
            raise ValueError("ssid already exists!")

        del_network(self)

        self.__SSID = newSSID
        add_network(self)
        # change vaps and network SSID
        for vap in self.__listVAP:
            vap.ssid = newSSID
        if keepenabled:
            vap.enabled = True

    def associateVirtualAP(self, vap):
        """ join the vap to the network.
            called by ssid.setter in VAP class
        """
        if isinstance(vap, VAP) and not(vap in self.__listVAP):
            self.__listVAP.append(vap)

    def deassociateVirtualAP(self, vap):
        """ releases the vap from the network
            called by ssid.setter in VAP class
        """
        if isinstance(vap, VAP) and (vap in self.__listVAP):
            vap.enable = False
            vap.ssid = None
            self.__listVAP.remove(vap)

    def handoffUser(station, new_vap):
        """ handles handoff. This method relies on 802.11 mobility domain
            feature.
            So the station and the AP should be configure to use mobility
            domain.
            This method disassociates the station from a vap in the network and
            moves it to a new_vap in this network.
            It also sends a message to the station,
            using station.triggerTransition(), instructing it to roam to a
            new ap.

            @see: documentacao-para-handover.pdf for instruction on how to set
            up the station and the AP for handover.
            **** not implemented yet ****

        """
        if not isinstance(station, Station):
            raise ValueError("station parameter must be a Station class!")
        if not isinstance(new_vap, VAP):
            raise ValueError("vap parameter must be a VAP class!")

        # TODO: migrate user
        # 1) prepare new vap to get user
        if new_vap.connectNewUser(station):
            # 2) send message to station to request change
            if station.triggerTransition(new_vap):
                # 3) if not change, disconnect from old_vap
                vap = station.vap()
                vap.disassociateUser(station)
        else:
            raise Exception("Cannot connect station " + station +
                            " to ap " + new_vap)
