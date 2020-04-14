# coding=utf-8
# Date ：2020/3/11 15:05
__author__ = 'Maojun'

import time
import datetime
import socket
import threading
import struct
import sys
import json
import socket
import collections
import itertools
import logging
import logging.handlers
import getopt
from struct import *

# from AXOS.milan.ipfix_collector.field_types import ipfix_fields

""""https://gitlab.com/thart/flowanalyzer/-/tree/master/Python"""

# Windows socket.inet_ntop support via win_inet_pton
try:
    import win_inet_pton
except ImportError:
    pass

from socket import inet_ntoa, inet_ntop

# from elasticsearch import Elasticsearch, helpers
# from IPy import IP

# Parsing functions
# from AXOS.milan.ipfix_collector.parser_modules import mac_address, icmp_parse, ip_parse, netflowv9_parse, int_parse, \
#     ports_and_protocols, \
#     name_lookups
#
# # Field types, ports, etc
# from AXOS.milan.ipfix_collector.field_types import ipfix_fields
# from AXOS.milan.ipfix_collector.netflow_options import *
# from AXOS.milan.ipfix_collector.protocol_numbers import *

# Get command line arguments ###
try:
    arguments = getopt.getopt(sys.argv[1:], "hl:", ["--help", "log="])

    for option_set in arguments:
        for opt, arg in option_set:

            if opt in ('-l', '--log'):  # Log level
                arg = arg.upper()  # Uppercase for matching and logging.basicConfig() format
                if arg in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
                    log_level = arg  # Use what was passed in arguments

            elif opt in ('-h', '--help'):  # Help file
                with open("./help.txt") as help_file:
                    print(help_file.read())
                sys.exit()

            else:  # No options
                pass

except Exception as argument_error:
    sys.exit("Unsupported or badly formed options, see -h for available arguments - EXITING")

# Logging level ###
# Set the logging level per https://docs.python.org/2/howto/logging.html
try:
    log_level  # Check if log level was passed in from command arguments
except NameError:
    log_level = "WARNING"  # Use default logging level

logging.basicConfig(level=str(log_level))  # Set the logging level
logging.critical('Log level set to ' + str(log_level) + " - OK")  # Show the logging level for debug

# DNS Lookups ###
# Reverse lookups
try:
    if dns is False:
        logging.warning("DNS reverse lookups disabled - DISABLED")
    elif dns is True:
        logging.warning("DNS reverse lookups enabled - OK")
    else:
        logging.warning("DNS enable option incorrectly set - DISABLING")
        dns = False
except:
    logging.warning("DNS enable option not set - DISABLING")
    dns = False

# RFC-1918 reverse lookups
try:
    if lookup_internal is False:
        logging.warning("DNS local IP reverse lookups disabled - DISABLED")
    elif lookup_internal is True:
        logging.warning("DNS local IP reverse lookups enabled - OK")
    else:
        logging.warning("DNS local IP reverse lookups incorrectly set - DISABLING")
        lookup_internal = False
except:
    logging.warning("DNS local IP reverse lookups not set - DISABLING")
    lookup_internal = False

# IPFIX port ###
try:
    ipfix_port
except NameError:  # Not specified, use default
    ipfix_port = 4739
    logging.warning("IPFIX port not set in netflow_options.py, defaulting to " + str(ipfix_port) + " - OK")


# Elasticsearch instance ###
# es = Elasticsearch([elasticsearch_host])

# IPFIX Data
def ipfix_data(conn, source_ip, port):
    flow_dic = []  # Stage the flows for the bulk API index operation
    template_list = {}  # Cache the IPFIX templates, in orderedDict to decode the data flows
    record_num = 0  # Record counter for Elasticsearch bulk upload API

    # Classes for parsing fields
    # icmp_parser = icmp_parse()  # Class for parsing ICMP Types and Codes
    # ip_parser = ip_parse()  # Class for unpacking IPv4 and IPv6 addresses
    # mac = mac_address()  # Class for parsing MAC addresses and OUIs
    # int_un = int_parse()  # Class for parsing integers
    # ports_protocols_parser = ports_and_protocols()  # Class for parsing ports and protocols
    # name_lookups = name_lookups()  # Class for DNS lookups

    while True:  # Continually collect packets
        for j in range(0, 2):
            flow_packet_contents, sensor_address = conn.recvfrom(2048)  # Listen for packets inbound
            print('sean_collector_get:', flow_packet_contents, sensor_address)
            print("flow_total_len: ", len(flow_packet_contents))
            print("E7_data_ip: ", source_ip, port)

            import ipfix.message
            # import ipfix.template
            # import ipfix.ie

            # msg = ipfix.message.MessageBuffer()
            # print(type(flow_packet_contents))
            # print('aaaa:', msg.from_bytes(flow_packet_contents))
            # for rec in msg.namedict_iterator():
            #     print('sean_ipfix_message: ', sorted(rec.items()))

            from ipfix import reader

            sean_ipfix = reader.MessageStreamReader(flow_packet_contents)
            print('sean_ipfix_reader:', sean_ipfix)

            for flow_con in str(flow_packet_contents).split('x00'):
                # print('get data from udp client: {}\r'.format(dd))
                for msg in flow_con.split('\n'):
                    print("ipfix_content: ", msg.encode("utf-8"))

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

                packet_attributes["sensor"] = sensor_address[0]  # For debug purposes
                logging.info("Unpacking header[0:16]: " + str(packet_attributes))

            # Error unpacking the header
            except Exception as flow_header_error:
                logging.warning("Failed unpacking flow header from " + str(sensor_address[0]) + " - FAIL")
                logging.warning(flow_header_error)
                continue

            # Check IPFIX version ###
            if int(packet_attributes["netflow_version"]) != 10:
                logging.warning("Received a non-IPFIX packet from " + str(sensor_address[0]) + " - DROPPING")
                continue

            byte_position = 16  # Position after the standard protocol header

            # Iterate through total flows in the packet ###
            # Can be any combination of templates and data flows, any lengths
            """modify by Maojun Wang"""
            # while True:
            try:
                # Unpack the flow set ID and the length ###
                # Determine if it's a template set or a data set and the size
                try:
                    logging.info("Unpacking ID and length at byte position " + str(byte_position))
                    (flow_set_id, flow_set_length) = struct.unpack('!HH',
                                                                   flow_packet_contents[
                                                                   byte_position:byte_position + 4])
                    logging.info("Flow_SET_ID, Length[16:20] " + str((flow_set_id, flow_set_length)))
                except Exception as id_unpack_error:
                    logging.info("Out of bytes to unpack, breaking")
                    break  # Done with the packet

                # Advance past the initial header of ID and length
                byte_position += 4

                # Parse sets based on Set ID ###
                # ID 0 and 1 are not used
                # ID 2 is a Template
                # ID 3 is an Options Template
                # IDs > 255 are flow data

                # IPFIX template set (ID 2)
                if flow_set_id == 2:
                    template_position = byte_position
                    # final_template_position = (byte_position + flow_set_length) - 4
                    final_template_position = (byte_position + len(flow_packet_contents) - 4)
                    print("final_template_position: ", final_template_position)

                    # Cache for the following templates
                    template_cache = {}

                    while template_position < final_template_position:

                        print("template_position: ", template_position)
                        print("final_template_position: ", final_template_position)

                        logging.info("Unpacking template set at " + str(template_position))
                        (template_id, template_id_length) = struct.unpack('!HH', flow_packet_contents[
                                                                                 template_position:template_position + 4])
                        logging.info(
                            "Found (TEMPLATE_ID, TMP_counters) --[20:24]: " + str((template_id, template_id_length)))

                        template_position += 4  # Advance

                        # Template for flow data set
                        if template_id > 255:

                            # Produce unique hash to identify unique template ID and sensor
                            hashed_id = hash(str(sensor_address[0]) + str(template_id))
                            print("template_sensor_address[0]", str(sensor_address[0]))

                            # Cache to upload to template store
                            template_cache[hashed_id] = {}
                            template_cache[hashed_id]["Sensor"] = str(sensor_address[0])
                            template_cache[hashed_id]["Template ID"] = template_id
                            # template_cache[hashed_id]["Length"] = template_id_length
                            template_cache[hashed_id]["counters"] = template_id_length
                            # template_cache[hashed_id]["Definitions"] = collections.OrderedDict()  # ORDER MATTERS
                            template_cache[hashed_id]["%s" % source_ip] = collections.OrderedDict()  # ORDER MATTERS

                            # Iterate through template lines
                            for _ in range(0, template_id_length):
                                # Unpack template element number and length
                                '''change by Maojun Wang'''
                                print("template_position, TMP_Len ", template_position, template_id_length)
                                (template_element, template_element_length) = \
                                    struct.unpack('!HH', flow_packet_contents[template_position: template_position + 4])
                                print("template_element", hex(template_element), template_element & 0x7fff,
                                      type(template_element), eval('0x' + str(hex(template_element))[3:]))
                                # HEX to DEC
                                ie_type = template_element & 0x7fff

                                # Cache each Element and its Length
                                template_cache[hashed_id]["%s" % source_ip][
                                    template_element & 0x7fff] = template_element_length

                                # Advance
                                template_position += 4
                                (aa, vendor) = \
                                    struct.unpack('!HH', flow_packet_contents[template_position: template_position + 4])
                                print("aa,vendor content: ", aa, vendor)

                                template_position += 4
                                print("template_cache: ", template_cache)
                                print("template_position_after: ", template_position)

                        template_list.update(template_cache)  # Add template to the template cache, list_dict
                        logging.debug(str(template_list))
                        logging.info("Template[25-28] " + str(template_id) + " parsed successfully")

                    logging.info("Finished parsing templates at byte " + str(template_position) + " of " + str(
                        final_template_position))
                    logging.info('\n\n')

                    byte_position = (flow_set_length + byte_position) - 4  # Advance to the end of the flow
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
                    hashed_id = hash(str(sensor_address[0]) + str(flow_set_id))
                    print("data_sensor_address[0]", str(sensor_address[0]))
                    print("hashed_id: ", hashed_id)

                    # Check if there is a template
                    if hashed_id in template_list.keys():

                        logging.info("Parsing data flow " + str(flow_set_id) + " at byte " + str(byte_position))
                        now = datetime.datetime.utcnow()  # Get the current UTC time for the flows
                        data_position = byte_position  # Temporary counter
                        print("data_position, flow_set_length: ", data_position, flow_set_length)

                        # Iterate through flow bytes until we run out
                        while data_position + 4 <= (flow_set_length + (byte_position - 4)):

                            logging.info(
                                "Parsing flow " + str(flow_set_id) + " at " + str(data_position) + ", sequence " + str(
                                    packet_attributes["sequence_number"]))

                            # Cache the flow data, to be appended to flow_dic[]
                            flow_index = {
                                "_index": str("flow-" + now.strftime("%Y-%m-%d")),
                                "_type": "Flow",
                                "_source": {
                                    "Flow Type": "IPFIX",
                                    "Sensor": sensor_address[0],
                                    "Sequence": packet_attributes["sequence_number"],
                                    "Observation Domain": str(packet_attributes["observation_id"]),
                                    "Time": now.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (
                                                now.microsecond / 1000) + "Z",
                                }
                            }

                            print("hashed_id: ", hashed_id, template_list[hashed_id]["%s" % source_ip])
                            parameter = []
                            # Iterate through template elements
                            for template_key, field_size in template_list[hashed_id]["%s" % source_ip].items():
                                print("template_key, field_size, type(field_size)", template_key, field_size)

                                from AXOS.milan.ipfix_collector.xml_read import read_ipfix
                                ie_name = read_ipfix(str(template_key))
                                print("ie_name: ", ie_name)

                                # tree = ET.ElementTree(file='export.xml')
                                # root = tree.getroot()
                                # elem.tag = ''
                                # for elem in tree.iter():
                                #     for el, value in elem.attrib.items():
                                #         if template_key == int(value):
                                #             print("ie-type: {}, E7-parameter: {}".format(template_key, elem.tag))

                                if field_size == 65535:
                                    print("field is string", data_position)
                                    # Unpack the string
                                    (flow_len,) = struct.unpack('!s',
                                                                flow_packet_contents[data_position:data_position + 1])
                                    print("flow_len_value: ", flow_len)
                                    # bytes convert to int
                                    f_len = int.from_bytes(flow_len, byteorder='big', signed=False)
                                    print("flow_len: %d" % f_len)
                                    data_position += 1
                                    print("start decode")
                                    (flow_payload,) = struct.unpack('!%ss' % f_len, flow_packet_contents[
                                                                                    data_position:data_position + f_len])
                                    print("finish decode")
                                    # bytes convert to string
                                    print("flow_field_value: ", flow_payload)
                                    # flow_payload.decode()
                                    parameter.append("{}: {}".format(ie_name, flow_payload))
                                    data_position += f_len

                                elif field_size == 17:
                                    print("field is int with DEC need convert to ASCII", data_position)
                                    (flow_payload_2) = struct.unpack('!%sb' % field_size, flow_packet_contents[
                                                                                          data_position:data_position + field_size])
                                    print("flow_field_value_2: ", flow_payload_2, type(flow_payload_2))
                                    ma = "".join(chr(fl) for fl in flow_payload_2)
                                    print("MAC: ", ma),
                                    parameter.append(("{}: {}".format(ie_name, ma)))
                                    data_position += field_size

                                elif field_size < 17:
                                    # https://www.cnblogs.com/volcao/p/8807507.html
                                    print("field is int with DEC", data_position)
                                    unpack_re = ''
                                    if field_size == 1:
                                        unpack_re = '!B'
                                    elif field_size == 2:
                                        unpack_re = '!h'
                                    elif field_size == 4:
                                        unpack_re = '!L'
                                    elif field_size == 8:
                                        unpack_re = '!Q'
                                    (flow_payload_2) = struct.unpack(unpack_re, flow_packet_contents[
                                                                                data_position:data_position + field_size])
                                    print("flow_field_value_3: ", flow_payload_2, type(flow_payload_2))
                                    mm = "".join(str(int_value) for int_value in flow_payload_2)
                                    print("int_value: ", mm, type(mm)),
                                    if field_size == 4 and int(mm) > 999999999:

                                        tt = datetime.datetime.fromtimestamp(int(mm))
                                        print("time: ", tt, type(str(tt)))
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

                            print("\n\n{}_temp_{}: ".format(source_ip, flow_set_id))
                            for para in parameter:
                                print(para)
                            # Traffic and Traffic Category tagging
                            # Transport protocols eg TCP, UDP, etc
                            # print('sean_flow_index:', flow_index)

                    # No template, drop the flow per the standard and advanced the byte position
                    else:
                        byte_position += flow_set_length
                        logging.warning(
                            "Waiting on template " +
                            str(flow_set_id) +
                            " from " +
                            str(sensor_address[0]) +
                            ", sequence " +
                            str(packet_attributes["sequence_number"]) +
                            " - DROPPING"
                        )
                        # break
                        """changed by Maojun"""

                    byte_position = (flow_set_length + byte_position) - 4  # Advance to the end of the flow
                    logging.info("Ending data set at " + str(byte_position))

                # Received a flow set ID we haven't accounted for
                else:
                    logging.warning("Unknown flow ID " + str(flow_set_id) + " from " + str(sensor_address[0]))
                    break  # Bail out

            except Exception as error:
                print(error, "data error and modify by Maojun")

            # print('sean_flowdic:', template_list)


if __name__ == "__main__":
    # Socket listener ###
    '''change by Maojun Wang'''
    localip = socket.gethostbyname(socket.gethostname())
    try:
        netflow_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        netflow_sock.bind((localip, ipfix_port))
        logging.warning("Bound to port " + str(ipfix_port) + " - OK")
        netflow_sock.listen(50)

        while 1:
            time.sleep(0.1)
            sock, addr = netflow_sock.accept()
            print("E7_ip: ", addr[0], addr[1])
            t = threading.Thread(target=ipfix_data, args=(sock, addr[0], addr[1]))
            t.start()

    except ValueError as socket_error:
        logging.critical("Could not open or bind a socket on port " + str(ipfix_port))
        logging.critical(str(socket_error))
        sys.exit()
