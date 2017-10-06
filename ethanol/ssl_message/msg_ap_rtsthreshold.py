#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* get_ap_rtsthreshold

* set_ap_rtsthreshold

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
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

msg_ap_rtsthreshold = Struct('msg_ap_rtsthreshold',
                             Embed(msg_default),   # default fields
                             Embed(field_intf_name),
                             ULInt32('rts_threshold'),
                             # Probe(),
                             )


def get_ap_rtsthreshold(server, id=0, intf_name=None):
  """ verify is the interface is broadcasting the SSID
    @param server: tuple (ip, port_num)
    @param id: message id
    @param intf_name: name of the wireless interface
    @type intf_name: str
    @return: msg, value
  """
  if intf_name==None:
    return None, None

  #1) create message
  msg_struct = Container(
                  m_type = MSG_TYPE.MSG_GET_AP_RTSTHRESHOLD,
                  m_id = id,
                  p_version_length=len(VERSION),
                  p_version = VERSION,
                  m_size = 0,
                  intf_name_size = 0 if intf_name == None else len(intf_name),
                  intf_name = intf_name,
                  rts_threshold = 0,
               )
  error, msg = send_and_receive_msg(server, msg_struct, msg_ap_rtsthreshold.build, msg_ap_rtsthreshold.parse)
  if not error:
    value = msg['enabled'] if 'enabled' in msg else None
  else:
    value = None

  return msg, value

def set_ap_rtsthreshold(server, id=0, intf_name=None, rts_threshold=0):
  """ enable or disable the broadcasting of the SSID
    @param server: tuple (ip, port_num)
    @param id: message id
    @param intf_name: name of the wireless interface
    @type intf_name: str
  """
  if intf_name==None:
    return None, None

  #1) create message
  msg_struct = Container(
                  m_type = MSG_TYPE.MSG_SET_AP_RTSTHRESHOLD,
                  m_id = id,
                  p_version_length=len(VERSION),
                  p_version = VERSION,
                  m_size = 0,
                  intf_name_size = 0 if intf_name == None else len(intf_name),
                  intf_name = intf_name,
                  rts_threshold = rts_threshold,
               )
  send_and_receive_msg(server, msg_struct, msg_ap_rtsthreshold.build, msg_ap_rtsthreshold.parse, only_send=True)
