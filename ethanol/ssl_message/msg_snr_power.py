#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* get_snr: MSG_GET_SNR

* get_txpower: MSG_GET_TXPOWER

* set_txpower: MSG_SET_TXPOWER

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
from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core   import msg_default, decode_default_fields, field_intf_name, field_station
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

msg_snr_power = Struct('msg_snr_power',
                    Embed(msg_default),   # default fields
                    Embed(field_intf_name),
                    Embed(field_station),
                    SLInt64('value'), # snr or tx_power
                    #Probe()
                )


def get_snr_power(server, id=0, intf_name=None, sta_ip=None, sta_port=0, m_type=None):
  """INTERVAL FUNCTION: DON'T CALL THIS METHOD.

    @param server: tuple (ip, port_num)
    @param id: message id
    @param intf_name: name of the wireless interface
    @type intf_name: str
    @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
    @type sta_ip: str 
    @param sta_port: socket port number of the station
    @type sta_port: int

    @return: msg - received message
    @return: the value
    -1 equals an error has occured
  """

  if intf_name == None or m_type not in [ MSG_TYPE.MSG_GET_SNR, MSG_TYPE.MSG_GET_TXPOWER]:
    return None, -1

  #1) create message
  msg_struct = Container(
                  m_type = m_type,
                  m_id = id,
                  p_version_length=len(VERSION),
                  p_version = VERSION,
                  m_size = 0,
                  intf_name_size = 0 if intf_name == None else len(intf_name),
                  intf_name = intf_name,
                  sta_ip_size = 0 if sta_ip == None else len(sta_ip),
                  sta_ip = sta_ip,
                  sta_port = sta_port,
                  value = 0
               )


  error, msg = send_and_receive_msg(server, msg_struct, msg_snr_power.build, msg_snr_power.parse)
  #print msg

  if not error:
    value = msg['value'] if 'value' in msg else -1
  else:
    value = -1

  return msg, value

def get_snr(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
  """ obtain SNR
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
  return get_snr_power(server, id=id, intf_name=intf_name,
          sta_ip=sta_ip, sta_port=sta_port, m_type=MSG_TYPE.MSG_GET_SNR)

def get_txpower(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
  """ obtain txpower
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
  return get_snr_power(server, id=id, intf_name=intf_name, sta_ip=sta_ip,
          sta_port=sta_port, m_type=MSG_TYPE.MSG_GET_TXPOWER)

def set_txpower(server, id=0, intf_name=None, sta_ip=None, sta_port=0, txpower=None):
  """ set the txpower for the wireless interfacce
    @param server: tuple (ip, port_num)
    @param id: message id
    @param intf_name: name of the wireless interface
    @type intf_name: str
    @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
    @type sta_ip: str 
    @param sta_port: socket port number of the station
    @type sta_port: int
  """
  if txpower==None and isinstance(txpower, int):
    return

  #1) create message
  msg_struct = Container(
                  m_type = MSG_TYPE.MSG_SET_TXPOWER,
                  m_id = id,
                  p_version_length=len(VERSION),
                  p_version = VERSION,
                  m_size = 0,
                  intf_name_size = 0 if intf_name == None else len(intf_name),
                  intf_name = intf_name,
                  sta_ip_size = 0 if sta_ip == None else len(sta_ip),
                  sta_ip = sta_ip,
                  sta_port = sta_port,
                  value = txpower
               )

  msg = msg_snr_power.build(msg_struct)
  send_and_receive_msg(server, msg_struct, msg_snr_power.build, msg_snr_power.parse, only_send = True)
