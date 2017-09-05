#!/usr/bin/python
# -*- coding: utf-8 -*-
""" implements the BYE message

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
from datetime import datetime
from construct import SLInt32
from construct import Embed
from construct import Struct
from construct import Container

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_error import is_error_msg, get_error_msg
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION, BUFFER_SIZE
from pox.ethanol.ssl_message.msg_common import hex, connect_ssl_socket

from pox.ethanol.events import Events
events_bye = Events()
"""to handle a receiving bye messages, just add your function to events_bye
   your function must use 'def my_funct(**kwargs)' signature for compatibility
   @change: we send to parameters: msg, fromaddr
"""


msg_bye = Struct('msg_bye',
                    Embed(msg_default),   # default fields
                    SLInt32('tcp_port'),
                   )


def send_msg_bye(server, id=0, tcp_port=None):
  """ disconnects the ethanol device from the controller
    @param server: tuple (ip, port_num)
    @param id: message id
    @param tcp_port: socket port number of the device
    @type tcp_port: int
  """
  if (tcp_port is None):
    return None # error

  ssl_sock = connect_ssl_socket(server)

  #print "send_msg_bye id:", id
  #1) create message
  msg_struct = Container(
                m_type = MSG_TYPE.MSG_BYE_TYPE, 
                m_id = id,
                p_version_length=len(VERSION),
                p_version = VERSION,
                m_size = 0,
                tcp_port=tcp_port,
               )
  error, msg = send_and_receive_msg(server, msg_struct, msg_bye.build, msg_bye.parse, only_send = True)

  return msg


def process_bye(received_msg, fromaddr):
  """returns the message to the ssl server process.
     nothing to be done, only send back the same message
     @param func_bye: event
  """
  msg = msg_bye.parse(received_msg)
  if (func_bye is not None):
    func_bye(fromaddr, msg["tcp_port"])

  events_bye.on_change(msg=msg, fromaddr=fromaddr) # call all registered functions

  return received_msg

def bogus_bye_on_change(**kwargs):
  print "bye message received: ",
  if fromaddr in kwargs:
    print fromaddr
  else:
    print


#add a bogus procedure
events_bye.on_change += bogus_bye_on_change
