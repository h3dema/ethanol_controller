#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module is a template that is being provided as a guideline for creating Ethanol based controllers.
    This Python code is a POX module and should be loaded on the command line along with 
    the Ethanol server as shown in the line below.

    To run this module:
    1) link this diretory inside pox directory
    ln -s ~/ethanol/ethanol_controller/template ~/ethanol/ethanol_controller/pox/pox/template

    2) start the module with ethanol
    cd ~/ethanol/ethanol_controller/pox
    python pox.py ethanol.server template.sampleApp --ap_ip="<your AP's ip address here>"

   SampleApp checks if ethanol is running,
   if ethanol is running, this module can also run
   It print a list of AP's already connected to the controller.
"""

import sys
import os
import core

log = core.getLogger()

"""this is the path of this python file"""
__my_path = os.path.dirname(os.path.realpath(__file__))


def set_app_paths(paths=['']):
    """set python's system path so we can call our functions
       :param list paths contains the relative path for our functions
    """
    for path in paths:
        sys.path.append(os.path.join(__my_path, path))


def is_ethanol_loaded(module_name='pox.ethanol.server'):
    """verifies if ethanol module is loaded

    Keyword Arguments:
      module_name {str} -- name of the ethanol module (default: {'pox.ethanol.server'})

    Returns:
      [bool] -- True if the module is loaded
    """
    modules = sorted(sys.modules.keys())
    return module_name in modules


def launch(ap_ip='127.0.0.1', sleep_time=1):
    """
        this is a sample code
    """

    if is_ethanol_loaded():
        log.info("Ethanol is LOADED -- checked")
        # wait until the AP is connected

        log.info("Waiting for AP @ %s to connect" % ap_ip)
        from pox.ethanol.ethanol.ap import is_ap_with_ip_connected
        while not is_ap_with_ip_connected(ap_ip):
            # wait x seconds
            import time
            time.sleep(sleep_time)  # sleeps sleep_time seconds

        # get and print the list of APs
        from ethanol.ethanol.ap import connected_aps
        list_of_aps = connected_aps()
        for ap in list_of_aps:
            print ap

    else:
        print "Ethanol is NOT LOADEAD -- exiting"


set_app_paths()
