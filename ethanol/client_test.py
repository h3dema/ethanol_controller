#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    For TESTING purpose only.
    Don't use it as a template to your code.
    This module uses construct (https://pypi.python.org/pypi/construct)
    See more info at msg_core.py on how to install it.

    We use this module to test ethanol messages. It does not use Ethanol architecture, only its messages.
    We must import the correct message module, and place its call in launch()

    This is a pox module. It should by called using pox.py.

    Command sample:

    cd pox
    ./pox.py ethanol.client_test --server_address='thunder' --server_port=22223


'''
from threading import Thread

from pox.core import core

from pox.ethanol.ssl_message.msg_log import log


def msg_acs(connect, intf_name='wlan0', num_acs_tests=1):
    """this is a test function. it runs num_acs_tests times on interface wlan0"""
    msg, num_chan, acs = get_acs(server=connect, id=0, intf_name=intf_name, num_tests=num_acs_tests)

    print 'num_channnels = ', num_chan
    if len(acs.keys()) == 0:
        print 'no ACS'
    else:
        print 'ACS'
        for k in sorted(acs.keys()):
            print 'channnel = ', k, ' factor = ', acs[k]


'''
    =================================================================================
    procedimento principal do servidor
    =================================================================================
'''


def launch(server_address='0.0.0.0', server_port='22223',
           num_acs_tests=1,
           intf_name='wlan0',
           mac_sta='0c:84:dc:d4:7a:73'):
    """ launch is a default method used by pox to load and run this module """
    if server_address == '0.0.0.0':
        return

    server_port = int(server_port)

    """
      registra a classe que trata as conexões dos Aps
      (server_address, server_port) tuple with the AP's ip address and TCP port
    """
    log.info("Running message(s)")

    '''
      send a message
    '''

    if True:
        server = (server_address, server_port)
        # MSG_HELLO
        # from pox.ethanol.ssl_message.msg_hello import send_msg_hello
        # print "sending msg_hello"
        # print send_msg_hello(server=server)

        # MSG_HELLO
        # from pox.ethanol.ssl_message.msg_ping import send_msg_ping
        # from random import randint
        # num_tries=randint(1,10)+1
        # print "sending msg_ping - num_tries=",num_tries
        # print send_msg_ping(server=server, num_tries=num_tries)

        # MSG_GET_ACS
        # from pox.ethanol.ssl_message.msg_acs import get_acs
        # msg_acs(connect=server, intf_name = intf_name, num_acs_tests = num_acs_tests)

        # MSG_GET_TXPOWER
        # from pox.ethanol.ssl_message.msg_snr_power import get_txpower, set_txpower
        # msg, value = get_txpower(server=(server_address, server_port), intf_name = intf_name)
        # print "tx power =", value
        # value = ( value + 1 ) % 20
        # #MSG_SET_TXPOWER
        # print "setting tx power to",value
        # set_txpower(server=server, intf_name=intf_name, txpower=value)
        # #MSG_GET_TXPOWER
        # msg, value = get_txpower(server=(server_address, server_port), intf_name = intf_name)
        # print "tx power =", value

        # MSG_GET_SNR
        # from pox.ethanol.ssl_message.msg_snr_power import get_snr
        # msg, value = get_snr(server=server, intf_name = intf_name)
        # print "SNR =", value


        # MSG_GET_AP_SSID
        # from pox.ethanol.ssl_message.msg_ap_ssid import get_ap_ssids
        # msg, value = get_ap_ssids(server=server, intf_names = [intf_name])
        # print value


        # MSG_GET_MEMORY
        # from pox.ethanol.ssl_message.msg_memcpu import get_memory_usage
        # msg, value = get_memory_usage(server=server)
        # print "memory", value

        # MSG_GET_CPU
        # from pox.ethanol.ssl_message.msg_memcpu import get_cpu_usage
        # msg, value =  get_cpu_usage(server=server)
        # print "cpu", value

        # MSG_WLAN_INFO
        # from pox.ethanol.ssl_message.msg_wlan_info import req_wlan_info
        # msg, info = req_wlan_info(server=server, intf_name_list = [intf_name])
        # print info

        # MSG_GET_AP_IN_RANGE_TYPE
        # from pox.ethanol.ssl_message.msg_ap_in_range import get_ap_in_range
        # msg, num_aps, aps = get_ap_in_range(server=server, intf_name = intf_name)
        # print aps

        # MSG_GET_RADIO_WLANS
        # from pox.ethanol.ssl_message.msg_radio_wlans import get_radio_wlans
        # msg, wlans = get_radio_wlans(server=server, intf_name = intf_name)
        # print wlans

        # MSG_GET_STATISTICS
        # from pox.ethanol.ssl_message.msg_statistics import send_msg_get_statistics
        # msg, stats = send_msg_get_statistics(server=server, intf_name = intf_name)
        # print stats

        # MSG_GET_STA_STATISTICS

        # MSG_GET_CURRENTCHANNEL
        from pox.ethanol.ssl_message.msg_channels import get_currentchannel, set_currentchannel
        msg, value = get_currentchannel(server=server, intf_name=intf_name)
        print "current chan = ", value
        value = (value + 1) % 11 + 1
        # #MSG_SET_CURRENTCHANNEL
        print "setting new channel to ", value
        set_currentchannel(server=server, intf_name=intf_name, channel=value)
        msg, value = get_currentchannel(server=server, intf_name=intf_name)
        print "current chan = ", value

        # MSG_GET_TX_BITRATE
        # from pox.ethanol.ssl_message.msg_bitrates import get_tx_bitrate
        # msg, value = get_tx_bitrate(server=server,
        #                            intf_name = intf_name,
        #                            sta_mac=mac_sta)
        # print value

        # MSG_GET_TX_BITRATES
        # from pox.ethanol.ssl_message.msg_bitrates import get_tx_bitrates
        # msg, value = get_tx_bitrates(server=server, intf_name = intf_name)
        # print value

        # MSG_GET_CHANNELINFO
        # from pox.ethanol.ssl_message.msg_channelinfo import get_channelinfo
        # msg, value = get_channelinfo(server=server, intf_name = intf_name)
        # print value
        # msg, value = get_channelinfo(server=server, intf_name = intf_name, only_channel_in_use=True)
        # print "MSG_GET_CHANNELINFO\n",value


        import time
        time.sleep(1)

        if True:
            # quit
            import sys
            sys.exit(0)
