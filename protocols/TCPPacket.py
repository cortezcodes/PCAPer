from scapy.layers.inet import IP, TCP
from scapy.all import Raw, wrpcap
from scapy.layers.l2 import Ether
from models import PacketTemplate
from util import ensure_filepath

# Switch TCPPackets over to class
class TCPPacket:
    def __init__(self,
             src_ip: str,
             src_mac: str,
             src_port: int,
             dst_ip: str,
             dst_mac: str,
             dst_port: str,
             seq: int,
             ack: int,
             flags: str,
             payload: str,
             checksum:int=None,
             name:str="",
             description:str=""
            ):
        '''
        Initialize the TCP packet parameters.
        :param src_ip: Source IP address
        :param src_mac: Source MAC address
        :param src_port: Source port
        :param dst_ip: Destination IP address
        :param dst_mac: Destination MAC address
        :param dst_port: Destination port
        :param  seq: TCP Sequence number
        :param ack: Acknowledgment number
        :param flags: SYN, ACK, FIN, RST flags
        :param payload: Data to include in the UDP packet
        :param length: Length of the UDP packet (header + payload)
        :param checksum: Custom checksum for the UDP packet
        '''
        self.type:str = "tcp"
        self.src_ip:str = src_ip
        self.src_mac:str = src_mac
        self.src_port:int = src_port
        self.dst_ip:str = dst_ip
        self.dst_mac:str = dst_mac
        self.dst_port:int = dst_port
        self.seq:int = seq
        self.ack:int = ack
        self.flags:str = flags
        self.payload:str = payload
        self.checksum:int = checksum
        self.name:str = name
        self.description = description

    @classmethod
    def from_template(cls, template:PacketTemplate):
        return cls(src_mac=template.data["smac"],
                  src_ip=template.data["sip"],
                  src_port=template.data["sport"],
                  dst_mac=template.data["dmac"],
                  dst_ip=template.data["dip"],
                  dst_port=template.data["dport"],
                  seq=template.data["seq"],
                  ack=template.data["ack"],
                  flags=template.data["flags"],
                  payload=template.data["payload"])
    
    @classmethod
    def get_parameters_list(cls):
        '''
        returns a list of strings of all the parameters within this class. Used for when creating tables 
        '''
        return ["Type","Source MAC","Source IP","Source Port", 
                "Destination MAC", "Destination IP", "Destination Port",
                "Flags","Sequence #","Ack #", "Payload"]

    def generate_packet(self, filepath: str):
        '''
        Given a filepath, generate UDP packet
        '''
        mac_layer = Ether(src=self.src_mac, dst=self.dst_mac)
        ip_layer = IP(src=self.src_ip, dst=self.dst_ip)
        udp_layer = TCP(sport=self.src_port, dport=self.dst_port, seq=self.seq, ack=self.ack, flags=self.flags)
        packet = mac_layer / ip_layer / udp_layer / Raw(load=self.payload)
        ensure_filepath(file_path=filepath)
        wrpcap(filepath, packet)

    def get_dict(self):
        '''
        Returns a dictionary of all parameters and the cooresponding values
        '''
        return {"sip": self.src_ip, "smac": self.src_mac, "sport":self.src_port,
                "dip": self.dst_ip, "dmac":self.dst_mac, "dport":self.dst_port,
                "payload":self.payload, "checksum":self.checksum, "name":self.name,
                "description": self.description, "flags":self.flags,"ack":self.ack, "seq":self.seq}
    
    def __repr__(self):
        return f"\nSrc IP: {self.src_ip}\nSrc MAC: {self.src_mac}\nSrc Port: {self.src_port}\nDest IP: {self.dst_ip}\nDest MAC: {self.dst_mac}\nDest Port: {self.dst_port}\nFlags: {self.flags}\nSequence #: {self.seq}\nAck: {self.ack}\nPayload: [green]{self.payload}[/green]\nChecksum: {self.checksum}\n"