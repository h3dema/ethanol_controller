#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* changed_ap

* process_changed_ap

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
from construct import Embed, If
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

field_current_ap = Struct('current_ap',
                          SLInt32('current_ap_size'),
                          If(lambda ctx: ctx["current_ap_size"] > 0, CString("current_ap")),
                          )

msg_changed_ap = Struct('msg_changed_ap',
                        Embed(msg_default),  # default fields
                        Embed(field_intf_name),
                        Embed(field_current_ap),
                        SLInt32('status'),
                        # Probe()
                        )


def changed_ap(server, id=0, status=0, current_ap=None, intf_name=None):
    """ verify is the interface is broadcasting the SSID
      @param server: tuple (ip, port_num)
      @param id: message id
      @param intf_name: names of the wireless interface
      @type intf_name: list of str
      @param status: inform the status of the operation (result from change ap operation)
      @type status: int
      @param current_ap: MAC address of the ap
      @type current_ap: str
    """
    if (intf_name is None) or (current_ap is None):
        return

    # 1) create message
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_CHANGED_AP,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        current_ap_size=len_of_string(current_ap),
        current_ap=current_ap,
        status=status,
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_changed_ap.build, msg_changed_ap.parse, only_send=True)


def process_hello(received_msg, fromaddr):
    """
      for now, only logs the information
      @param received_msg: stream of bytes to be decoded
      @param fromaddr: IP address from the device that sent this message
    """
    msg = msg_changed_ap.parse(received_msg)
    print "Changed AP: status: %d - current ap: %s - interface: %s " % \
          (msg["status"], msg["current_ap"], msg["intf_name"])
