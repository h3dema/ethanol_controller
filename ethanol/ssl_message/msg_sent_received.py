#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* send_msg_get_bytesreceived

* send_msg_get_bytessent

* send_msg_get_byteslost

* send_msg_get_packetsreceived

* send_msg_get_packetssent

* send_msg_get_packetslost

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

from construct import SLInt64
from construct import Embed
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default, field_intf_name, field_station
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

msg_sent_received = Struct('msg_sent_received',
                           Embed(msg_default),  # default fields
                           Embed(field_intf_name),
                           Embed(field_station),
                           SLInt64('value'),
                           # Probe()
                           )
""" message structure common to all supported_messages messages"""

supported_messages = [
    MSG_TYPE.MSG_GET_BYTESRECEIVED,
    MSG_TYPE.MSG_GET_BYTESSENT,
    MSG_TYPE.MSG_GET_PACKETSRECEIVED,
    MSG_TYPE.MSG_GET_PACKETSSENT,
    MSG_TYPE.MSG_GET_PACKETSLOST,
]
""" this module deals with multiple message types. these types are listed in supported_messages
"""


def send_msg_sent_received(server, id=0, type=None, intf_name=None, sta_ip=None, sta_port=0):
    """ INTERNAL FUNCTION: don't call this function

      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
          value (bytes or packets received or sent or lost)
    """
    if (type is None) or (type not in supported_messages):
        return None, None  # nothing to do if the message type is not defined

    # 1) create message
    msg_struct = Container(
        m_type=type,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        value=0
    )

    error, msg = send_and_receive_msg(server, msg_struct, msg_sent_received.build, msg_sent_received.parse)
    if not error:
        value = msg['value'] if 'value' in msg else -1
    else:
        value = -1

    return msg, value


def send_msg_get_bytesreceived(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    """ requests number of bytes received. this number is always incremented since the interface activation
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    return send_msg_sent_received(server=server, id=id,
                                  type=MSG_TYPE.MSG_GET_BYTESRECEIVED,
                                  intf_name=intf_name, sta_ip=sta_ip, sta_port=sta_port)


def send_msg_get_bytessent(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    """ requests number of bytes sent by the interface. this number is always incremented since the interface activation
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    return send_msg_sent_received(server=server, id=id,
                                  type=MSG_TYPE.MSG_GET_BYTESSENT,
                                  intf_name=intf_name, sta_ip=sta_ip, sta_port=sta_port)


def send_msg_get_packetsreceived(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    """ requests number of packets received by the interface. this number is always incremented since the interface activation
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    return send_msg_sent_received(server=server, id=id,
                                  type=MSG_TYPE.MSG_GET_PACKETSRECEIVED,
                                  intf_name=intf_name, sta_ip=sta_ip, sta_port=sta_port)


def send_msg_get_packetssent(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    """ requests number of packets sent by the interface. this number is always incremented since the interface activation
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    return send_msg_sent_received(server=server, id=id,
                                  type=MSG_TYPE.MSG_GET_PACKETSSENT,
                                  intf_name=intf_name, sta_ip=sta_ip, sta_port=sta_port)


def send_msg_get_packetslost(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    """ requests number of packets lost by the interface. this number is always incremented since the interface activation
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    return send_msg_sent_received(server=server, id=id,
                                  type=MSG_TYPE.MSG_GET_PACKETSLOST,
                                  intf_name=intf_name, sta_ip=sta_ip, sta_port=sta_port)


# exemplo diferente
"""
def send_msg_get_packetslost(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    return send_msg_sent_received(server=server, id=id,
                  type=MSG_TYPE.MSG_GET_PACKETSLOST,
                  intf_name=intf_name, sta_ip=sta_ip, sta_port=sta_port)
"""
