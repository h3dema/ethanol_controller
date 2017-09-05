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

from construct import SLInt32, SLInt64
from construct import Embed
from construct import Array
from construct import Struct
from construct import Container
from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core   import msg_default
from pox.ethanol.ssl_message.msg_core   import field_intf_name, field_station
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

msg_acs = Struct('msg_ap_in_range',
                    Embed(msg_default),   # default fields
                    Embed(field_intf_name),
                    Embed(field_station),
                    SLInt32('num_tests'),
                    SLInt32('num_chan'),
                    Array(lambda ctx: ctx.num_chan, SLInt32('freq')), # int
                    Array(lambda ctx: ctx.num_chan, SLInt64('factor')), # long double == LFloat64 ??
                    #Probe(),
                )

ACS_SCALE_FACTOR = 1000000000000000000.0

def get_acs(server, id=0, intf_name=None, sta_ip = None, sta_port = 0, num_tests = 1):
  """ request the ap to provide ACS information
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: name of the wireless interface
      @type intf_name: str
      @param sta_ip: ip address of a station to which this message should be relayed. If None don't relay message, server should process the request
      @param sta_port: socket port of the station
      @param num_tests: number of tests (greater than or equal to 1) that should be executed
      @param num_tests: int

      @return msg: received message
      @return num_chan: number of channels scanned by the device
      @return acs: list of acs factor for each channels
  """
  if intf_name==None:
    return None, 0, []
  if num_tests < 1:
    num_tests = 1 # at least one test

  #1) create message
  msg_struct = Container(
                  m_type = MSG_TYPE.MSG_GET_ACS,
                  m_id = id,
                  p_version_length=len(VERSION),
                  p_version = VERSION,
                  m_size = 0,
                  intf_name_size = 0 if intf_name == None else len(intf_name),
                  intf_name = intf_name,
                  sta_ip_size = 0 if sta_ip == None else len(sta_ip),
                  sta_ip = sta_ip,
                  sta_port = sta_port,
                  num_tests = num_tests,
                  num_chan = 0,    # don´t know how many channels yet
                  freq = [],  # field will be filled by the AP
                  factor = [],  # field will be filled by the AP
               )

  error, msg = send_and_receive_msg(server, msg_struct, msg_acs.build, msg_acs.parse)

  acs = {}
  if not error:
    num_chan = msg['num_chan'] if 'num_chan' in msg else 0
    for i in range(len(msg['freq'])):
      freq = msg['freq'][i]
      factor = msg['factor'][i] / ACS_SCALE_FACTOR
      acs[freq] = factor
  else:
    num_chan = 0
  return msg, num_chan, acs

