from scapy.layers.inet import UDP, IP, TCP
from scapy.all import Raw, wrpcap
from scapy.layers.l2 import Ether
from util import clear, ensure_filepath

def tcp_generator(src_mac: str,  src_ip: str, src_port: int, dest_mac: str, dest_ip: str, dest_port: int, flag: str, payload: str, output_file: str):
    '''
    Function for generating tcp pcap files using scapy
    Returns the name of the output file if successful
    '''
    mac_layer = datalink_layer(src_mac=src_mac, dest_mac=dest_mac)
    ip_layer = network_layer(src_ip=src_ip, dest_ip=dest_ip)
    tcp_layer = transport_layer(type="tcp", src_port=src_port, dest_port=dest_port, flag=flag)
    packet = mac_layer / ip_layer / tcp_layer / Raw(load=payload)
    ensure_filepath(file_path=output_file)
    wrpcap(output_file, packet)
    return  output_file


def transport_layer(type: str,src_port: int, dest_port: int, flag: str = ""):
    '''
    Handles all transport layer configurations
    '''
    if type == "udp":
        return UDP(sport=src_port, dport=dest_port)
    elif type == "tcp":
        return TCP(sport=src_port, dport=dest_port, flags=flag)

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