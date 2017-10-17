#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* get_ssid

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
from construct import Struct, Array
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_station, field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg


field_time_stamp = Struct('time_stamp',
                          SLInt32('time_stamp_size'),
                          If(lambda ctx: ctx["time_stamp_size"] > 0, CString("time_stamp")),
                          )

stats_field = Struct('stats',
                     # char * mac_addr;
                     # char * intf_name;
                     # long inactive_time'),
                     SLInt64('rx_bytes'),
                     SLInt64('tx_bytes'),
                     SLInt64('rx_packets'),
                     SLInt64('rx_duration'),
                     SLInt64('tx_packets'),
                     SLInt64('tx_retries'),
                     SLInt64('tx_failed'),
                     SLInt64('beacon_loss'),
                     SLInt64('beacon_rx'),
                     SLInt64('rx_drop_misc'),
                     SLInt32('signal'),
                     SLInt32('signal_avg'),
                     SLInt32('beacon_signal_avg'),
                     SLInt64('time_offset'),
                     SLInt64('connected_time'),
                     # float tx_bitrate;
                     )


msg_sta_statistics = Struct('msg_sta_statistics',
                            Embed(msg_default),   # default fields
                            Embed(field_intf_name),
                            Embed(field_station),
                            SLInt32('num_stats'),
                            Array(lambda ctx: ctx.num_stats, stats_field),
                            Embed(field_time_stamp),
                            # Probe()
                            )


def get_sta_statistics(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    """
      returns the value
      None equals an error has occured (or no interface found)
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
    # 1) create message
    msg_struct = Container(m_type=MSG_TYPE.MSG_GET_STA_STATISTICS,
                           m_id=id,
                           p_version_length=len(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           intf_name_size=0 if intf_name is None else len(intf_name),
                           intf_name=intf_name,
                           sta_ip_size=0 if sta_ip is None else len(sta_ip),
                           sta_ip=sta_ip,
                           sta_port=sta_port,
                           num_stats=0,
                           stats=[],
                           time_stamp_size=0,
                           time_stamp=None,
                           )
    error, msg = send_and_receive_msg(server, msg_struct, msg_sta_statistics.build, msg_sta_statistics.parse)
    if not error:
        value = msg['stats'] if 'stats' in msg else []
    else:
        value = []

    return msg, value
