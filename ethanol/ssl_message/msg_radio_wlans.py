#!/usr/bin/python
# -*- coding: utf-8 -*-

"""implements the following messages:

* get_radio_wlans() : MSG_GET_RADIO_WLANS

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
from construct import Embed, Array
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_station, field_intf_name, field_mac_addr
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

# ###############################################################
#
# MSG_TYPE.MSG_GET_RADIO_WLANS
#
# ###############################################################

""" info about one wlan"""
list_of_radio_wlans = Struct('list_of_radio_wlans',
                             Embed(field_intf_name),
                             Embed(field_mac_addr),
                             ULInt32('wiphy'),
                             )

""" message structure """
msg_radio_wlans = Struct('msg_radio_wlans',
                         Embed(msg_default),  # default fields
                         Embed(field_station),
                         ULInt32('num_wlans'),
                         Array(lambda ctx: ctx.num_wlans, list_of_radio_wlans),
                         # Probe()
                         )


def get_radio_wlans(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    """ requests the radio wlans, if intf_name is not None, only this interface is considered, otherwise returns all wireless interfaces

      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
      @return: value
    """
    value = []
    """
      returns the value
      None equals an error has occured (or no interface found)
    """

    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_GET_RADIO_WLANS,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        num_wlans=0,
        list_of_radio_wlans=[],
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_radio_wlans.build, msg_radio_wlans.parse)
    if not error:
        value = msg['list_of_radio_wlans'] if 'list_of_radio_wlans' in msg else None
    else:
        value = []

    return msg, value
