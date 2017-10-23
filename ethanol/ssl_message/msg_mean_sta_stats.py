#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* send_msg_mean_sta_statistics

* send_msg_mean_sta_statistics_interface_add

* send_msg_mean_sta_statistics_interface_remove

* send_msg_mean_sta_statistics_alpha

* send_msg_mean_sta_statistics_time

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

from construct import SLInt32, SLInt64, CString, LFloat64
from construct import Embed
from construct import Struct
from construct import Container, Array
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default, field_intf_name, field_station
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

mean_net_statistics = Struct('mean_net_statistics',
                             LFloat64('collisions'),
                             LFloat64('multicast'),
                             LFloat64('rx_bytes'),
                             LFloat64('rx_compressed'),
                             LFloat64('rx_crc_errors'),
                             LFloat64('rx_dropped'),
                             LFloat64('rx_errors'),
                             LFloat64('rx_fifo_errors'),
                             LFloat64('rx_frame_errors'),
                             LFloat64('rx_length_errors'),
                             LFloat64('rx_missed_errors'),
                             LFloat64('rx_over_errors'),
                             LFloat64('rx_packets'),
                             LFloat64('tx_aborted_errors'),
                             LFloat64('tx_bytes'),
                             LFloat64('tx_carrier_errors'),
                             LFloat64('tx_compressed'),
                             LFloat64('tx_dropped'),
                             LFloat64('tx_errors'),
                             LFloat64('tx_fifo_errors'),
                             LFloat64('tx_heartbeat_errors'),
                             LFloat64('tx_packets'),
                             LFloat64('tx_window_errors'),
                             # Probe()
                             )

msg_mean_statistics = Struct('msg_mean_statistics',
                             Embed(msg_default),  # default fields
                             Embed(field_station),
                             SLInt32('num'),
                             Array(lambda ctx: ctx.num, CString('intf')),
                             Array(lambda ctx: ctx.num, mean_net_statistics),
                             # Probe()
                             )


def send_msg_mean_sta_statistics(server, id=0, sta_ip=None, sta_port=0):
    """
      @param server: tuple (ip, port_num)
      @param id: message id
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int

      @return: msg - received message
    """
    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_MEAN_STA_STATISTICS_GET,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        num=0,
        intf=[],
        mean_net_statistics=[],
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_mean_statistics.build, msg_mean_statistics.parse)
    value = {}
    if not error:
        for i in range(msg['num']):
            intf = msg['intf'][i]
            stats = msg['mean_net_statistics'][i]
            value[intf] = stats
    return msg, value


msg_mean_sta_statistics_interface = Struct('msg_mean_sta_statistics_interface',
                                           Embed(msg_default),  # default fields
                                           Embed(field_station),
                                           Embed(field_intf_name),
                                           # Probe()
                                           )


def send_msg_mean_sta_statistics_interface_add(server, id=0, sta_ip=None, sta_port=0, intf_name=None):
    """
      @param server: tuple (ip, port_num)
      @param id: message id
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int
      @param intf_name: name of the wireless interface you want to get statistics from
      @type intf_name: str

      @return: msg - received message
    """
    if intf_name is None:
        return
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_MEAN_STA_STATISTICS_SET_INTERFACE,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
    )
    send_and_receive_msg(server, msg_struct, msg_mean_sta_statistics_interface.build,
                         msg_mean_sta_statistics_interface.parse, only_send=True)


def send_msg_mean_sta_statistics_interface_remove(server, id=0, sta_ip=None, sta_port=0, intf_name=None):
    """
      @param server: tuple (ip, port_num)
      @param id: message id
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int
      @param intf_name: name of the wireless interface you want to remove from pool
      @type intf_name: str

      @return: msg - received message
    """
    if intf_name is None:
        return
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_MEAN_STA_STATISTICS_REMOVE_INTERFACE,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
    )
    send_and_receive_msg(server, msg_struct, msg_mean_sta_statistics_interface.build,
                         msg_mean_sta_statistics_interface.parse, only_send=True)


msg_mean_sta_statistics_alpha = Struct('msg_mean_sta_statistics_alpha',
                                       Embed(msg_default),  # default fields
                                       Embed(field_station),
                                       SLInt64('alpha'),
                                       # Probe()
                                       )


def send_msg_mean_sta_statistics_alpha(server, id=0, sta_ip=None, sta_port=0, alpha=0.1):
    """
      @param server: tuple (ip, port_num)
      @param id: message id
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int
      @param alpha: alpha from EWMA
      @type alpha: float

      @return: msg - received message
    """
    if not(isinstance(alpha, float) or isinstance(alpha, int)):
        return
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_MEAN_STA_STATISTICS_SET_ALPHA,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        alpha=alpha,
    )
    send_and_receive_msg(server, msg_struct,
                         msg_mean_sta_statistics_alpha.build,
                         msg_mean_sta_statistics_alpha.parse,
                         only_send=True)


msg_mean_sta_statistics_time = Struct('msg_mean_sta_statistics_time',
                                      Embed(msg_default),  # default fields
                                      Embed(field_station),
                                      SLInt32('msec'),
                                      # Probe()
                                      )


def send_msg_mean_sta_statistics_time(server, id=0, sta_ip=None, sta_port=0, msec=100):
    """
      @param server: tuple (ip, port_num)
      @param id: message id
      @param sta_ip: ip address of the station that this message should be relayed to, if sta_ip is different from None
      @type sta_ip: str
      @param sta_port: socket port number of the station
      @type sta_port: int
      @param msec: statistics are collected during "msec" interval
      @type msec: int

      @return: msg - received message
    """
    if not isinstance(msec, int):
        return
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_MEAN_STA_STATISTICS_SET_TIME,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        msec=msec,
    )
    send_and_receive_msg(server, msg_struct,
                         msg_mean_sta_statistics_time.build,
                         msg_mean_sta_statistics_time.parse,
                         only_send=True)
