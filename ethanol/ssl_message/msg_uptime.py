#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* get_uptime

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

from construct import LFloat64
from construct import Embed
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string


msg_uptime = Struct('msg_uptime',
                    Embed(msg_default),  # default fields
                    LFloat64('uptime'),
                    LFloat64('idle'),
                    # Probe()
                    )
""" message structure common to all supported_messages messages"""


def get_uptime(server, id=0):
    """ get uptime

      @param server: tuple (ip, port_num)
      @param id: message id

      @return: msg - received message
          value (bytes or packets received or sent or lost)
    """
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_GET_UPTIME,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        uptime=0,
        idle=0,
    )

    error, msg = send_and_receive_msg(server, msg_struct, msg_uptime.build, msg_uptime.parse)
    if not error:
        uptime = msg['uptime'] if 'uptime' in msg else -1
        idle = msg['idle'] if 'idle' in msg else -1
    else:
        uptime = -1
        idle = -1

    return msg, uptime, idle
