#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 error messagens

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
from construct import Struct, Embed
from construct import Container

from pox.ethanol.ssl_message.msg_common import MSG_TYPE, MSG_ERROR_TYPE
from pox.ethanol.ssl_message.msg_common import VERSION
from pox.ethanol.ssl_message.msg_core import msg_default, decode_default_fields

msg_error = Struct('msg_error',
                   Embed(msg_default),  # default fields
                   SLInt32('error_type')  # int (32 bits) - little endian --> define the type of error, default UNKNOWN
                   )


def return_error_msg_struct(m_id, error_type=MSG_ERROR_TYPE.ERROR_UNKNOWN):
    """
      return error message as an array of bytes
      @param id: message id

      @return: msg - received message
    """
    msg_struct = Container(m_type=MSG_TYPE.MSG_ERR_TYPE,
                           m_id=m_id,
                           p_version_length=len(VERSION),
                           p_version=VERSION,
                           m_size=0,
                           error_type=error_type,
                           )
    return msg_error.build(msg_struct)


def process_msg_not_implemented(received_msg, fromaddr):
    """ generates an error message for the case where the process procedure is not implemented in Python
        returns an error

        (not implemented)
    """
    msg = decode_default_fields(received_msg)
    m_id = msg['m_id']

    # only send back the same message saying that this method is not implemented
    return return_error_msg_struct(m_id, MSG_ERROR_TYPE.ERROR_PROCESS_NOT_IMPLEMENTED_FOR_THIS_MESSAGE)
