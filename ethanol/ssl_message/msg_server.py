#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  this is creates the server, that deals with clients (aps and stations) messages
  the messages implemented are mapped in map_msg_to_procedure
  main entry to this module is: call run(server)

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
from threading import Thread
import socket
import ssl
import os
import sys

from pox.ethanol.ssl_message.msg_common import MSG_TYPE, SERVER_PORT
from pox.ethanol.ssl_message.msg_hello import process_hello
from pox.ethanol.ssl_message.msg_bye import process_bye
from pox.ethanol.ssl_message.msg_ping import process_msg_ping
from pox.ethanol.ssl_message.msg_error import return_error_msg_struct
from pox.ethanol.ssl_message.msg_core import decode_default_fields
from pox.ethanol.ssl_message.msg_error import process_msg_not_implemented
from pox.ethanol.ssl_message.msg_association import process_association
from pox.ethanol.ssl_message.msg_metric import process_metric

""" maps the message type (received in the client's message) to the function that will process it
    there aren't many, because the controller is supposed to be the active part (it requests info or sets values)
"""
map_msg_to_procedure = {MSG_TYPE.MSG_ASSOCIATION: process_association,
                        MSG_TYPE.MSG_AUTHORIZATION: process_association,
                        MSG_TYPE.MSG_BYE_TYPE: process_bye,
                        MSG_TYPE.MSG_CHANGED_AP: process_msg_not_implemented,
                        MSG_TYPE.MSG_DISASSOCIATION: process_association,
                        MSG_TYPE.MSG_GET_802_11E_ENABLED: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_ACS: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_AP_BROADCASTSSID: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_AP_CTSPROTECTION_ENABLED: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_AP_DTIMINTERVAL: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_AP_FRAMEBURSTENABLED: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_AP_GUARDINTERVAL: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_AP_IN_RANGE_TYPE: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_AP_RTSTHRESHOLD: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_AP_SSID: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_BEACON_INTERVAL: process_msg_not_implemented,
                        MSG_TYPE.MSG_SET_BEACON_INTERVAL: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_BYTESRECEIVED: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_BYTESSENT: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_CHANNELINFO: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_CPU: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_CURRENTCHANNEL: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_FASTBSSTRANSITION_COMPATIBLE: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_MEMORY: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_PACKETSLOST: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_PACKETSRECEIVED: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_PACKETSSENT: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_PREAMBLE: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_RADIO_WLANS: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_SNR: process_msg_not_implemented,
                        MSG_TYPE.MSG_GET_VALIDCHANNELS: process_msg_not_implemented,
                        MSG_TYPE.MSG_HELLO_TYPE: process_hello,
                        MSG_TYPE.MSG_PING: process_msg_ping,
                        MSG_TYPE.MSG_PONG: process_msg_not_implemented,
                        MSG_TYPE.MSG_REASSOCIATION: process_association,
                        MSG_TYPE.MSG_SET_AP_BROADCASTSSID: process_msg_not_implemented,
                        MSG_TYPE.MSG_SET_AP_CTSPROTECTION_ENABLED: process_msg_not_implemented,
                        MSG_TYPE.MSG_SET_AP_DTIMINTERVAL: process_msg_not_implemented,
                        MSG_TYPE.MSG_SET_AP_FRAMEBURSTENABLED: process_msg_not_implemented,
                        MSG_TYPE.MSG_SET_AP_GUARDINTERVAL: process_msg_not_implemented,
                        MSG_TYPE.MSG_SET_AP_RTSTHRESHOLD: process_msg_not_implemented,
                        MSG_TYPE.MSG_SET_CURRENTCHANNEL: process_msg_not_implemented,
                        MSG_TYPE.MSG_SET_PREAMBLE: process_msg_not_implemented,
                        MSG_TYPE.MSG_USER_CONNECTING: process_association,
                        MSG_TYPE.MSG_USER_DISCONNECTING: process_association,
                        MSG_TYPE.MSG_MEAN_STA_STATISTICS_GET: process_msg_not_implemented,
                        MSG_TYPE.MSG_MEAN_STA_STATISTICS_SET_INTERFACE: process_msg_not_implemented,
                        MSG_TYPE.MSG_MEAN_STA_STATISTICS_REMOVE_INTERFACE: process_msg_not_implemented,
                        MSG_TYPE.MSG_MEAN_STA_STATISTICS_SET_ALPHA: process_msg_not_implemented,
                        MSG_TYPE.MSG_MEAN_STA_STATISTICS_SET_TIME: process_msg_not_implemented,
                        MSG_TYPE.MSG_SET_METRIC: process_msg_not_implemented,
                        MSG_TYPE.MSG_METRIC_RECEIVED: process_metric,
                        }
"""all message types supported"""


def deal_with_client(connstream, fromaddr):
    """ this function is called as a Thread to manage each connection

        @param connstream:
        @param fromaddr:
    """
    # read data from client
    received_msg = connstream.read(65536)
    if len(received_msg) > 0:
        # decode message
        msg = decode_default_fields(received_msg)
        m_type = msg['m_type']
        # To print the messages received on controler
        # print "msg recebida - tipo:", m_type
        if m_type in map_msg_to_procedure:
            # switch...case to deal with each kind of message
            func = map_msg_to_procedure[msg.m_type]
            reply = func(received_msg, fromaddr)
        else:
            reply = return_error_msg_struct(msg.id)

    # reply to client, if necessary
    if reply is not None:
        # num_bytes = connstream.write(reply)
        connstream.write(reply)
        # log.debug(num_bytes)

    # finished with client
    connstream.close()


DEFAULT_CERT_PATH = os.path.dirname(os.path.abspath(__file__))
"""path to the ssl certificate used in the secure socket connections"""
SSL_CERTIFICATE = DEFAULT_CERT_PATH + '/mycert.pem'
"""path and default name of the ssl certificate"""


def run(server):
    """ to use this module only call this method, providing a tuple with (server ip address, server port)
       @param server: (ip, port) tuple
    """
    # check if certificate exists
    if not os.path.exists(SSL_CERTIFICATE):
        print "Cannot run server without the certificate: %s" % SSL_CERTIFICATE
        print "Fatal error..exiting now"
        return -1
    else:
        # socket
        bindsocket = socket.socket()
        bindsocket.bind(server)
        bindsocket.listen(5)  # specifies the maximum number of queued connections
        while True:
            try:
                newsocket, fromaddr = bindsocket.accept()
                connstream = ssl.wrap_socket(newsocket,
                                             server_side=True,
                                             certfile=SSL_CERTIFICATE,  # load certs
                                             keyfile=SSL_CERTIFICATE,
                                             ssl_version=ssl.PROTOCOL_SSLv3)  # same as ssl_server.c
                """ deal without a thread """
                # deal_with_client(connstream, fromaddr)
                """ deal with the request in a thread, so multiple connections can be served """
                t = Thread(target=deal_with_client, args=(connstream, fromaddr))
                t.start()
            except:
                error_found = sys.exc_info()[0]
                print "Error: ", str(error_found)

    return 0


if __name__ == "__main__":
    server = ('localhost', SERVER_PORT)  # SERVER_PORT
    run(server)
