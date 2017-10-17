#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* get_ssid

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

from construct import ULInt32
from construct import Embed
from construct import Struct, Array
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_station, field_ssid, field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

ssid_info = Struct('ssid_info',
                   Embed(field_intf_name),
                   Embed(field_ssid),
                   ULInt32('channel'),
                   ULInt32('frequency'),
                   )

msg_ssid = Struct('msg_ssid',
                  Embed(msg_default),   # default fields
                  Embed(field_station),
                  ULInt32('num_ssids'),
                  Array(lambda ctx: ctx.num_ssids, ssid_info),
                  # Probe()
                  )


def get_ssid(server, id=0, intf_name=[], sta_ip=None, sta_port=0):
    """
      returns the value
      None equals an error has occured (or no interface found)
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
    ssid_info = []
    for intf in intf_name:
        entry = Container(intf_name_size=len(intf),
                          intf_name=intf,
                          ssid_size=0,
                          ssid=None,
                          )
        ssid_info.append(entry)
    num_ssids = len(ssid_info)

    #1) create message
    msg_struct = Container(m_type=MSG_TYPE.MSG_GET_AP_SSID,
                           m_id=id,
                           p_version_length=len(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           sta_ip_size=0 if sta_ip is None else len(sta_ip),
                           sta_ip=sta_ip,
                           sta_port=sta_port,
                           num_ssids=num_ssids,
                           ssid_info=ssid_info,
                           )
    error, msg = send_and_receive_msg(server, msg_struct, msg_ssid.build, msg_ssid.parse)
    if not error:
        value = msg['ssid_info'] if 'ssid_info' in msg else None
    else:
        value = None

    return msg, value
