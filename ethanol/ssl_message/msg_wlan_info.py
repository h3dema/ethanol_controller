#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  implements:
  * req_wlan_info(): MSG_WLAN_INFO

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
from datetime import datetime
from construct import ULInt32, SLInt32, ULInt64, SLInt64, CString
from construct import Embed, Struct, Container, Array
from construct import If

from pox.ethanol.ssl_message.msg_core   import msg_default, decode_default_fields
from pox.ethanol.ssl_message.msg_core   import field_station, field_mac_addr, field_ssid, field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg



# ###############################################################
#
# MSG_TYPE.MSG_WLAN_INFO
#
# ###############################################################
wlan_entry = Struct('wlan_entry',
                    SLInt32('ifindex'),
                    Embed(field_intf_name),
                    ULInt32('wlan_indx'),
                    ULInt32('phy_indx'),
                    ULInt64('dev'),
                    Embed(field_mac_addr),
                    Embed(field_ssid),
                    ULInt32('channel_type'),
                    ULInt32('chan_width'),
                    ULInt32('freq'),
                    ULInt32('freq1'),
                    ULInt32('freq2'),
                    SLInt32('iftype'),
                    )
""" information about a wifi interface"""

msg_wlan_info = Struct('msg_wlan_info',
                       Embed(msg_default),   # default fields
                       Embed(field_station),

                       ULInt32('num_entries'),
                       Array(lambda ctx: ctx.num_entries, wlan_entry),
                       #Probe()
                       )

def req_wlan_info(server, id=0, intf_name_list=None, sta_ip = None, sta_port = 0):
    """
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name_list: names of the wireless interface
      @type intf_name_list: list of str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    if intf_name_list == None:
        return None, None

    """
      returns the information about some interface defined by intf_name
      (or all interfaces if intf_name = None)
    """
    wlan_entry = []
    for intf in intf_name_list:
        entry = Container(
            ifindex = 0,
            intf_name_size = len(intf),
            intf_name = intf,
            wlan_indx = 0,
            phy_indx = 0,
            dev = 0,
            mac_addr_size = 0,
            mac_addr = None,
            ssid_size = 0,
            ssid = None,
            channel_type = 0,
            chan_width = 0,
            freq = 0,
            freq1 = 0,
            freq2 = 0,
            iftype = 0
        )
        wlan_entry.append(entry)
    num_entries = len(wlan_entry)

    #1) create message
    msg_struct = Container(
        m_type = MSG_TYPE.MSG_WLAN_INFO,
        m_id = id,
        p_version_length=len(VERSION),
        p_version = VERSION,
        m_size = 0,
        sta_ip_size = 0 if sta_ip == None else len(sta_ip),
        sta_ip = sta_ip,
        sta_port = sta_port,
        num_entries = num_entries,
        wlan_entry = wlan_entry,
    )

    error, msg = send_and_receive_msg(server, msg_struct, msg_wlan_info.build, msg_wlan_info.parse)
    if not error:
        value = msg['wlan_entry'] if 'wlan_entry' in msg else []
    else:
        value = []

    return msg, value

