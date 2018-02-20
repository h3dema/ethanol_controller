#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  implements:

  * the default process function used by the controller

  * register_metric() used in VAP

  * set_metric()

  @todo: message MSG_METRIC_MSG to enable or disable the event at the device

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
from construct import SLInt8, SLInt32, ULInt64, LFloat32
from construct import Embed, Struct, Container

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION, tri_boolean
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string
from pox.ethanol.ssl_message.msg_core import field_mac_addr


msg_metric = Struct('msg_metric',
                    Embed(msg_default),  # default fields
                    SLInt8('enable'),    # boolean enable or disable
                    SLInt32('period'),
                    ULInt64('metric'),   # bit array, bit=0 is not considered, bit=1 apply 'enable' action
                    )
""" all metric message types are the same
"""


def set_metric(server, id=0, metric=0, enable=True, period=100):
    """ only for tests. the controller don't use this!!!
    """
    if metric == 0:
        return None
    msg_struct = Container(m_type=MSG_TYPE.MSG_SET_METRIC,
                           m_id=id,
                           p_version_length=len_of_string(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           enable=enable,
                           period=period,
                           metric=metric,
                           )
    error, msg = send_and_receive_msg(server, msg_struct, msg_metric.build, msg_metric.parse, only_send=True)
    if not error and 'allowed' in msg and 'response' in msg:
        allowed = tri_boolean('allowed', msg)
        response = msg['response']
    else:
        allowed = True
        response = 0
    return msg, allowed, response


""" keeps a list of the functions in the VAP that treat the process
    maps the AP's MAC to the VAP object
    all VAPs must implement those functions
"""
registered_functions = {}


def register_metric(mac, device):
    """ use this function to register the device object
        process_association will call the object's methods to deal with each one of the association steps
        mac is the device's mac address
    """
    # print "inside register_functions"
    registered_functions[mac] = device


msg_metric_received = Struct('msg_metric',
                             Embed(msg_default),  # default fields
                             Embed(field_mac_addr),  # mac of the device
                             ULInt64('metric'),  # index of the metric
                             LFloat32('value'),  # metric EWMA
                             )
""" all received metric message types are the same
"""


def process_metric(received_msg, fromaddr):
    """ calls the device evMetric"""
    msg = msg_metric_received.parse(received_msg)
    mac_device = msg['mac_addr']
    if mac_device in registered_functions:
        device = registered_functions[mac_device]
        value = msg['value']
        metric = msg['metric']
        device.evMetric(metric, value)
    return None
