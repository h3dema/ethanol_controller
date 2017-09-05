#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
implements the following messages: 

* get_ap_in_range

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

from construct import ULInt32, SLInt32, SLInt64, LFloat32, SLInt8
from construct import Embed, If
from construct import Array
from construct import Struct
from construct import Container
from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core   import msg_default
from pox.ethanol.ssl_message.msg_core   import field_mac_addr, field_ssid, field_intf_name, field_station
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg


ap_in_range = Struct('ap_in_range',
                      Embed(field_intf_name),
                      Embed(field_mac_addr),
                      Embed(field_ssid),
                      SLInt32('status'),
                      SLInt64('frequency'),
                      SLInt32('channel'),
                      LFloat32('signal'), # float in C is coded as little endian 32 bit number
                      SLInt32('powerconstraint'),
                      SLInt32('tx_power'),
                      SLInt32('link_margin'),
                      SLInt32('age'),
                      SLInt8('is_dBm'), # this is a boolean coded as a 8 bit integer
                  )


msg_ap_in_range = Struct('msg_ap_in_range',
                    Embed(msg_default),   # default fields
                    Embed(field_intf_name),
                    Embed(field_station),
                    ULInt32('num_aps'),
                    Array(lambda ctx: ctx.num_aps, ap_in_range),
                    #Probe(),
                )

def get_ap_in_range(server, id=0, intf_name=None, sta_ip = None, sta_port = 0):
  """ request the ap or the client to try to detect the aps in range, using 802.11 scanning capability

    @param server: tuple (ip, port_num)
    @param id: message id
    @param intf_name: name of the wireless interface
    @type intf_name: str
    @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
    @type sta_ip: str 
    @param sta_port: socket port number of the station
    @type sta_port: int
    @return: msg, num_aps, aps
              the received message (a Container), the number of aps in range, a list of aps (ap_in_range struct)
  """
  if intf_name==None:
    return None, 0, []

  #1) create message
  msg_struct = Container(
                  m_type = MSG_TYPE.MSG_GET_AP_IN_RANGE_TYPE,
                  m_id = id,
                  p_version_length=len(VERSION),
                  p_version = VERSION,
                  m_size = 0,
                  intf_name_size = 0 if intf_name == None else len(intf_name),
                  intf_name = intf_name,
                  sta_ip_size = 0 if sta_ip == None else len(sta_ip),
                  sta_ip = sta_ip,
                  sta_port = sta_port,
                  num_aps = 0,    # don´t know how many aps yet
                  ap_in_range = [],  # field will be filled by the AP
               )

  error, msg = send_and_receive_msg(server, msg_struct, msg_ap_in_range.build, msg_ap_in_range.parse)
  if not error:
    num_aps = msg['num_aps'] if 'num_aps' in msg else 0
    aps = msg['ap_in_range'] if 'ap_in_range' in msg else []
  else:
    num_aps = 0
    aps = []
  return msg, num_aps, aps
