#!/usr/bin/env python3

import scapy.all as scapy
import argparse as argp

def get_arguments():
    parser = argp.ArgumentParser(description='Send an ARP broadcast and prints the result')
    parser.add_argument('--target', '-t', dest="target", type=str,
        help='IP address of the host which you send the packet')
    args = parser.parse_args()
    return args

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
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

args = get_arguments()
scan_result = scan(args.target)
print_result(scan_result)
