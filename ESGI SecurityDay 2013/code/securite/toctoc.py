#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from scapy.all import *
conf.verb = 0  # Empeche Scapy d'afficher des informations supplémentaires


def normalize_ports(ps):
    ports = set()
    for p in ps.split(','):
        if '-' in p:
            sp, ep = map(int, p.split('-'))
            ports.update(range(sp, ep+1))
        else:
            ports.add(int(p))
    return list(ports)


usage = "%s IP PORTS" % sys.argv[0]
if len(sys.argv) != 3:
    print usage
    sys.exit(1)

_, ip, ports = sys.argv
ports = normalize_ports(ports)
print "Starting scan on %d ports" % len(ports)

pkt = IP(dst=ip)/TCP(dport=ports, flags='S')
ans, unans = sr(pkt)

for sent, received in ans:
    if received.sprintf('%TCP.flags%') == 'SA':
        print "%d (%s) is open" % (sent.dport, sent.sprintf('%TCP.dport%'))
for sent in unans:
    print "%d (%s) is open|filtered" % (sent.dport, sent.sprintf('%TCP.dport%'))
