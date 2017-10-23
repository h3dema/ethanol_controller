#!/usr/bin/python
# -*- coding: utf-8 -*-

""" handles the beacon interval information: gets or sets it. Implements:

* get_beacon_interval()

* set_beacon_interval()

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
from construct import Embed, Struct, Container

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

msg_beacon_interval = Struct('msg_beacon_interval',
                             Embed(msg_default),  # default fields
                             Embed(field_intf_name),
                             SLInt32('beacon_interval'),
                             )

ERROR = -1


def get_beacon_interval(server, id=0, intf_name=None):
    """
    get beacon interval in miliseconds for the interface intf_name
    @param server: tuple (ip, port_num)
    @param id: message id
    @param intf_name: name of the wireless interface
    @type intf_name: str

    @return: -1 if an error occurs
    """
    if intf_name is None:
        return None, ERROR

    # 1) create message
    msg_struct = Container(m_type=MSG_TYPE.MSG_GET_BEACON_INTERVAL,
                           m_id=id,
                           p_version_length=len_of_string(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           intf_name_size=len_of_string(intf_name),
                           intf_name=intf_name,
                           beacon_interval=0
                           )
    error, msg = send_and_receive_msg(server, msg_struct, msg_beacon_interval.build, msg_beacon_interval.parse)
    if not error:
        value = msg['beacon_interval'] if 'beacon_interval' in msg else []
    else:
        value = []

    return msg, value


def set_beacon_interval(server, id=0, intf_name=None, beacon_interval=100):
    """
      set the beacon interval (in ms)
      default = 100ms
      different brands and models offer different allowable beacon interval ranges

      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param beacon_interval:
      @type beacon_interval: int
    """
    # create message container
    msg_struct = Container(m_type=MSG_TYPE.MSG_SET_BEACON_INTERVAL,
                           m_id=id,
                           p_version_length=len_of_string(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           intf_name_size=len_of_string(intf_name),
                           intf_name=intf_name,
                           beacon_interval=beacon_interval,
                           )

    send_and_receive_msg(server, msg_struct, msg_beacon_interval.build, msg_beacon_interval.parse, only_send=True)
