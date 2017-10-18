#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
implements the following messages: 

* set_ap_dtiminterval

* get_ap_dtiminterval


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
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

msg_ap_dtiminterval = Struct('msg_ap_dtiminterval',
                             Embed(msg_default),  # default fields
                             Embed(field_intf_name),
                             SLInt32('dtim_interval'),
                             # Probe()
                             )


def get_ap_dtiminterval(server, id=0, intf_name=None):
    """ get the DTIM interval set in the interface intf_name
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
        m_type=MSG_TYPE.MSG_GET_AP_DTIMINTERVAL,
        m_id=id,
        p_version_length=len(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=0 if intf_name is None else len(intf_name),
        intf_name=intf_name,
        dtim_interval=-1,
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_ap_dtiminterval.build, msg_ap_dtiminterval.parse)
    if not error:
        value = msg['dtim_interval'] if 'dtim_interval' in msg else None
    else:
        value = None

    return msg, value


def set_ap_dtiminterval(server, id=0, intf_name=None, dtim_interval=100):
    """ set the DTIM interval of the interface intf_name
        @param server: tuple (ip, port_num)
        @param id: message id
        @param intf_name: name of the wireless interface
        @type intf_name: str
        @param dtim_interval: DTIM interval
        @type dtim_interval: int
        @note: https://routerguide.net/dtim-interval-period-best-setting/
  
    """
    if intf_name is None:
        return None, None

    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_SET_AP_DTIMINTERVAL,
        m_id=id,
        p_version_length=len(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=0 if intf_name is None else len(intf_name),
        intf_name=intf_name,
        dtim_interval=dtim_interval,
    )
    send_and_receive_msg(server, msg_struct, msg_ap_dtiminterval.build, msg_ap_dtiminterval.parse, only_send=True)
