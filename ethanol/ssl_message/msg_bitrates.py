#!/usr/bin/python
# -*- coding: utf-8 -*-

"""implements the following messages:

* MSG_GET_TX_BITRATES: get_tx_bitrates

* MSG_GET_TX_BITRATE : get_tx_bitrate

* MSG_SET_TX_BITRATES: TODO

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

from construct import ULInt32, LFloat32, ULInt8
from construct import Embed
from construct import Array, Struct, Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core   import msg_default, decode_default_fields
from pox.ethanol.ssl_message.msg_core   import field_intf_name
from pox.ethanol.ssl_message.msg_core   import field_station
from pox.ethanol.ssl_message.msg_core   import field_mac_addr
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

iw_bitrates = Struct('iw_bitrates',
                     LFloat32("bitrate"),
                     ULInt8('is_short'), # this is a boolean coded as a byte
                     )

iw_bands = Struct('iw_bands',
                  Embed(field_intf_name),
                  ULInt32('band'),
                  ULInt32('num_bitrates'),
                  # Probe(),
                  Array(lambda ctx: ctx.num_bitrates, iw_bitrates),
                  )

msg_tx_bitrates = Struct('msg_tx_bitrates',
                    Embed(msg_default),   # default fields
                    Embed(field_intf_name),
                    Embed(field_station),
                    ULInt32('num_bands'),
                    # Probe(),
                    Array(lambda ctx: ctx.num_bands, iw_bands),
                )


def get_tx_bitrates(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
  """ get the channels the interface intf_name supports, this function applies to access points

    @param server: tuple (ip, port_num)
    @param id: message id
    @param intf_name: name of the wireless interface
    @type intf_name: str
    @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
    @type sta_ip: str 
    @param sta_port: socket port number of the station
    @type sta_port: int
    @return: a dictionary, the index is the band
  """
  if intf_name==None:
    raise ValueError("intf_name must have a valid value!")
  #1) create message
  msg_struct = Container(
                  m_type = MSG_TYPE.MSG_GET_TX_BITRATES,
                  m_id = id,
                  p_version_length=len(VERSION),
                  p_version = VERSION,
                  m_size = 0,
                  intf_name_size = 0 if intf_name == None else len(intf_name),
                  intf_name = intf_name,
                  sta_ip_size = 0 if sta_ip == None else len(sta_ip),
                  sta_ip = sta_ip,
                  sta_port = sta_port,
                  num_bands = 0,    # don´t know how many bands are in the AP
                  iw_bands = [],    # field will be filled by the AP
               )
  error, msg = send_and_receive_msg(server, msg_struct, msg_tx_bitrates.build, msg_tx_bitrates.parse)
  value = dict()
  if not error or ('iw_bands' not in msg):
    for v in msg['iw_bands']:
      bitrates = []
      is_short = []
      for e in v['iw_bitrates']:
        bitrates.append(e['bitrate'])
        is_short.append(e['is_short']==1)
      value[v['band']] = { 'intf_name': v['intf_name'],
                           'bitrates' : bitrates,
                           'support_short' : is_short, # if this bitrate supports short preamble or not
                         }

  """
    returns the value, note: {} equals an error has occured or no band found
  """
  return msg, value



msg_tx_bitrate = Struct('msg_tx_bitrate',
                    Embed(msg_default),   # default fields
                    Embed(field_intf_name),
                    Embed(field_station),
                    Embed(field_mac_addr),
                    LFloat32('bitrate'),
                    #Probe()
                )
""" ************************* MSG_TYPE.MSG_GET_TX_BITRATE ************************* """

def get_tx_bitrate(server, id=0, intf_name=None, sta_ip=None, sta_port=0, sta_mac=None):
  """ get the channels the interface intf_name supports, applies to access points
    @param server: tuple (ip, port_num)
    @param id: message id
    @param intf_name: name of the wireless interface
    @type intf_name: str
    @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
    @type sta_ip: str 
    @param sta_port: socket port number of the station
    @type sta_port: int
    @param sta_mac: if None, scan for all stations. If specified (str with MAC address dotted format), returns only the station, if connected
  """
  if intf_name==None:
    raise ValueError("intf_name must have a valid value! Received %s" % intf_name)
  if sta_mac==None:
    raise ValueError("sta_mac must have a valid value! Received %s" % sta_mac)
  #1) create message
  msg_struct = Container(
                  m_type = MSG_TYPE.MSG_GET_TX_BITRATE,
                  m_id = id,
                  p_version_length=len(VERSION),
                  p_version = VERSION,
                  m_size = 0,
                  intf_name_size = 0 if intf_name == None else len(intf_name),
                  intf_name = intf_name,
                  sta_ip_size = 0 if sta_ip == None else len(sta_ip),
                  sta_ip = sta_ip,
                  sta_port = sta_port,
                  mac_addr_size = 0 if sta_mac == None else len(sta_mac),
                  mac_addr = sta_mac,
                  bitrate = 0,
               )
  error, msg = send_and_receive_msg(server, msg_struct, msg_tx_bitrate.build, msg_tx_bitrate.parse)
  if not error:
    value = msg['bitrate'] if 'bitrate' in msg else -1
  else:
    value = -1

  """
    returns the value, -1 equals an error has occured
  """
  return msg, value
