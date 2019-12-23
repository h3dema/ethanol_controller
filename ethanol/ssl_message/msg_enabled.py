#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* is_802_11e_enabled

* is_fastbsstransition_compatible

no process is implemented: the controller is not supposed to respond to these message

@author: Henrique Duarte Moura
@organization: WINET/DCC/UFMG
@copyright: h3dema (c) 2017
@contact: henriquemoura@hotmail.com
@licence: GNU General Public License v2.0
(https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
@since: July 2015
@status: in development

@requires: construct 2.5.2
"""

from construct import SLInt8
from construct import Embed
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_station, field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION, DEFAULT_WIFI_INTFNAME
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, tri_boolean, len_of_string

msg_enabled = Struct('msg_enabled',
                     Embed(msg_default),  # default fields
                     Embed(field_intf_name),
                     Embed(field_station),
                     SLInt8('value'),
                     # Probe(),
                     )


def is_802_11e_enabled(server, id=0, intf_name=DEFAULT_WIFI_INTFNAME, sta_ip=None, sta_port=0):
    """ verifies if 802.11e is supported and is enabled
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: names of the wireless interface
      @type intf_name: list of str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    return __get_enabled(server=server, id=id,
                         sta_ip=sta_ip, sta_port=sta_port, intf_name=intf_name, m_type=MSG_TYPE.MSG_GET_802_11E_ENABLED)


def is_fastbsstransition_compatible(server, id=0, intf_name=DEFAULT_WIFI_INTFNAME, sta_ip=None, sta_port=0):
    """ checks if the interface supports fast BSS transition feature
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: names of the wireless interface
      @type intf_name: list of str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    return __get_enabled(server=server, id=id,
                         sta_ip=sta_ip, sta_port=sta_port, m_type=MSG_TYPE.MSG_GET_FASTBSSTRANSITION_COMPATIBLE)


def __get_enabled(server, id=0, intf_name=None, sta_ip=None, sta_port=0, m_type=None):
    """
     internal function: provides suporte to get_interfaces and get_one_intf

      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: names of the wireless interface
      @type intf_name: list of str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int
      @param m_type: message type
      @type m_type: int

      @return: msg - received message
    """
    if intf_name is None or m_type not in [MSG_TYPE.MSG_GET_802_11E_ENABLED,
                                           MSG_TYPE.MSG_GET_FASTBSSTRANSITION_COMPATIBLE]:
        return None, None

    """
      returns the value
      None equals an error has occured (or no interface found)
    """
    value = None

    # 1) create message
    msg_struct = Container(
        m_type=m_type,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        value=False,
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_enabled.build, msg_enabled.parse)
    if not error:
        value = tri_boolean('value', msg)
    else:
        value = []

    return msg, value
