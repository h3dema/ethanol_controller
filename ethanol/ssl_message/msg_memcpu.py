#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* get_memory_usage

* get_cpu_usage

no process is implemented: the controller is not supposed to respond to these message

@note: see msg_cpu.h and msg_memory.h in hostapd/src/messaging

@author: Henrique Duarte Moura
@organization: WINET/DCC/UFMG
@copyright: h3dema (c) 2017
@contact: henriquemoura@hotmail.com
@licence: GNU General Public License v2.0 (https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
@since: July 2015
@status: in development

@requires: construct 2.5.2
"""

from construct import SLInt64
from construct import Embed
from construct import Struct
from construct import Container
from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core   import msg_default, decode_default_fields, field_station
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

msg_memcpu = Struct('msg_memcpu',
                    Embed(msg_default),   # default fields
                    Embed(field_station),
                    SLInt64('value'),
                    # Probe()
                    )
"""
  format the MSG_GET_CPU and MSG_GET_MEMORY data structure to be sent by ethanol protocol
"""


def get_memcpu(server, id=0, type=None, sta_ip=None, sta_port=0):
    """ INTERNAL FUNCTION: don't call it
        @param server: tuple (ip, port_num)
        @param id: message id
        @param sta_ip: ip address of a station that this message should be relayed to
        @param sta_port: socket port of the station
    """
    value = -1

    if (type is None) or (type not in [MSG_TYPE.MSG_GET_CPU, MSG_TYPE.MSG_GET_MEMORY]):
        return None, value

    #1) create message
    msg_struct = Container(
        m_type = type,
        m_id = id,
        p_version_length=len(VERSION),
        p_version = VERSION,
        m_size = 0,
        sta_ip_size = 0 if sta_ip is None else len(sta_ip),
        sta_ip = sta_ip,
        sta_port = sta_port,
        value = 0
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_memcpu.build, msg_memcpu.parse)
    #print msg
    if not error:
        value = msg['value'] / 1000000.0 if 'value' in msg else -1
    else:
        """
          returns the value
          -1 equals an error has occured
        """
        value = -1

    return msg, value


def get_memory_usage(server, id=0, sta_ip=None, sta_port=0):
    """ requests the memory usage (in percent)
        implements MSG_GET_MEMORY
        @param server: tuple (ip, port_num)
        @param id: message id
        @param sta_ip: ip address of a station that this message should be relayed to
        @param sta_port: socket port of the station
        @return: msg, memory usage in percent
    """
    return get_memcpu(server=server, id=id, type=MSG_TYPE.MSG_GET_MEMORY, sta_ip=sta_ip, sta_port=sta_port)

def get_cpu_usage(server, id=0, sta_ip=None, sta_port=0):
    """ requests the memory usage (in percent)
        implements MSG_GET_CPU
        @param server: tuple (ip, port_num)
        @param id: message id
        @param sta_ip: ip address of a station that this message should be relayed to
        @param sta_port: socket port of the station
        @return: msg, cpu usage in percent
    """
    return get_memcpu(server=server, id=id, type=MSG_TYPE.MSG_GET_CPU, sta_ip=sta_ip, sta_port=sta_port)

