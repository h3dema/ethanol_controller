# -*- coding: utf-8 -*-
"""
  defines if our modules will use pox.log facility or python log facility

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

USING_POX = False
"""if true, then pox logs our module messages"""

if USING_POX:
  from pox.core import core
  log = core.getLogger()
else:
  import logging
  log = logging
  log.basicConfig(level=log.INFO)

