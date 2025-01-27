from scapy.layers.inet import UDP, IP, TCP
from scapy.all import Raw, wrpcap
from scapy.layers.l2 import Ether
from util import ensure_filepath

class UDPPacket:
    def __init__(self,
             src_ip: str,
             src_mac: str,
             src_port: int,
             dst_ip: str,
             dst_mac: str,
             dst_port: str,
             payload: str,
             length:int=None,
             checksum:int=None,
             name:str="",
             description:str=""
            ):
        '''
        Initialize the UDP packet parameters.
        :param src_ip: Source IP address
        :param src_mac: Source MAC address
        :param src_port: Source port
        :param dst_ip: Destination IP address
        :param dst_mac: Destination MAC address
        :param dst_port: Destination port
        :param payload: Data to include in the UDP packet
        :param length: Length of the UDP packet (header + payload)
        :param checksum: Custom checksum for the UDP packet
        '''
        self.type:str = "udp"
        self.src_ip:str = src_ip
        self.src_mac:str = src_mac
        self.src_port:int = src_port
        self.dst_ip:str = dst_ip
        self.dst_mac:str = dst_mac
        self.dst_port:int = dst_port
        self.payload:str = payload
        self.length:int = length
        self.checksum:int = checksum
        self.name:str = name
        self.description = description

    def generate_packet(self, filepath: str):
        '''
        Given a filepath, generate UDP packet
        '''
        mac_layer = Ether(src=self.src_mac, dst=self.dst_mac)
        ip_layer = IP(src=self.src_ip, dst=self.dst_ip)
        udp_layer = UDP(sport=self.src_port, dport=self.dst_port)
        packet = mac_layer / ip_layer / udp_layer / Raw(load=self.payload)
        ensure_filepath(file_path=filepath)
        wrpcap(filepath, packet)

    def get_dict(self):
        '''
        Returns a dictionary of all parameters and the cooresponding values
        '''
        return {"sip": self.src_ip, "smac": self.src_mac, "sport":self.src_port,
                "dip": self.dst_ip, "dmac":self.dst_mac, "dport":self.dst_port,
                "payload":self.payload, "length":self.length, "checksum":self.checksum, "name":self.name,
                "description": self.description}
    
    def __repr__(self):
        return f"Src IP: {self.src_ip}\nSrc MAC: {self.src_mac}\nSrc Port: {self.src_port}\nDest IP: {self.dst_ip}\nDest MAC: {self.dst_mac}Dest Port: {self.dst_port}\nPayload: [green]{self.payload}[/green]\nChecksum: {self.checksum}\nLength: {self.length}\n"