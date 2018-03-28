#!/usr/bin/python
# -*- coding: utf-8 -*-

""" configure hostapd. Implements:

* get_hostapd_conf()

* set_hostapd_conf()

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

from construct import SLInt32, CString
from construct import Embed, Struct, Container, If

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

field_parameter = Struct('param_name',
                         SLInt32('param_name_size'),
                         If(lambda ctx: ctx["param_name_size"] > 0, CString("param_name")),
                         )
""" name of the parameter
"""

field_parameter_value = Struct('param_name_value',
                               SLInt32('param_name_value_size'),
                               If(lambda ctx: ctx["param_name_value_size"] > 0, CString("param_value_name")),
                               )
""" value of the parameter
"""


msg_hostapd_conf = Struct('msg_hostapd_conf',
                          Embed(msg_default),  # default fields
                          Embed(field_intf_name),
                          Embed(field_parameter),
                          Embed(field_parameter_value),
                          )


def get_hostapd_conf(server, id=0, intf_name=None, conf_param=None):
    """
    get beacon interval in miliseconds for the interface intf_name
    @param server: tuple (ip, port_num)
    @param id: message id
    @param intf_name: name of the wireless interface
    @type intf_name: str

    @return: -1 if an error occurs
    """
    if intf_name is None or conf_param is None:
        return None, None

    # 1) create message
    msg_struct = Container(m_type=MSG_TYPE.MSG_GET_HOSTAPD_CONF,
                           m_id=id,
                           p_version_length=len_of_string(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           intf_name_size=len_of_string(intf_name),
                           intf_name=intf_name,
                           param_name_size=len_of_string(conf_param),
                           param_name=conf_param,
                           param_name_value_size=0,
                           param_value_name=None,
                           )
    error, msg = send_and_receive_msg(server, msg_struct, msg_hostapd_conf.build, msg_hostapd_conf.parse)
    if not error:
        value = msg['param_value_name'] if 'param_value_name' in msg else None
    else:
        value = None
    return msg, value


def set_hostapd_conf(server, id=0, intf_name=None, conf_param=None, conf_value=None):
    """
      set the beacon interval (in ms)
      default = 100ms
      different brands and models offer different allowable beacon interval ranges

      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
    """
    # create message container
    msg_struct = Container(m_type=MSG_TYPE.MSG_SET_HOSTAPD_CONF,
                           m_id=id,
                           p_version_length=len_of_string(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           intf_name_size=len_of_string(intf_name),
                           intf_name=intf_name,
                           param_name_size=len_of_string(conf_param),
                           param_name=conf_param,
                           param_name_value_size=len_of_string(conf_value),
                           param_value_name=conf_value,
                           )

    send_and_receive_msg(server, msg_struct, msg_hostapd_conf.build, msg_hostapd_conf.parse, only_send=True)
