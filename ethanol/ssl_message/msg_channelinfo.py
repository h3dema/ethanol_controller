#!/usr/bin/python
# -*- coding: utf-8 -*-

"""implements the following messages:

* MSG_GET_CHANNELINFO: get_channelinfo

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

from construct import ULInt32, SLInt32, SLInt64, SLInt8
from construct import Embed
from construct import Array, Struct, Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, tri_boolean, len_of_string

channel_info = Struct('channel_info',
                      ULInt32('frequency'),
                      SLInt8('in_use'),  # boolean
                      SLInt64('noise'),  # long in c is coded as a unsigned 64-bit integer little endian
                      SLInt64('receive_time'),  # long long in c is coded as a unsigned 64-bit integer little endian
                      SLInt64('transmit_time'),
                      SLInt64('active_time'),
                      SLInt64('busy_time'),
                      SLInt64('channel_type'),
                      SLInt64('extension_channel_busy_time'),
                      )

msg_channelinfo = Struct('msg_channelinfo',
                         Embed(msg_default),  # default fields
                         Embed(field_intf_name),
                         SLInt32('channel'),
                         SLInt32('num_freqs'),
                         # Probe(),
                         Array(lambda ctx: ctx.num_freqs, channel_info),
                         )


def get_channelinfo(server, id=0, intf_name=None, channel=0, only_channel_in_use=False):
    """ get the channels the interface inff_name supports, this function applies to access points

      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: names of the wireless interface
      @type intf_name: list of str
      @param channel: specify a channel to scan
      @type channel: int
      @param only_channel_in_use: return only the channel in use
      @type only_channel_in_use: bool

      @return: msg - received message
       a list
    """
    if intf_name is None:
        raise ValueError("intf_name must have a valid value!")
    # 1) create message
    msg_struct = Container(m_type=MSG_TYPE.MSG_GET_CHANNELINFO,
                           m_id=id,
                           p_version_length=len_of_string(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           intf_name_size=len_of_string(intf_name),
                           intf_name=intf_name,
                           channel=channel,
                           num_freqs=0,  # don´t know how many bands are in the AP
                           channel_info=[],  # field will be filled by the AP
                           )
    error, msg = send_and_receive_msg(server, msg_struct, msg_channelinfo.build, msg_channelinfo.parse)
    # print msg
    if error:
        return msg, []

    value = msg['channel_info'] if 'channel_info' in msg else []
    if (value != []) and only_channel_in_use:
        for i in range(len(value)):
            if value[i]['in_use'] == 1:
                d = dict(value[i])
                if '__recursion_lock__' in d:
                    del d['__recursion_lock__']
                value = [d]
                break

    for c in value:
        v = tri_boolean('in_use', c)
        c['in_use'] = v

    """
      returns the value, note: {} equals an error has occured or no band found
    """
    return msg, value
