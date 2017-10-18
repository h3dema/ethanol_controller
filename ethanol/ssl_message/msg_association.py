#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  implements:

  * the default process function used by the controller

  * process_association()

  * get_association()

  * register_functions() used in VAP

  * set_event_association()

  @todo: message MSG_ENABLE_ASSOC_MSG to enable or disable the event at the AP

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
from construct import SLInt8, SLInt32, ULInt64, CString
from construct import Embed, Struct, Container
from construct import If

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION, tri_boolean

field_mac_ap = Struct('mac_ap',
                      SLInt32('mac_ap_size'),
                      If(lambda ctx: ctx["mac_ap_size"] > 0, CString("mac_ap")),
                      )
""" handles the ap's mac address used in msg_association
"""

field_mac_sta = Struct('mac_sta',
                       SLInt32('mac_sta_size'),
                       If(lambda ctx: ctx["mac_sta_size"] > 0, CString("mac_sta")),
                       )
""" handles the station's mac address used in msg_association
"""
msg_association = Struct('msg_association',
                         Embed(msg_default),  # default fields
                         Embed(field_mac_ap),
                         Embed(field_mac_sta),
                         SLInt8('allowed'),
                         SLInt32('response'),
                         )
""" all association message types are the same, and use msg_association struct to send information
"""


def get_association(server, id=0, association_type=None, mac_sta=None, mac_ap=None):
    """ only for tests. the controller don't use this!!!
    """
    if (association_type is None) or (mac_sta is None) or (mac_ap is None):
        return None

    value = None  # error

    msg_struct = Container(m_type=association_type,
                           m_id=id,
                           p_version_length=len(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           mac_ap_size=0 if mac_ap is None else len(mac_ap),
                           mac_ap=mac_ap,
                           mac_sta_size=0 if mac_sta is None else len(mac_sta),
                           mac_sta=mac_sta,
                           allowed=True,
                           response=0,
                           )
    error, msg = send_and_receive_msg(server, msg_struct, msg_association.build, msg_association.parse)
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


def register_functions(mac, vap):
    """ use this function to register the VAP object
        process_association will call the object's methods to deal with each one of the association steps
    """
    # print "inside register_functions"
    registered_functions[mac] = vap


#
# returns the message to the ssl server process
#
def process_association(received_msg, fromaddr):
    msg = msg_association.parse(received_msg)
    mac_ap = msg['mac_ap']
    if mac_ap in registered_functions:
        m_type = msg['m_type']
        mac_sta = msg['mac_sta']
        response = 0  # default value is accepted
        if m_type == MSG_TYPE.MSG_ASSOCIATION:
            enabled = vap.evUserAssociating(mac_sta)
            response = 1 if enabled else 0
        elif m_type == MSG_TYPE.MSG_DISASSOCIATION:
            enabled = vap.evUserDisassociating(mac_sta)
            response = 1 if enabled else 0
        elif m_type == MSG_TYPE.MSG_REASSOCIATION:
            enabled = vap.evUserReassociating(mac_sta)
            response = 1 if enabled else 0
        elif m_type == MSG_TYPE.MSG_AUTHORIZATION:
            enabled = vap.evUserAuthenticating(mac_sta)
            response = 1 if enabled else 0
        elif m_type == MSG_TYPE.MSG_USER_DISCONNECTING:
            enabled = vap.evUserDisconnecting(mac_sta)
        elif m_type == MSG_TYPE.MSG_USER_CONNECTING:
            enabled = vap.evUserConnecting(mac_sta)
    else:
        # default is to return true
        enable = True
    msg['allowed'] = enabled
    msg['response'] = response
    return received_msg


EVENT_MSG_ASSOCIATION = 1 << 0
EVENT_MSG_DISASSOCIATION = 1 << 1
EVENT_MSG_REASSOCIATION = 1 << 2
EVENT_MSG_AUTHORIZATION = 1 << 3
EVENT_MSG_USER_DISCONNECTING = 1 << 4
EVENT_MSG_USER_CONNECTING = 1 << 5

msg_event_association = Struct('msg_event_association',
                               Embed(msg_default),  # default fields
                               Embed(field_mac_sta),
                               ULInt64('events_to_change'),
                               SLInt8('action'),  # True: set the events, False: unset the events
                               )


def set_event_association(server, id=0, mac_sta=None, events=[], action=True):
    if mac_sta is None or len(events) == 0:
        # nothing to do
        return

    events_to_change = sum(events)
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_ENABLE_ASSOC_MSG,
        m_id=id,
        p_version_length=len(VERSION),
        p_version=VERSION,
        m_size=0,
        mac_sta_size=0 if mac_sta == None else len(mac_sta),
        mac_sta=mac_sta,
        events_to_change=events_to_change,
        action=action,
    )
    error, msg = send_and_receive_msg(server, msg_struct,
                                      msg_event_association.build,
                                      msg_event_association.parse,
                                      only_send=True)
