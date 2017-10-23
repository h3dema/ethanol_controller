#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* get_sta_link_info

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

from construct import SLInt32
from construct import Embed
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_station, field_ssid, field_intf_name, field_mac_addr
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

msg_sta_link_info = Struct('msg_sta_link_info',
                           Embed(msg_default),
                           Embed(field_intf_name),
                           Embed(field_station),
                           Embed(field_mac_addr),
                           Embed(field_ssid),
                           SLInt32('frequency'),
                           )


def get_sta_link_info(server, id=0, sta_ip=None, sta_port=0, intf_name=None):
    """
      returns three values: mac_addr, ssid, frequency
      None equals an error has occured (or no interface found)

      @todo: Nao eh necessario retornar intf_name

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
    if intf_name is None:
        return None, None, None, None, None

    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_GET_LINK_INFO,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        ssid=None,
        ssid_size=0,
        mac_addr=None,
        mac_addr_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        frequency=0,
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_sta_link_info.build, msg_sta_link_info.parse)
    if not error:
        mac_addr = msg['mac_addr'] if 'mac_addr' in msg else None
        ssid = msg['ssid'] if 'ssid' in msg else None
        freq = msg['frequency'] if 'frequency' in msg else -1
        intf_name = msg['intf_name'] if 'intf_name' in msg else None
    else:
        mac_addr = None
        ssid = None
        freq = -1
        intf_name = None

    return msg, mac_addr, ssid, freq, intf_name
