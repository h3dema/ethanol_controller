#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* station_trigger_transition

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

from construct import SLInt32, CString
from construct import Embed
from construct import Struct
from construct import Container, If
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_mac_addr
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_core import field_station
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

field_mac_new_ap = Struct('mac_new_ap',
                          SLInt32('mac_new_ap_size'),
                          If(lambda ctx: ctx["mac_new_ap_size"] > 0,
                             CString("mac_new_ap")
                             ),
                          )
""" handles a mac address field for the new ap (a C char * field)
"""

msg_station_trigger_transition = Struct('msg_station_trigger_transition',
                                        Embed(msg_default),  # default fields
                                        Embed(field_station),
                                        Embed(field_mac_addr),  # mac_sta
                                        Embed(field_intf_name),  # intf_name
                                        Embed(field_mac_new_ap),  # mac_new_ap
                                        # Probe()
                                        )
""" message structure common to all supported_messages messages"""


def station_trigger_transition(server, id=0, sta_ip=None, sta_port=0,
                               sta_mac=None, intf_name=None, mac_new_ap=None):
    """ sendo command to station to change to a new ap

      @param server: tuple (ip, port_num)
      @param id: message id

    """
    msg_struct = Container(m_type=MSG_TYPE.MSG_TRIGGER_TRANSITION,
                           m_id=id,
                           p_version_length=len_of_string(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           sta_ip_size=len_of_string(sta_ip),
                           sta_ip=sta_ip,
                           sta_port=sta_port,
                           mac_addr_size=len_of_string(sta_mac),
                           mac_addr=sta_mac,
                           intf_name_size=len_of_string(intf_name),
                           intf_name=intf_name,
                           mac_new_ap_size=len_of_string(mac_new_ap),
                           mac_new_ap=mac_new_ap,
                           )
    error, msg = send_and_receive_msg(server, msg_struct, msg_station_trigger_transition.build,
                                      msg_station_trigger_transition.parse, only_send=True)
