from scapy.layers.inet import UDP, IP
from scapy.all import Raw, wrpcap
from scapy.layers.l2 import Ether
from util import clear, ensure_filepath

def udp_generator(src_mac: str, dest_mac: str, src_ip: str, src_port: int, dest_ip: str, dest_port: int, payload: str, output_file: str):
    '''
    Function for generating pcap files using scapy
    '''
    mac_layer = datalink_layer(src_mac=src_mac, dest_mac=dest_mac)
    ip_layer = network_layer(src_ip=src_ip, dest_ip=dest_ip)
    udp_layer = transport_layer(src_port=src_port, dest_port=dest_port)
    packet = mac_layer / ip_layer / udp_layer / Raw(load=payload)
    ensure_filepath(file_path=output_file)
    wrpcap(output_file, packet)

    clear()
    print(f"pcap file created at {output_file}")
    return 


def transport_layer(src_port: int, dest_port: int):
    '''
    Handles all transport layer configurations
    '''
    return UDP(sport=src_port, dport=dest_port)

def network_layer(src_ip: str, dest_ip: str):
    '''
    Handles all network layer configurations
    '''
    return IP(src=src_ip, dst=dest_ip)

def datalink_layer(src_mac:str, dest_mac:str):
    '''
    Handles all datalink layer configurations
    '''
    return Ether(src=src_mac, dst=dest_mac)