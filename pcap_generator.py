from scapy.all import *

def udp_generator(src_ip: str, src_port: int, dest_ip: str, dest_port: int, payload: str):
    '''
    Function for generating pcap files using scapy
    '''
    #TODO Start here. Generate UDP packet