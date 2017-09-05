#!/usr/bin/python
# -*- coding: utf-8 -*-

"""implements the following messages:

* get_frequency

* set_frequency

no process is implemented: the controller is not supposed to answer these message

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

from construct import ULInt32, Embed
from construct import Array, Struct, Container
from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core   import msg_default, decode_default_fields
from pox.ethanol.ssl_message.msg_core   import field_intf_name, field_station, field_ssid
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

msg_frequency = Struct('msg_frequency',
                    Embed(msg_default),   # default fields
                    Embed(field_ssid),
                    Embed(field_intf_name),
                    Embed(field_station),
                    ULInt32('frequency'),
                    #Probe()
                )

def get_frequency(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
  """ the interface is configured to use the frequency returned by this function
      can ask the AP to relay this request to the station if (sta_ip, sta_port) is provided
      
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
  #1) create message
  msg_struct = Container(
                  m_type = MSG_TYPE.MSG_GET_FREQUENCY, 
                  m_id = id,
                  p_version_length=len(VERSION),
                  p_version = VERSION,
                  m_size = 0,
                  ssid_size = 0,
                  ssid = None,
                  intf_name_size = 0 if intf_name == None else len(intf_name),
                  intf_name = intf_name,
                  sta_ip_size = 0 if sta_ip == None else len(sta_ip),
                  sta_ip = sta_ip,
                  sta_port = sta_port,
                  frequency = 0,
               )
  error, msg = send_and_receive_msg(server, msg_struct, msg_frequency.build, msg_frequency.parse)
  if not error:
    value = msg['frequency'] if 'frequency' in msg else -1
  else:
    value = -1

  # print "intf_name", intf_name, "canal ", value
  return msg, value

def set_currentchannel(server, id=0, frequency=None, intf_name=None, sta_ip=None, sta_port=0):
  """ set the current frequency to value provided by the parameter "frequency"

    @param frequency: new channel based on frequency
    @type frequency: int
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
  if frequency == None or not isinstance(frequency, int):
    return
  #1) create message
  msg_struct = Container(
                  m_type = MSG_TYPE.MSG_SET_FREQUENCY, 
                  m_id = id,
                  p_version_length=len(VERSION),
                  p_version = VERSION,
                  m_size = 0,
                  ssid_size = 0,
                  ssid = None,
                  intf_name_size = 0 if intf_name == None else len(intf_name),
                  intf_name = intf_name,
                  sta_ip_size = 0 if sta_ip == None else len(sta_ip),
                  sta_ip = sta_ip,
                  sta_port = sta_port,
                  frequency = frequency,
               )
  send_and_receive_msg(server, msg_struct, msg_frequency.build, msg_frequency.parse, only_send = True)
