#!/usr/bin/env python3

import scapy.all as scapy
import argparse as argp

parser = argp.ArgumentParser(description='Scan the hosts and prints the result')
parser.add_argument('--ip', '-i', type=str,
        help='IP address of the host which you send the packet')
parser.add_argument('--mac', '-m', type=str,
        help='MAC address of the host which you send the packet')

args = parser.parse_args()
ip = args.ip
mac = args.mac

def scan(ip, mac):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst=mac)
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return(clients_list)

def print_result(results_list):
    print("#######################################################")
    print("IP\t\t\tMAC Address")
    print("#######################################################")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])
        print("#######################################################")

scan_result = scan(ip, mac)
print_result(scan_result)
