#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  implements:
  * set_txqueuelen
  * set_mtu

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

from construct import SLInt32
from construct import Embed, Struct, Container

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_station
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

msg_mtu_qlen = Struct('msg_mtu_qlen',
                      Embed(msg_default),  # default fields
                      Embed(field_station),
                      Embed(field_intf_name),
                      SLInt32('value'),
                      )
""" message structure """


def set_msg_mtu_qlen(server, m_type, m_id=0, sta_ip=None, sta_port=0, intf_name=None, value=None):
    """ sets the MTU or Queue Len values
    @param server: tuple (ip, port_num)
    @param id: message id
    @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
    @type sta_ip: str
    @param sta_port: socket port number of the station
    @type sta_port: int
    @param intf_name: name of the interface
    """
    if intf_name is None or \
                    m_type not in [MSG_TYPE.MSG_SET_TXQUEUELEN, MSG_TYPE.MSG_SET_MTU] or \
            not isinstance(value, int):
        return

    msg_struct = Container(m_type=m_type,
                           m_id=m_id,
                           p_version_length=len(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           sta_ip_size=0 if sta_ip is None else len(sta_ip),
                           sta_ip=sta_ip,
                           sta_port=sta_port,
                           intf_name_size=0 if intf_name is None else len(intf_name),
                           intf_name=intf_name,
                           value=value,
                           )
    send_and_receive_msg(server, msg_struct, msg_mtu_qlen.build, msg_mtu_qlen.parse, only_send=True)


def set_mtu(server, m_id=0, sta_ip=None, sta_port=0, intf_name=None, mtu=None):
    set_msg_mtu_qlen(server,
                     MSG_TYPE.MSG_SET_MTU,
                     m_id=m_id,
                     sta_ip=sta_ip,
                     sta_port=sta_port,
                     intf_name=intf_name,
                     value=mtu)


def set_txqueuelen(server, m_id=0, sta_ip=None, sta_port=0, intf_name=None, txqueuelen=None):
    set_msg_mtu_qlen(server,
                     MSG_TYPE.MSG_SET_TXQUEUELEN,
                     m_id=m_id,
                     sta_ip=sta_ip,
                     sta_port=sta_port,
                     intf_name=intf_name,
                     value=txqueuelen)
