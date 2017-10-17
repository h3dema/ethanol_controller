#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  implements:
  * get_preamble
  * set_preamble

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
from construct import SLInt32, LFloat32, CString
from construct import Embed, Struct, Container
from construct import If


from pox.ethanol.ssl_message.msg_core   import msg_default
from pox.ethanol.ssl_message.msg_core   import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg
from pox.ethanol.ssl_message.msg_common import DEFAULT_WIFI_INTFNAME

msg_preamble = Struct('msg_preamble',
                      Embed(msg_default),   # default fields
                      Embed(field_intf_name),
                      SLInt32('preamble'),
                      )


def get_preamble(server, id=0, intf_name=DEFAULT_WIFI_INTFNAME):
    """ gets if the configured preamble is long or short
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str

      @return: msg - received message
    """
    #1) create message
    msg_struct = Container(
        m_type = MSG_TYPE.MSG_GET_PREAMBLE,
        m_id = id,
        p_version_length=len(VERSION),
        p_version = VERSION,
        m_size = 0,
        intf_name_size = 0 if intf_name == None else len(intf_name),
        intf_name = intf_name,
        preamble = 0
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_preamble.build, msg_preamble.parse)
    if not error:
        value = msg['preamble'] if 'preamble' in msg else -1
    else:
        value = -1

    return msg, value


def set_preamble(server, id=0, intf_name=DEFAULT_WIFI_INTFNAME, preamble=0):
    """ set the preamble used in some interface
        0 = preamble LONG | 1 = preamble SHORT
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param preamble:
      @type sta_ip: bool

      @return: msg - received message
    """
    if preamble != 1: preamble = 0 # default equals LONG

    # create message container
    msg_struct = Container(
        m_type = MSG_TYPE.MSG_SET_PREAMBLE,
        m_id = id,
        p_version_length=len(VERSION),
        p_version = VERSION,
        m_size = 0,
        intf_name_size = 0 if intf_name == None else len(intf_name),
        intf_name = intf_name,
        preamble = preamble
    )
    send_and_receive_msg(server, msg_struct, msg_preamble.build, msg_preamble.parse, only_send = True)

