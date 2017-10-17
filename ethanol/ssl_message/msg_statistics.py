#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* send_msg_get_statistics

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

from construct import SLInt32, SLInt64, CString
from construct import Embed, If
from construct import Struct
from construct import Container
from construct.debug import Probe
from decimal import Decimal

from pox.ethanol.ssl_message.msg_core   import msg_default, decode_default_fields, field_intf_name, field_station
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg

from pox.ethanol.ethanol.ap import add_ap

field_time_stamp = Struct('time_stamp',
                          SLInt32('time_stamp_size'),
                          If(lambda ctx: ctx["time_stamp_size"] > 0,
                             CString("time_stamp")
                             ),
                          )

msg_statistics = Struct('msg_statistics',
                        Embed(msg_default),   # default fields
                        Embed(field_intf_name),
                        Embed(field_station),
                        SLInt64('rx_packets'),
                        SLInt64('rx_bytes'),
                        SLInt64('rx_dropped'),
                        SLInt64('rx_errors'),
                        SLInt64('tx_packets'),
                        SLInt64('tx_bytes'),
                        SLInt64('tx_dropped'),
                        SLInt64('tx_errors'),
                        Embed(field_time_stamp),
                        #Probe()
                        )
""" message structure common to all supported statistics messages"""

""" this module deals with multiple message types. these types are listed in supported_messages
"""

def send_msg_get_statistics(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    """ INTERNAL FUNCTION

      returns the statistics using a dict() with 9 fields

      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: names of the wireless interface
      @type intf_name: list of str
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    if intf_name==None:
        return None, -1, -1, -1, -1, -1, None

    #1) create message
    msg_struct = Container(
        m_type = MSG_TYPE.MSG_GET_STATISTICS,
        m_id = id,
        p_version_length=len(VERSION),
        p_version = VERSION,
        m_size = 0,
        intf_name_size = 0 if intf_name == None else len(intf_name),
        intf_name = intf_name,
        sta_ip_size = 0 if sta_ip == None else len(sta_ip),
        sta_ip = sta_ip,
        sta_port = sta_port,
        rx_packets = 0,
        rx_bytes = 0,
        rx_dropped = 0,
        rx_errors = 0,
        tx_packets = 0,
        tx_bytes = 0,
        tx_dropped = 0,
        tx_errors = 0,
        time_stamp_size = 0,
        time_stamp = None,
    )


    error, msg = send_and_receive_msg(server, msg_struct, msg_statistics.build, msg_statistics.parse)
    #print msg
    if not error:
        rx_packets = msg['rx_packets'] if 'rx_packets' in msg else -1
        rx_bytes = msg['rx_bytes'] if 'rx_bytes' in msg else -1
        rx_dropped = msg['rx_dropped'] if 'rx_dropped' in msg else -1
        rx_errors = msg['rx_errors'] if 'rx_errors' in msg else -1
        tx_packets = msg['tx_packets'] if 'tx_packets' in msg else -1
        tx_bytes = msg['tx_bytes'] if 'tx_bytes' in msg else -1
        tx_dropped = msg['tx_dropped'] if 'tx_dropped' in msg else -1
        tx_errors = msg['tx_errors'] if 'tx_errors' in msg else -1
        time_stamp = msg['time_stamp'] if 'time_stamp' in msg else None
    else:
        rx_packets = -1
        rx_bytes = -1
        rx_dropped = -1
        rx_errors = -1
        tx_packets = -1
        tx_bytes = -1
        tx_dropped = -1
        tx_errors = -1
        time_stamp = None

    return msg, { 'rx_packets' : rx_packets,
                  'rx_bytes'   : rx_bytes,
                  'rx_dropped' : rx_dropped,
                  'rx_errors'  : rx_errors,
                  'tx_packets' : tx_packets,
                  'tx_bytes'   : tx_bytes,
                  'tx_dropped' : tx_dropped,
                  'tx_errors'  : tx_errors,
                  'time_stamp' : time_stamp, }



