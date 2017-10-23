#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements:

* process_msg_ping(): generates a pong message in response to a received ping message

* send_msg_ping(): send a ping to another device

@note: see msg_ping.h in hostapd/src/messaging

@author: Henrique Duarte Moura
@organization: WINET/DCC/UFMG
@copyright: h3dema (c) 2017
@contact: henriquemoura@hotmail.com
@licence: GNU General Public License v2.0 (https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
@since: July 2015
@status: in development

@requires: construct 2.5.2
"""
from datetime import datetime
from construct import SLInt32, LFloat32, CString, SLInt8
from construct import Embed, Struct, Container
from construct import If
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION, BUFFER_SIZE
from pox.ethanol.ssl_message.msg_common import connect_ssl_socket
from pox.ethanol.ssl_message.msg_common import is_error_msg, tri_boolean, len_of_string

msg_ping = Struct('msg_ping',
                  Embed(msg_default),  # default fields
                  SLInt32('data_size'),
                  If(lambda ctx: ctx["data_size"] > 0, CString("data")),
                  # Probe(),
                  )
""" ping message data structure
"""

msg_pong = Struct('msg_pong',
                  Embed(msg_default),  # default fields
                  LFloat32('rtt'),  # float com 32 bits, LFloat32 (C little endian 32 bits)
                  SLInt8('verify_data'),  # class boolean
                  # Probe(),
                  )
""" pong message data structure
"""

BYTE_INICIAL = 48


def generate_ping_data(p_size=64):
    data = '';
    for i in range(p_size):
        data += chr((BYTE_INICIAL + i) % 128)  # 7-bit ASCII
    data += chr(0)
    return data;


def verify_data(data, p_size):
    """
      check if the payload received is correct
    """
    data_to_check = generate_ping_data(p_size)
    # ok = (data.find(data_to_check) == 0) and (len(data_to_check) == len(data))
    return data_to_check == data


def send_msg(server, msg):
    """ sends a message PING msg to the server
        @param server: tuple (ip, port) used to socket connect to the client
        @param msg: message to be sent (ping or pong)
    """
    ssl_sock = connect_ssl_socket(server)

    t0 = datetime.now()
    num_bytes = ssl_sock.write(msg)

    # 3) retrieve server's response
    received_msg = ssl_sock.read(BUFFER_SIZE)
    t1 = datetime.now()
    ssl_sock.close()
    if is_error_msg(received_msg):
        return None
    else:
        msg = msg_pong.parse(received_msg)
        msg.rtt = t1 - t0
        return msg


def send_msg_ping(server, id=0, num_tries=1, p_size=64):
    """ send a ping message to other ethanol device (mainly to the controller)
        and receives a pong response
        @param server: tuple (ip, port_num)
        @param id: message id
        @param num_tries: number of message retries before quitting
        @param p_size: payload size (extra size in bytes added to the message)
        @return: all messages sent
    """
    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_PING,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        data_size=p_size
    )
    msg_struct.data = generate_ping_data(p_size)

    ret = []
    for i in range(num_tries):
        msg = msg_ping.build(msg_struct)
        msg = send_msg(server, msg)
        if msg is not None:
            verify_data = tri_boolean('verify_data', msg)
            msg['verify_data'] = verify_data
            ret.append(msg)
        msg_struct.m_id = msg_struct.m_id + 1

    return ret


def process_msg_ping(received_msg, fromaddr):
    """ grabs the ping message, verifies the data field and returns a pong message
    """
    msg = msg_ping.parse(received_msg)
    msg['data'] += chr(0)  # add "\0" at the end of this field, to transform it into a C string
    # print "process_msg_ping - parse", msg

    result = Container(
        m_type=MSG_TYPE.MSG_PONG,
        m_id=msg['m_id'],
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        rtt=0,
        verify_data=verify_data(msg['data'], msg['data_size'])
    )
    return msg_pong.build(result)
