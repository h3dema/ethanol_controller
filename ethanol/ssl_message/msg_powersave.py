#!/usr/bin/python
# -*- coding: utf-8 -*-

"""implements the following messages:

* get_powersave_mode(intf_name)

* set_powersave_mode(intf_name, powersave_mode)

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

from construct import ULInt32, SLInt32
from construct import Embed
from construct import Array, Struct, Container
from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default, decode_default_fields
from pox.ethanol.ssl_message.msg_core import field_intf_name, field_station
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

msg_powersave = Struct('msg_powersave',
                       Embed(msg_default),  # default fields
                       Embed(field_intf_name),
                       Embed(field_station),
                       ULInt32('value'),
                       # Probe()
                       )


def get_powersave_mode(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    """ get if the powersave is set or not
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """

    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_GET_POWERSAVEMODE,
        m_id=id,
        p_version_length=len(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=0 if intf_name == None else len(intf_name),
        intf_name=intf_name,
        sta_ip_size=0 if sta_ip == None else len(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        value=0,
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_powersave.build, msg_powersave.parse)
    if not error:
        value = True if ('value' in msg) and (msg['value'] == 1) else False
    else:
        value = False

    return msg, value


def set_powersave_mode(server, id=0, powersave=True, intf_name=None, sta_ip=None, sta_port=0):
    """
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int
      """
    if intf_name is None:
        return
    """ set the powersave mode """
    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_SET_POWERSAVEMODE,
        m_id=id,
        p_version_length=len(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=0 if intf_name is None else len(intf_name),
        intf_name=intf_name,
        value=powersave,
    )
    send_and_receive_msg(server, msg_struct, msg_powersave.build, msg_powersave.parse, only_send=True)
