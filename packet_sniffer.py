#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http

def sniff(iface):
    scapy.sniff(iface=iface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            load = print(packet[scapy.Raw].load)

iface = input(print("[?] Insert your interface here: ", end=''))
sniff(iface)
