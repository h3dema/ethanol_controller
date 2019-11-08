#!/usr/bin/python
# -*- coding: utf-8 -*-
"""	This is a pox module. It should be called using pox.py.

Command sample:

./pox.py ethanol.server


@requires: construct (https://pypi.python.org/pypi/construct)
@see: more info at msg_core.py
"""
from threading import Thread

from pox.ethanol.ssl_message.msg_log import log
from pox.ethanol.ssl_message.msg_server import run
# from pox.ethanol.ssl_message.msg_common import SERVER_ADDR
from pox.ethanol.ssl_message.msg_common import SERVER_PORT, SERVER_ADDR, VERSION
from pox.ethanol.ethanol.ap import add_ap_openflow

from pox.core import core
# import pox.openflow.libopenflow_01 as of


def run_server(server_address=SERVER_ADDR, server_port=SERVER_PORT):
    """ creates an Ethanol server at SERVER_PORT and activates it
    """
    server = (server_address, server_port)  # socket provided by the server
    log.info("Listening @ %s:%i" % server)
    log.info("Ethanol version %s" % VERSION)
    if run(server) == -1:
        log.info("Server error. Not receiving messages!")
    log.info("Server finished!")


class ethanol_ap_server(object):
    """ Waits for OpenFlow switches to connect and saves their information to match with Ethanol AP.
    """

    def __init__(self):
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        """ when a connection is up, inserts this openflow device in a mapping list
            if this devices sends an Ethanol Hello then we know that it has openflow and ethanol capabilities
        """
        log.debug("Connection %s" % (event.connection,))
        # registra um novo AP
        sock = event.connection.sock
        ip, port = sock.getpeername()
        add_ap_openflow(ip)

    def _handle_ConnectionDown(self, event):
        """ TODO> remove the device from the mapping ?
        """
        pass


"""
    =================================================================================
    procedimento principal do servidor
    =================================================================================
"""


def launch():
    """
      registra a classe que trata as conexões dos Aps
    """
    log.info("Registering ethanol_ap_server")
    core.registerNew(ethanol_ap_server)

    """
      ativa parte wireless do servidor ethanol
    """
    log.info("Starting server thread")
    thread = Thread(target=run_server)
    thread.daemon = True
    thread.start()
