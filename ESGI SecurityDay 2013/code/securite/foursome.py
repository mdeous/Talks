#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from scapy.all import *

if len(sys.argv) != 3:
    print "USAGE: %s INPUT_PCAP OUTPUT_PCAP" % sys.argv[0]
    sys.exit(1)
_, in_pcap, out_pcap = sys.argv

print "Reading input file: %s" % in_pcap
packets = rdpcap(in_pcap)
handshake_packets = []
for packet in packets:
    if EAPOL in packet:
        print packet.sprintf(" - Found packet from %Dot11.addr2% to %Dot11.addr1%")
        handshake_packets.append(packet)
print "Writing to output file: %s" % out_pcap
wrpcap(out_pcap, handshake_packets)
print "Done"
