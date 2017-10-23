#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
implements the following messages:

* get_ap_frameburstenabled

* set_ap_frameburstenabled


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

from construct import SLInt8
from construct import Embed
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, tri_boolean, len_of_string

msg_ap_frameburstenabled = Struct('msg_ap_frameburstenabled',
                                  Embed(msg_default),  # default fields
                                  Embed(field_intf_name),
                                  SLInt8('enabled'),
                                  # Probe()
                                  )


def get_ap_frameburstenabled(server, id=0, intf_name=None):
    """
        if frame burst is enabled

        @param server: tuple (ip, port_num)
        @param id: message id
        @param intf_name: name of the wireless interface
        @type intf_name: str

        @return msg: received message
        @return value:
    """
    if intf_name is None:
        return None, None

    """
      returns the value
      None equals an error has occured (or no interface found)
    """
    value = None

    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_GET_AP_FRAMEBURSTENABLED,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        enabled=False,
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_ap_frameburstenabled.build,
                                      msg_ap_frameburstenabled.parse)
    if not error:
        value = tri_boolean('enabled', msg)
    else:
        value = None

    return msg, value


def set_ap_frameburstenabled(server, id=0, intf_name=None, enabled=False):
    """

        @param server: tuple (ip, port_num)
        @param id: message id
        @param intf_name: name of the wireless interface
        @type intf_name: str
        @param enabled: enables or disables frame burst
        @type enabled: bool
    """
    if intf_name is None:
        return None, None

    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_SET_AP_FRAMEBURSTENABLED,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        enabled=enabled,
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_ap_frameburstenabled.build,
                                      msg_ap_frameburstenabled.parse, only_send=True)
