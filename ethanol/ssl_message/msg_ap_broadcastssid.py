#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
implements the following messages:

* get_acs

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
from construct import Embed
from construct import SLInt8
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name, field_ssid
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, tri_boolean

msg_ap_broadcastssid = Struct('msg_ap_broadcastssid',
                              Embed(msg_default),   # default fields
                              Embed(field_intf_name),
                              Embed(field_ssid),
                              SLInt8('enabled'),
                              # Probe()
                              )


def get_broadcastssid(server, id=0, intf_name=None, ssid=None):
    """ verify is the interface is broadcasting the SSID
        @param server: tuple (ip, port_num)
        @param id: message id
        @param intf_name: name of the wireless interface
        @type intf_name: str

        @return msg: received message
        @return value:
    """
    if intf_name is None or ssid is None:
        return None, None

    #1) create message
    msg_struct = Container(m_type = MSG_TYPE.MSG_GET_AP_BROADCASTSSID,
                           m_id = id,
                           p_version_length=len(VERSION),
                           p_version = VERSION,
                           m_size = 0,
                           intf_name_size = 0 if intf_name is None else len(intf_name),
                           intf_name = intf_name,
                           ssid_size = 0 if ssid is None else len(ssid),
                           ssid = ssid,
                           enabled = False,
                           )
    error, msg = send_and_receive_msg(server, msg_struct, msg_ap_broadcastssid.build, msg_ap_broadcastssid.parse)
    if not error:
        value = tri_boolean('enabled', msg)
    else:
        value = None

    return msg, value

def set_broadcastssid(server, id=0, intf_name=None, enable=False, ssid=None):
  """ enable or disable the broadcasting of the SSID
        @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param enable: set if the SSID should be broadcasted or if it is a hidden SSID
      @param enable: bool
  """
  if intf_name is None or ssid is None:
      return None, None

  #1) create message
  msg_struct = Container(m_type = MSG_TYPE.MSG_SET_AP_BROADCASTSSID,
                         m_id = id,
                         p_version_length=len(VERSION),
                         p_version = VERSION,
                         m_size = 0,
                         intf_name_size = 0 if intf_name is None else len(intf_name),
                         intf_name = intf_name,
                         ssid_size = 0 if ssid is None else len(ssid),
                         ssid = ssid,
                         enabled = enable,
                         )
  send_and_receive_msg(server, msg_struct, msg_ap_broadcastssid.build, msg_ap_broadcastssid.parse, only_send=True)
