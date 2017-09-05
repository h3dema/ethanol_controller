#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
All ssl_modules use python construct (https://pypi.python.org/pypi/construct).
To install this module:

wget -c https://pypi.python.org/packages/source/c/construct/construct-2.5.2.tar.gz
tar zxvf construct-2.5.2.tar.gz
cd construct-2.5.2
sudo ./setup.py install

@see: documentation at http://construct.readthedocs.io/en/latest/

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
from construct import Struct
from construct import If

from construct.lib.py3compat import int2byte
from construct.macros import SymmetricMapping
from construct.debug import Probe
from construct import Field
from struct import pack, unpack


def toHex(s):
    """
      @param s: is a number stored in an string
      @return: a string, each byte of s is coded as a two char hex string
    """
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)

    return reduce(lambda x,y:x+y, lst)

def int32_to_bytes(i, endian='l'):
    """
      helper function to BooleanFlag()
      returns boolean value coded as string of 4 bytes
      default is little endian
    """
    v = unpack("4b", pack("I", i))
    if endian == 'b':
      return chr(v[3])+chr(v[2])+chr(v[1])+chr(v[0])
    else:
      return chr(v[0])+chr(v[1])+chr(v[2])+chr(v[3])

def BooleanFlag(name, truth_value = 1, false_value = 0, default = False):
    """
      Defines a Construct boolean type. The flag is coded as a 32 bit value
    """
    """
    A boolean field coded as integer.

    Flags are usually used to signify a Boolean value, and this construct
    maps values onto the ``bool`` type.

    .. note:: This construct works with both bit and byte contexts.

    .. warning:: Flags default to False, not True. This is different from the
        C and Python way of thinking about truth, and may be subject to change
        in the future.

    :param name: field name
    :param truth: value of truth (default 1)
    :param falsehood: value of falsehood (default 0)
    :param default: default value (default False)
    """
    return SymmetricMapping(Field(name, 4),
        #FormatField(name, "<", "l")
        {True : int32_to_bytes(truth_value), False : int32_to_bytes(false_value)},
        default = default,
    )

msg_default = Struct('msg_default',
                   #Probe(), # utilizado para debug
                   SLInt32('m_type'),
                   SLInt32('m_id'),
                   SLInt32('p_version_length'),
                   CString("p_version"),
                   #Probe(),
                   SLInt32('m_size'),
              )
"""
  default message structure
  to be embedded in the first part of every message
"""

field_intf_name = Struct('intf_name',
                        SLInt32('intf_name_size'),
                        If(lambda ctx: ctx["intf_name_size"] > 0,
                          CString("intf_name")
                        ),
                  )
""" handles an interface name field (a C char * field)
"""

field_mac_addr = Struct('mac_addr',
                        SLInt32('mac_addr_size'),
                        If(lambda ctx: ctx["mac_addr_size"] > 0,
                          CString("mac_addr")
                        ),
                  )
""" handles a mac address field (a C char * field)
"""

field_ssid = Struct('ssid',
                        SLInt32('ssid_size'),
                        If(lambda ctx: ctx["ssid_size"] > 0,
                          CString("ssid")
                        ),
                  )
""" handles a ssid field (a C char * field)
"""

field_station = Struct('station_connection',
                    SLInt32('sta_ip_size'),
                    If(lambda ctx: ctx["sta_ip_size"] > 0,
                      CString("sta_ip")
                    ),
                    SLInt32('sta_port'),
                )
""" handles a station IP address (a C char * field), and its port (a C int field)
"""

def decode_default_fields(received_msg):
  """ handles the default header of all ethanol's messages
  @param received_msg: byte stream to be decoded (parsed) using construct message struct
  """
  msg = msg_default.parse(received_msg)
  #print "decode_default_fields", msg
  return msg


if __name__ == "__main__":
  a = BooleanFlag('flag')
  f = a.build(True)
  print ("True : ", f)
  c = a.parse(f)
  print ("c : ", c)

  f = a.build(False)
  print ("False: ", f)
  c = a.parse(f)
  print ("c : ", c)