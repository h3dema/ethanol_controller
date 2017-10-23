#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  implements:
  * get_ap_ssids

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

from construct import SLInt32, ULInt32
from construct import Embed, Struct, Container, Array

from pox.ethanol.ssl_message.msg_core import msg_default, field_ssid, field_station, field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

ssid_info = Struct('ssid_info',
                   Embed(field_intf_name),
                   Embed(field_ssid),
                   ULInt32('channel'),
                   ULInt32('frequency'),
                   )
""" information about the configured SSID: wiphy, ESSID, channel, frequency, mode
"""

msg_ap_ssid = Struct('msg_ap_ssid',
                     Embed(msg_default),  # default fields
                     Embed(field_station),
                     SLInt32('num_ssids'),
                     Array(lambda ctx: ctx.num_ssids, ssid_info),
                     )
""" message structure """


def get_ap_ssids(server, id=0, sta_ip=None, sta_port=0, intf_names=[]):
    """ returns the channel and frequency of the ssid for each intf_names
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_names: names of the wireless interface
      @type intf_names: list of str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int
    """
    num_ssids = len(intf_names)
    ssid_info = []
    for intf in intf_names:
        entry = Container(intf_name_size=len_of_string(intf),
                          intf_name=intf,
                          ssid_size=0,
                          ssid=None,
                          channel=0,
                          frequency=0,
                          )
        ssid_info.append(entry)

    msg_struct = Container(
        m_type=MSG_TYPE.MSG_GET_AP_SSID,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        num_ssids=num_ssids,
        ssid_info=ssid_info,
    )

    error, msg = send_and_receive_msg(server, msg_struct, msg_ap_ssid.build, msg_ap_ssid.parse)
    if not error:
        value = msg['ssid_info'] if 'ssid_info' in msg else []
    else:
        value = []

    return msg, value
