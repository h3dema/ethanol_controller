#!/usr/bin/python
# -*- coding: utf-8 -*-

""" implements the following messages:

* msg_tos_cleanall

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

from construct import SLInt32
from construct import CString
from construct import Embed
from construct import If
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg


msg_tos_cleanall = Struct('msg_tos_cleanall',
                          Embed(msg_default),   # default fields
                          # Probe(),
                          )
""" message to clear mange rules """


def msg_tos_cleanall(server, id=0):
    """ msg_tos_cleanall uptime

      @param server: tuple (ip, port_num)
      @param id: message id

      @return: nothing
    """
    msg_struct = Container(m_type=MSG_TYPE.MSG_TOS_CLEANALL,
                           m_id=id,
                           p_version_length=len(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           )
    send_and_receive_msg(server, msg_struct, msg_tos_cleanall.build, msg_tos_cleanall.parse, only_send=True)


msg_tos = Struct('msg_tos',
                 Embed(msg_default),   # default fields
                 SLInt32('rule_id'),
                 Embed(field_intf_name),
                 SLInt32('proto_size'),
                 If(lambda ctx: ctx["proto_size"] > 0, CString("proto")),
                 SLInt32('sip_size'),
                 If(lambda ctx: ctx["sip_size"] > 0, CString("sip")),
                 SLInt32('sport_size'),
                 If(lambda ctx: ctx["sport_size"] > 0, CString("sport")),
                 SLInt32('dip_size'),
                 If(lambda ctx: ctx["dip_size"] > 0, CString("dip")),
                 SLInt32('dport_size'),
                 If(lambda ctx: ctx["dport_size"] > 0, CString("dport")),
                 SLInt32('wmm_class'),
                 # Probe(),
                 )
""" message to add or replace mange rules """


def __msg_tos(server, m_type, msg_id=0, rule_id=-1, intf_name=None,
              proto=None, sip=None, sport=None, dip=None, dport=None, wmm_class=0):
    """ internal use only
    """
    if (rule_id < 1 and rule_id != -1) or (intf_name is None) or \
            (proto is None) or (wmm_class not in range(8)) or \
            (m_type not in [MSG_TYPE.MSG_TOS_ADD, MSG_TYPE.MSG_TOS_REPLACE]):
        return

    msg_struct = Container(m_type=m_type,
                           m_id=msg_id,
                           p_version_length=len(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           rule_id=rule_id,
                           intf_name_size=len(intf_name),
                           intf_name=intf_name,
                           proto_size=len(proto),
                           proto=proto,
                           sip_size=len(sip),
                           sip=sip,
                           sport_size=len(sport),
                           sport=sport,
                           dip_size=len(dip),
                           dip=dip,
                           dport_size=len(dport),
                           dport=dport,
                           wmm_class=wmm_class,
                           )
    send_and_receive_msg(server, msg_struct, msg_tos.build, msg_tos.parse, only_send=True)


def msg_tos_add(server, msg_id=0, intf_name=None, proto=None, sip=None, sport=None, dip=None, dport=None, wmm_class=0):
    """ add TOS rule

      @param server: tuple (ip, port_num)
      @param msg_id: message id

      @return: nothing
    """
    __msg_tos(server, m_type=MSG_TYPE.MSG_TOS_ADD, msg_id=msg_id, rule_id=-1,
              intf_name=intf_name, proto=proto,
              sip=sip, sport=sport, dip=dip, dport=dport,
              wmm_class=wmm_class)


def msg_tos_replace(server, msg_id=0, rule_id=-1, intf_name=None, proto=None, sip=None, sport=None, dip=None, dport=None, wmm_class=0):
    """ msg_tos_cleanall uptime

      @param server: tuple (ip, port_num)
      @param id: message id

      @return: nothing
    """
    __msg_tos(server, m_type=MSG_TYPE.MSG_TOS_REPLACE, msg_id=msg_id, rule_id=-1,
              intf_name=intf_name, proto=proto,
              sip=sip, sport=sport, dip=dip, dport=dport,
              wmm_class=wmm_class)
