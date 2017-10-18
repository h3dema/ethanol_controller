#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
implements the following messages:

* get_ap_interferenceMap

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


### ################### TODO  ###################


def get_ap_interferenceMap(server, m_id=0, intf_name=None):
    if intf_name is None:
        return None, None
