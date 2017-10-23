""" implements:

* snr_threshold_interval_reached and process_snr_threshold

* set_snr_threshold_interval

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

from construct import SLInt32, SLInt64, CString
from construct import Embed, If
from construct import Struct
from construct import Container
# from construct.debug import Probe

from pox.ethanol.ssl_message.msg_core import msg_default
from pox.ethanol.ssl_message.msg_core import field_intf_name, field_station
from pox.ethanol.ssl_message.msg_core import field_mac_addr
from pox.ethanol.ssl_message.msg_common import MSG_TYPE, VERSION
from pox.ethanol.ssl_message.msg_common import send_and_receive_msg, len_of_string

from pox.ethanol.events import Events

events_snr_threshold_reached = Events()
"""to handle a receiving snr_threshold_reached message, just add your function to events_snr_threshold_reached
   your function must use 'def my_funct(**kwargs)' signature for compatibility
   @change: we send to parameters: msg, fromaddr, sta_mac, intf_name, mac_ap
"""

field_mac_ap = Struct('mac_ap',
                      SLInt32('mac_ap_size'),
                      If(lambda ctx: ctx["mac_ap_size"] > 0,
                         CString("mac_ap")
                         ),
                      )
""" handles a mac address field for the new ap (a C char * field)
"""

msg_snr_threshold_reached = Struct('msg_snr_threshold_reached',
                                   Embed(msg_default),  # default fields
                                   Embed(field_station),
                                   Embed(field_mac_addr),  # sta_mac
                                   Embed(field_intf_name),  # intf_name
                                   Embed(field_mac_ap),  # mac_ap
                                   SLInt64('snr'),
                                   # Probe()
                                   )
""" message structure MSG_SET_SNR_THRESHOLD_REACHED
@note: mac_ap is used to send information to the device and to receive info from the device.
When sending, it contains the current_ap (i.e, the ap that the station is connected)
In the receiving message (inside process), it contains the ap that the stations should connect (can be the same as the current_ap meaning that no chance should occur)
"""


def snr_threshold_reached(server, id=0, sta_ip=None, sta_port=0, sta_mac=None, intf_name=None, mac_ap=None, snr=None):
    """ send information to controller. this implementation will 'never' be used in its python form

      @param server: tuple (ip, port_num)
      @param id: message id

    """
    if snr is None or not(isinstance(snr, int) or isinstance(snr, float)):
        return None
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_SET_SNR_THRESHOLD_REACHED,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        mac_addr_size=len_of_string(sta_mac),
        mac_addr=sta_mac,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        mac_ap_size=len_of_string(mac_ap),
        mac_ap=mac_ap,
        snr=snr,
    )
    error, msg = send_and_receive_msg(server, msg_struct, msg_snr_threshold_reached.build,
                                      msg_snr_threshold_reached.parse)
    if not error:
        pass
    return msg


def process_snr_threshold(received_msg, fromaddr):
    msg = msg_snr_threshold_reached.parse(received_msg)
    events_snr_threshold_reached.on_change(msg=msg,
                                           fromaddr=msg['fromaddr'],
                                           sta_mac=msg['sta_mac'],
                                           intf_name=msg['intf_name'],
                                           mac_ap=msg['mac_ap'])

    # TODO: define the new ap
    new_ap = None
    msg['mac_ap'] = new_ap
    return msg_snr_threshold_reached.build(msg)


def bogus_snr_threshold_reached_on_change(**kwargs):
    print "snr_threshold_reached message received: ",
    if 'fromaddr' in kwargs:
        print kwargs['fromaddr']
    else:
        print


# add a bogus procedure
events_snr_threshold_reached.on_change += bogus_snr_threshold_reached_on_change

msg_snr_interval = Struct('msg_snr_interval',
                          Embed(msg_default),  # default fields
                          Embed(field_station),
                          Embed(field_intf_name),  # intf_name
                          SLInt64('interval'),
                          # Probe()
                          )
""" message structure MSG_SET_SNR_INTERVAL"""


def snr_threshold_interval_reached(server, id=0, sta_ip=None, sta_port=0, intf_name=None, interval=10):
    """ set the time between SNR scans in the station.

      @param server: tuple (ip, port_num)
      @param id: message id
      @param interval: interval in miliseconds
      @type interval: int
    """
    if interval <= 0:
        interval = -1  # disable
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_SET_SNR_INTERVAL,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        interval=interval,
    )
    send_and_receive_msg(server, msg_struct, msg_snr_threshold_reached.build, msg_snr_threshold_reached.parse,
                         only_send=True)


msg_snr_threshold = Struct('msg_snr_threshold',
                           Embed(msg_default),  # default fields
                           Embed(field_station),
                           Embed(field_intf_name),  # intf_name
                           SLInt64('interval'),
                           # Probe()
                           )
""" message structure MSG_SET_SNR_THRESHOLD"""


def set_snr_threshold(server, id=0, sta_ip=None, sta_port=0, intf_name=None, threshold=10):
    """ set the SNR threshold in dBm. Send message to a station.

      @param server: tuple (ip, port_num)
      @param id: message id
      @param threshold: SNR threshold in dBm

    """
    msg_struct = Container(
        m_type=MSG_TYPE.MSG_SET_SNR_THRESHOLD,
        m_id=id,
        p_version_length=len_of_string(VERSION),
        p_version=VERSION,
        m_size=0,
        sta_ip_size=len_of_string(sta_ip),
        sta_ip=sta_ip,
        sta_port=sta_port,
        intf_name_size=len_of_string(intf_name),
        intf_name=intf_name,
        threshold=threshold,
    )
    send_and_receive_msg(server, msg_struct, msg_snr_threshold.build, msg_snr_threshold.parse, only_send=True)
