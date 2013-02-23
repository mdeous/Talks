#!/usr/bin/env python
# -*- coding; utf-8 -*-

from scapy.all import *


class Disney(Packet):
    name = "Walt Disney Protocol"
    fields_desc = [
        ShortField("mickey", 5),
        XByteField("minnie", 3),
        IntEnumField("donald", 1, {
            1: "happy",
            2: "cool",
            3: "angry"
        })
    ]

disney_pkt = Disney(mickey=1, minnie=2, donald=3)
print disney_pkt.sprintf("Donald is %Disney.donald%")
