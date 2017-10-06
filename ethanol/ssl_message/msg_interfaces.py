#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* get_one_intf

* get_interfaces

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

from construct import SLInt8, ULInt32, SLInt64
from construct import Embed
from construct import Struct, Container, Array
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_station, field_intf_name, field_mac_addr
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION, send_and_receive_msg, tri_boolean

intfs = Struct('intfs',
               SLInt64('ifindex'),
               Embed(field_intf_name),
               ULInt32('intf_type'),
               Embed(field_mac_addr),
               SLInt8('is_wifi'),
               )

msg_intf = Struct('msg_intf',
                  Embed(msg_default),   # default fields
                  Embed(field_station),
                  ULInt32('num_intf'),
                  Array(lambda ctx: ctx.num_intf, intfs),
                  # Probe()
                  )


def __get_intf(server, m_id=0, intf_name=[], sta_ip=None, sta_port=0, m_type=None):
    """
     internal function: provides suporte to get_interfaces and get_one_intf
      @param server: tuple (ip, port_num)
      @param m_id: message m_id
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
    if m_type not in [MSG_TYPE.MSG_GET_ALL_INTF, MSG_TYPE.MSG_GET_ONE_INTF]:
        return None, None

    value = None
    """
      returns the value
      None equals an error has occured (or no interface found)
    """

    if intf_name is None:
        intf_name = []

    intfs = []
    for intf in intf_name:
        entry = Container(ifindex=0,
                          intf_name_size=0 if intf_name is None else len(intf_name),
                          intf_name=intf_name,
                          intf_type=0,
                          mac_addr_size=0,
                          mac_addr=None,
                          is_wifi=True,
                          )
        intfs.append(entry)
    num_intf = len(intfs)

    # 1) create message
    msg_struct = Container(m_type=m_type,
                           m_id=m_id,
                           p_version_length=len(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           sta_ip_size=0 if sta_ip is None else len(sta_ip),
                           sta_ip=sta_ip,
                           sta_port=sta_port,
                           num_intf=num_intf,
                           intfs=intfs,
                           )
    # print msg_struct
    error, msg = send_and_receive_msg(server, msg_struct, msg_intf.build, msg_intf.parse)
    # print msg
    if not error:
        value = msg['intfs'] if 'intfs' in msg else []
    else:
        value = []

    for v in value:
        is_wifi = tri_boolean('is_wifi', v)
        v['is_wifi'] = is_wifi

    return msg, value


def get_one_intf(server, m_id=0, intf_name=None, sta_ip=None, sta_port=0):
    """ MSG_GET_ONE_INTF: eturns info of interface "intf_name"
      @param server: tuple (ip, port_num)
      @param m_id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    return __get_intf(server=server, m_id=m_id, intf_name=intf_name,
                      sta_ip=sta_ip, sta_port=sta_port, m_type=MSG_TYPE.MSG_GET_ONE_INTF)


def get_interfaces(server, m_id=0, sta_ip=None, sta_port=0):
    """ MSG_GET_ALL_INTF: returns all interfaces
      @param server: tuple (ip, port_num)
      @param m_id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    return __get_intf(server=server, m_id=m_id, intf_name=[],
                      sta_ip=sta_ip, sta_port=sta_port, m_type=MSG_TYPE.MSG_GET_ALL_INTF)
