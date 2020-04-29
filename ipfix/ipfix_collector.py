# coding=utf-8
# Date ：2020/3/11 15:05
__author__ = 'Maojun'

import time
import datetime
import socket
import threading
import struct
import sys
import socket
import collections
import logging
import logging.handlers
from struct import *
import xml.etree.ElementTree as ET
import platform

if sys.version_info < (3, 0):
    print("plase upgrade python to 3.0")
else:
    pass


def read_ipfix(ie_type):
    tree = ET.ElementTree(file='export.xml')

    for elem in tree.iter():
        for el, value in elem.attrib.items():
            if 'ie_type={}'.format(ie_type) == '{}={}'.format(el, value):
                print("ie-type: {}, E7-parameter: {}".format(ie_type, elem.tag))
                return elem.tag


# Logging level ###
# Set the logging level per https://docs.python.org/2/howto/logging.html
try:
    log_level  # Check if log level was passed in from command arguments
except NameError:
    log_level = "WARNING"  # Use default logging level

logging.basicConfig(level=str(log_level))  # Set the logging level
logging.critical('Log level set to ' + str(log_level) + " - OK")  # Show the logging level for debug

# IPFIX port ###
try:
    ipfix_port
except NameError:  # Not specified, use default
    ipfix_port = 4739

lock = threading.Lock()


# IPFIX Data
def ipfix_data(conn, source_ip, port):
    template_list = {}  # Cache the IPFIX templates, in orderedDict to decode the data flows

    while conn:  # Continually collect packets
        try:
            flow_packet_contents, sensor_address = conn.recvfrom(65535)  # Listen for packets inbound
            if len(flow_packet_contents) > 0:
                print('sean_collector_get:', flow_packet_contents, sensor_address)
                if debug:
                    print("flow_total_len: ", len(flow_packet_contents))
                print("AXOS_IP: ", source_ip, port)

                # Unpack the flow packet header
                try:
                    packet_attributes = {}  # Flow header attributes cache

                    (
                        packet_attributes["netflow_version"],
                        packet_attributes["ipfix_flow_bytes"],
                        packet_attributes["export_time"],
                        packet_attributes["sequence_number"],
                        packet_attributes["observation_id"]
                    ) = struct.unpack('!HHLLL', flow_packet_contents[0:16])  # Unpack header

                    packet_attributes["sensor"] = sensor_address  # For debug purposes

                    if debug:
                        logging.warning("Unpacking header[0:16]: " + str(packet_attributes))

                # Error unpacking the header
                except Exception as flow_header_error:
                    logging.warning("Failed unpacking flow header from " + str(sensor_address) + " - FAIL")
                    logging.warning(flow_header_error)
                    continue

                # Check IPFIX version ###
                if int(packet_attributes["netflow_version"]) != 10:
                    logging.warning("Received a non-IPFIX packet from " + str(sensor_address) + " - DROPPING")
                    continue

                byte_position = 16  # Position after the standard protocol header

                # Iterate through total flows in the packet ###
                # Can be any combination of templates and data flows, any lengths
                """modify by Maojun Wang"""
                try:
                    # Unpack the flow set ID and the length ###
                    # Determine if it's a template set or a data set and the size
                    # noinspection PyBroadException     #change by Maojun
                    try:
                        logging.info("Unpacking ID and length at byte position " + str(byte_position))
                        (flow_set_id, flow_set_length) = \
                            struct.unpack('!HH', flow_packet_contents[byte_position:byte_position + 4])
                        logging.info("Flow_SET_ID, Length[16:20] " + str((flow_set_id, flow_set_length)))
                    except Exception as id_unpack_error:
                        logging.info("Out of bytes to unpack, breaking")
                        break  # Done with the packet

                    # Advance past the initial header of ID and length
                    byte_position += 4

                    # IPFIX template set (ID 2)
                    if flow_set_id == 2:
                        template_position = byte_position
                        # final_template_position = (byte_position + len(flow_packet_contents) - 4)
                        final_template_position = (len(flow_packet_contents) - 28)
                        if debug:
                            print("final_template_position: ", final_template_position)

                        # Cache for the following templates
                        template_cache = {}

                        while template_position < final_template_position:
                            if debug:
                                print("template_position: ", template_position)
                                print("final_template_position: ", final_template_position)

                            logging.info("Unpacking template set at " + str(template_position))
                            (template_id, template_id_length) = \
                                struct.unpack('!HH', flow_packet_contents[template_position:template_position + 4])
                            logging.info(
                                "Found (TEMPLATE_ID, TMP_counters) --[20:24]: " + str((template_id, template_id_length))
                            )
                            template_position += 4  # Advance

                            # Template for flow data set
                            if template_id > 255:

                                # Produce unique hash to identify unique template ID and sensor
                                hashed_id = hash(str(sensor_address) + str(template_id))
                                if debug:
                                    print("template_sensor_address", str(sensor_address))
                                    pass

                                # Cache to upload to template store
                                template_cache[hashed_id] = {}
                                template_cache[hashed_id]["Sensor"] = str(sensor_address)
                                template_cache[hashed_id]["Template ID"] = template_id
                                template_cache[hashed_id]["counters"] = template_id_length
                                template_cache[hashed_id]["%s" % source_ip] = collections.OrderedDict()  # ORDER MATTERS

                                # Iterate through template lines
                                for _ in range(0, template_id_length):
                                    # Unpack template element number and length
                                    '''change by Maojun Wang'''
                                    (template_element, template_element_length) = \
                                        struct.unpack('!HH',
                                                      flow_packet_contents[template_position: template_position + 4])
                                    # HEX to DEC
                                    ie_type = template_element & 0x7fff

                                    # Cache each Element and its Length
                                    template_cache[hashed_id]["%s" % source_ip][
                                        template_element & 0x7fff] = template_element_length

                                    # Advance
                                    template_position += 4
                                    (aa, vendor) = \
                                        struct.unpack('!HH',
                                                      flow_packet_contents[template_position: template_position + 4])

                                    template_position += 4

                            # print("template_cache: ", template_cache)
                            template_list.update(template_cache)  # Add template to the template cache, list_dict
                            logging.debug(str(template_list))
                            logging.info("Template[25-28] " + str(template_id) + " parsed successfully")

                        print("template_cache: ", template_cache)
                        logging.info("Finished parsing templates at byte " + str(template_position) + " of " + str(
                            final_template_position))
                        logging.info('\n\n')

                        byte_position = (flow_set_length + byte_position) - 4  # Advance to the end of the flow
                        if debug:
                            print("byte_position: ", byte_position)

                    # IPFIX options template set (ID 3)
                    elif flow_set_id == 3:
                        logging.info("Unpacking Options Template set at " + str(byte_position))
                        logging.warning("Received IPFIX Options Template, not currently supported - SKIPPING")
                        byte_position = (flow_set_length + byte_position) - 4
                        logging.info("Finished Options Template set at " + str(byte_position))
                        break  # Code to parse the Options Template will go here eventually

                    # Received an IPFIX flow data set, corresponding with a template
                    elif flow_set_id > 255:
                        print("template_list: ", template_list)

                        # Compute the template hash ID
                        hashed_id = hash(str(sensor_address) + str(flow_set_id))

                        # Check if there is a template
                        if hashed_id in template_list.keys():

                            logging.info("Parsing data flow " + str(flow_set_id) + " at byte " + str(byte_position))
                            now = datetime.datetime.now()  # Get the current UTC time for the flows
                            data_position = byte_position  # Temporary counter
                            print("data_position, flow_set_length: ", data_position, flow_set_length)

                            # Iterate through flow bytes until we run out
                            while data_position + 4 <= (flow_set_length + (byte_position - 4)):

                                logging.info("Parsing flow " + str(flow_set_id) + " at " + str(data_position)
                                             + ", sequence " + str(packet_attributes["sequence_number"]))

                                # Cache the flow data, to be appended to flow_dic[]
                                flow_index = {
                                    "_index": str("flow-" + now.strftime("%Y-%m-%d")),
                                    "_type": "Flow",
                                    "_source": {
                                        "Flow Type": "IPFIX",
                                        "Sensor": sensor_address,
                                        "Sequence": packet_attributes["sequence_number"],
                                        "Observation Domain": str(packet_attributes["observation_id"]),
                                        "Time": now.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (
                                                now.microsecond / 1000) + "Z",
                                    }
                                }

                                parameter = []
                                # Iterate through template elements
                                for template_key, field_size in template_list[hashed_id]["%s" % source_ip].items():

                                    # from .xml_read import read_ipfix
                                    # print(tem)
                                    ie_name = read_ipfix(str(template_key))

                                    if field_size == 65535:
                                        # Unpack the string
                                        (flow_len,) = struct.unpack('!s',
                                                                    flow_packet_contents[
                                                                    data_position:data_position + 1])
                                        # bytes convert to int
                                        f_len = int.from_bytes(flow_len, byteorder='big', signed=False)
                                        data_position += 1
                                        (flow_payload,) = \
                                            struct.unpack('!%ss' % f_len,
                                                          flow_packet_contents[data_position:data_position + f_len])
                                        # bytes convert to string
                                        parameter.append("{}: {}".format(ie_name, flow_payload))
                                        data_position += f_len

                                    elif field_size == 17:
                                        print("field is int with DEC need convert to ASCII", data_position)
                                        (flow_payload_2) = \
                                            struct.unpack('!%sb' % field_size,
                                                          flow_packet_contents[
                                                          data_position:data_position + field_size])
                                        ma = "".join(chr(fl) for fl in flow_payload_2)
                                        parameter.append(("{}: {}".format(ie_name, ma)))
                                        data_position += field_size

                                    elif field_size < 17:
                                        # https://www.cnblogs.com/volcao/p/8807507.html
                                        unpack_re = ''
                                        if field_size == 1:
                                            unpack_re = '!B'
                                        elif field_size == 2:
                                            unpack_re = '!h'
                                        elif field_size == 4:
                                            unpack_re = '!L'
                                        elif field_size == 8:
                                            unpack_re = '!Q'
                                        (flow_payload_2) = \
                                            struct.unpack(unpack_re,
                                                          flow_packet_contents[
                                                          data_position:data_position + field_size])
                                        mm = "".join(str(int_value) for int_value in flow_payload_2)
                                        if field_size == 4 and int(mm) > 999999999:
                                            tt = datetime.datetime.fromtimestamp(int(mm))
                                            mm = str(tt)
                                        if type(mm) is tuple:
                                            parameter.append(("{}: {}".format(ie_name, str(int(mm)))))
                                        elif type(mm) is str:
                                            parameter.append("{}: {}".format(ie_name, mm))
                                        else:
                                            print("mm type not found")
                                        data_position += field_size

                                    # Something we haven't accounted for yet
                                    else:
                                        pass

                                print("\n\n{}_temp_{}_at: {}".format(source_ip, flow_set_id, now))
                                for para in parameter:
                                    print(para)
                                print("\n\n")

                        # No template, drop the flow per the standard and advanced the byte position
                        else:
                            byte_position += flow_set_length
                            logging.warning(
                                "Waiting on template " + str(flow_set_id) + " from " + str(sensor_address)
                                + ", sequence " + str(packet_attributes["sequence_number"]) + " - DROPPING"
                            )

                        byte_position = (flow_set_length + byte_position) - 4  # Advance to the end of the flow
                        if debug:
                            logging.warning("Ending data set at temp: {}".format(flow_set_id))

                    # Received a flow set ID we haven't accounted for
                    else:
                        logging.warning("Unknown flow ID " + str(flow_set_id) + " from " + str(sensor_address))
                        break  # Bail out

                except Exception as error:
                    print(error, "data error and modify by Maojun")

            elif len(flow_packet_contents) == 0:
                logging.warning("break out threading")
                break  # this will help break out threading, or threading will increase, memory will increase
            else:
                pass

            if debug:
                print("back to receive data")

        except Exception as error:
            print(error, "data error and modify by Maojun")

        if debug:
            print("connection still in")

    logging.warning("finished socket connection {}".format(source_ip))


if __name__ == "__main__":
    '''change by Maojun Wang'''
    localip = socket.gethostbyname(socket.gethostname())
    debug = False

    if platform.system() == 'Linux':
        from netifaces import interfaces, ifaddresses, AF_INET
        iplist = []
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
            if debug:
                print(addresses)
            iplist.append(addresses)
        if debug:
            print(iplist[1][0])

    try:
        netflow_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

        if platform.system() == 'Windows':
            netflow_sock.bind((localip, ipfix_port))
        elif platform.system() == 'Linux':
            """netstat -anp |grep 4739      check port status
            fuser -v -n tcp 4739    check port process ID"""
            netflow_sock.bind((iplist[1][0], ipfix_port))
            localip = iplist[1][0]
        logging.warning("Bound to port {} : {}".format(localip, ipfix_port))
        netflow_sock.listen(50)

        while netflow_sock:
            time.sleep(0.1)
            sock, addr = netflow_sock.accept()
            print("E7_ip: ", addr[0], addr[1])
            loop = range(1)
            tt = []

            for i in loop:
                t = threading.Thread(target=ipfix_data, args=(sock, addr[0], addr[1]))
                tt.append(t)
            if debug:
                print("threading: ", threading.enumerate())

            for i in loop:
                if debug:
                    print("threading start")
                tt[i].start()

            for i in loop:
                """SOCKET only can get one data, the socket will handle if using join."""
                pass
                # print("threading join")
                # tt[i].join()  #
            if debug:
                print("threading_active: ", threading.active_count())

    except ValueError as socket_error:
        logging.critical("Could not open or bind a socket on port " + str(ipfix_port))
        logging.critical(str(socket_error))
        sys.exit()

"""struct list
Format	C Type	Python type	Standard size	Notes
    x	pad byte	no value	 	 
    c	char	string of length     1	1	 
    b	signed char	integer	    1	(3)
    B	unsigned char	integer 	1	(3)
    ?	_Bool	bool	1	(1)
    h	short	integer	    2	(3)
    H	unsigned short	integer	    2	(3)
    i	int	    integer	    4	(3)
    I	unsigned int	integer	    4	(3)
    l	long	integer	    4	(3)
    L	unsigned long	integer 	4	(3)
    q	long long	integer	    8	(2), (3)
    Q	unsigned long long	integer 	8	(2), (3)
    f	float	float	4	(4)
    d	double	float	8	(4)
    s	char[]	string	1	 
    p	char[]	string	 	 
    P	void *	integer	 	(5), (3)
    
    
IPFIX Type	Python Type
octetArray	bytes
unsigned8	int
unsigned16	int
unsigned32	int
unsigned64	int
signed8	    int
signed16	int
signed32	int
signed64	int
float32	    float
float64	    float
boolean	    bool
macAddress	bytes
string	    str
dateTimeSeconds	    datetime
dateTimeMilliseconds	    datetime
dateTimeMicroseconds	    datetime
dateTimeNanoseconds	    datetime
ipv4Address	    ipaddress
ipv6Address	    ipaddress"""
