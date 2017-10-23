#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
implements the following messages:

* get_ap_guardinterval

* set_ap_guardinterval

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

from construct import SLInt64
from construct import Embed
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

msg_ap_guardinterval = Struct('msg_ap_guardinterval',
                              Embed(msg_default),  # default fields
                              Embed(field_intf_name),
                              SLInt64('guard_interval'),
                              # Probe()
                              )


def get_ap_guardinterval(server, id=0, intf_name=None):
    """ get the guard interval set in the interface intf_name
        @param server: tuple (ip, port_num)
        @param id: message id
        @param intf_name: name of the wireless interface
        @type intf_name: str

        @return msg: received message
        @return value:
    """
    if intf_name is None:
        return None, None

    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_GET_AP_GUARDINTERVAL,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        guard_interval=-1,
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_ap_guardinterval.build, msg_ap_guardinterval.parse)
    if not error:
        value = msg['guard_interval'] if 'guard_interval' in msg else None
    else:
        value = None

    return msg, value


def set_ap_guardinterval(server, id=0, intf_name=None, guard_interval=100):
    """ set the guard interval of the interface intf_name
        @param server: tuple (ip, port_num)
        @param id: message id
        @param intf_name: name of the wireless interface
        @type intf_name: str
        @param guard_interval: time used as guard interval between transmissions
        @type guard_interval: int
    """
    if intf_name is None:
        return None, None

    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_SET_AP_GUARDINTERVAL,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        guard_interval=guard_interval,
    )
    send_and_receive_msg(server, msg_struct, msg_ap_guardinterval.build, msg_ap_guardinterval.parse, only_send=True)
