from scapy.layers.inet import IP, ICMP
from scapy.all import wrpcap
from models import PacketTemplate
from util import ensure_filepath

# Switch TCPPackets over to class
class ICMPPacket:
    def __init__(self,
             src_ip: str,
             dst_ip: str,
             message_type: int,
             code: int,
             ident: int,
             seq: int,
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
        :param  seq: Sequence number
        :param message_type: error code
        :param code: subset of the message_type
        :param ident: id used to sync a request and a reply
        '''
        self.type:str = "icmp"
        self.src_ip:str = src_ip
        self.dst_ip:str = dst_ip
        self.message_type:int = message_type
        self.code:int = code
        self.ident:int = ident
        self.seq:int = seq
        self.name:str = name
        self.description = description

    @classmethod
    def from_template(cls, template:PacketTemplate):
        return cls(src_ip=template.data["sip"],
                  dst_ip=template.data["dip"],
                  seq=template.data["seq"],
                  message_type=template.data["msg_type"],
                  code=template.data["code"],
                  ident=template.data["ident"]
                  )
    
    @classmethod
    def get_parameters_list(cls):
        '''
        returns a list of strings of all the parameters within this class. Used for when creating tables 
        '''
        return ["Type","Source IP", "Destination IP",
                "Message","Code","ID","Sequence #","Checksum"]

    def generate_packet(self, filepath: str):
        '''
        Given a filepath, generate UDP packet
        '''
        ip_layer = IP(src=self.src_ip, dst=self.dst_ip)
        icmp = ICMP(type=self.message_type,code=self.code, id=self.ident, seq=self.seq)
        packet = ip_layer / icmp
        ensure_filepath(file_path=filepath)
        wrpcap(filepath, packet)

    def get_dict(self):
        '''
        Returns a dictionary of all parameters and the cooresponding values
        '''
        return {"sip": self.src_ip, "dip": self.dst_ip, "name":self.name, "msg_type":self.message_type,
                "description": self.description, "seq":self.seq, "ident":self.ident, "code":self.code}
    
    def __repr__(self):
        return f"\nSrc IP: {self.src_ip}\nDest IP: {self.dst_ip}\nMessage Type: {self.message_type}\nCode: {self.code}\nID:{self.id}\nSequence #: {self.seq}\n\n"