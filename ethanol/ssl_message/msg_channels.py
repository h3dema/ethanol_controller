#!/usr/bin/python
# -*- coding: utf-8 -*-

"""implements the following messages:

* get_channels

* get_currentchannel

* set_currentchannel

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

from construct import ULInt32, SLInt32
from construct import Embed
from construct import Array, Struct, Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name, field_station
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

valid_channel = Struct('valid_channel',
                       ULInt32('frequency'),
                       ULInt32('channel'),
                       )

msg_channels = Struct('msg_channels',
                      Embed(msg_default),  # default fields
                      Embed(field_intf_name),
                      ULInt32('num_channels'),
                      Array(lambda ctx: ctx.num_channels, valid_channel),
                      # Probe()
                      )


def get_channels(server, id=0, intf_name=None):
    """ get the channels the interface inff_name supports, applies to access points
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: names of the wireless interface
      @type intf_name: list of str

      @return: msg - received message
    """
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_GET_VALIDCHANNELS,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        num_channels=0,  # don´t know how many channels are in the AP
        valid_channel=[],  # field will be filled by the AP
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_channels.build, msg_channels.parse)
    if not error:
        value = msg['valid_channel'] if 'valid_channel' in msg else []
    else:
        value = []

    # returns the value
    # -1 equals an error has occured
    return msg, value


msg_currentchannel = Struct('msg_currentchannel',
                            Embed(msg_default),  # default fields
                            Embed(field_intf_name),
                            Embed(field_station),
                            SLInt32('channel'),
                            SLInt32('frequency'),
                            ULInt32('autochannel'),
                            # Probe()
                            )


def get_currentchannel(server, id=0, intf_name=None, sta_ip=None, sta_port=0):
    """ get the channel the interface is configured to use . You can ask the AP to relay this request to the station if (sta_ip, sta_port) is provided
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
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_GET_CURRENTCHANNEL,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        channel=0,
        frequency=0,
        autochannel=0,
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_currentchannel.build, msg_currentchannel.parse)
    if not error:
        value = msg['channel'] if 'channel' in msg else -1
    else:
        value = -1
    return msg, value


def set_currentchannel(server, id=0, channel=None, intf_name=None, sta_ip=None, sta_port=0):
    """ set the current channel to channel
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
    if channel is None or not isinstance(channel, int):
        return
    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_SET_CURRENTCHANNEL,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        channel=channel,
        frequency=0,
        autochannel=0,
    )
    send_and_receive_msg(server, msg_struct, msg_currentchannel.build, msg_currentchannel.parse, only_send=True)
