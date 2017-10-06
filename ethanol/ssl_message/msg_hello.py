#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  basic hello message. Hello carries information about the ap or station to the controller

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
from construct import LFloat32, SLInt32
from construct import Embed
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_common import is_error_msg, get_error_msg
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION, BUFFER_SIZE, SERVER_PORT
from pox.ethanol.ssl_message.msg_common import hexadecimal
from pox.ethanol.ssl_message.msg_common import connect_ssl_socket
from pox.ethanol.ssl_message.msg_log import log

from pox.ethanol.ethanol.ap import add_ap
from pox.ethanol.ethanol.station import add_station

from pox.ethanol.events import Events
events_hello = Events()
"""to handle a receiving hello message, just add your function to events_hello
   your function must use 'def my_funct(**kwargs)' signature for compatibility
   @change: we send to parameters: msg, fromaddr
"""


msg_hello = Struct('msg_hello',
                   Embed(msg_default),   # default fields
                   SLInt32('device_type'),  # 0 = controller, 1 = ap, 2 = station
                   SLInt32('tcp_port'),
                   LFloat32('rtt')       # float com 32 bits
                   )


def send_msg_hello(server, m_id=0):
    """
      @param server: tuple (ip, port_num)
      @param m_id: message id

      @return: msg - received message
    """
    ssl_sock = connect_ssl_socket(server)

    # print "send_msg_hello id:", m_id
    # 1) create message
    msg_struct = Container(m_type=MSG_TYPE.MSG_HELLO_TYPE,
                           m_id=m_id,
                           p_version_length=len(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           device_type=0,
                           tcp_port=SERVER_PORT,
                           rtt=0
                           )
    msg = msg_hello.build(msg_struct)
    # print "hello enviado para servidor > ", hexadecimal(msg)
    # 2) sending message
    t0 = datetime.now()
    log.debug(hexadecimal(msg))
    num_bytes = ssl_sock.write(msg)
    log.debug("num bytes enviados: %d" % num_bytes)

    # 3) retrieve server's response
    received_msg = ssl_sock.read(BUFFER_SIZE)
    if received_msg != '':
        t1 = datetime.now()
        # print "msg recebida > ", hexadecimal(received_msg)

        if is_error_msg(received_msg):
            msg = get_error_msg(received_msg)
        else:
            # print "msg recebida > ", hexadecimal(received_msg)
            msg = msg_hello.parse(received_msg)
            msg.rtt = t1 - t0
    else:
        msg = None
    ssl_sock.close()
    return msg


def process_hello(received_msg, fromaddr):
    """returns the message to the ssl server process
      @param received_msg:
      @param fromaddr: ip address of the device that sent this message
      @func_hello: event
    """
    msg = msg_hello.parse(received_msg)
    client_port = msg['tcp_port']
    client_socket = (fromaddr[0], client_port)

    log.debug("recebeu mensagem de Hello.")
    if msg['device_type'] == 1:
        # create ap object
        log.debug("\tConectar ao AP via %s:%d" % client_socket)
        add_ap(client_socket)  # returns ap
    elif msg['device_type'] == 2:
        log.info("Conectar a estacao via %s:%d" % client_socket)
        station = add_station(client_socket)

    events_hello.on_change(msg=msg, fromaddr=fromaddr)  # call all registered functions

    # only send back the same message
    return received_msg


def bogus_hello_on_change(**kwargs):
    print "hello message received: ",
    if 'fromaddr' in kwargs:
        print kwargs['fromaddr']
    else:
        print

#add a bogus procedure
events_hello.on_change += bogus_hello_on_change
