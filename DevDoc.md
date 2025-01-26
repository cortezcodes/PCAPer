# PCAPer Development File
Last update: 1/15/2025

## Purpose
PCAPer is a Command line tool used to create PCAP files from templates. PCAP templates are saved in a database for future editing and generation.

## Requirements
1. PCAPer must be able to generate the major type of PCAP files:
    - UDP
    - TCP
    - ICMP
    - IGMP
    - ARP Request
    - ARP Reply
2. PCAPer must be able to store these templates in a database
3. PCAPer must be able to sort these templates into there own 'folders'.
4. PCAPer must be able to create folders. 
5. PCAPer must be able to all CRUD functions on folders
6. PCAPer must be able to do all CRUD functions on PCAP template
7. PCAPer must be able to import pcap files to be used at templates. 
8. PCAPer should be able to send PCAP directly
9. PCAPer should be able to scp PCAP files between vms. 
10. PCAPer must be able to set default file saving location

## User Interface
[Source IP | Source MAC | Dest IP | Dest MAC | Protocol]
- Create PCAP
- Create PCAP Template
- Settings
    - Manage Save Locations
    - Manage scp hosts
- Exit

## Database Classes
Packet 
- id
- Type
- Name
- Description
- Created Date
- Modified Date
- data -  example
```JSON
{
  "Ethernet": {
    "src": "00:11:22:33:44:55",
    "dst": "66:77:88:99:AA:BB",
    "type": 2048
  },
  "IP": {
    "src": "192.168.1.10",
    "dst": "192.168.1.20",
    "version": 4,
    "ihl": 5,
    "tos": 0,
    "len": 0,
    "id": 1,
    "flags": 0,
    "frag": 0,
    "ttl": 64,
    "proto": 17  // UDP protocol number
  },
  "UDP": {
    "sport": 12345,
    "dport": 80,
    "len": 0,
    "chksum": null
  },
  "ARP": {
    "hwtype": 1,
    "ptype": 2048,
    "hwlen": 6,
    "plen": 4,
    "op": 1,
    "hwsrc": "00:11:22:33:44:55",
    "psrc": "192.168.1.10",
    "hwdst": "66:77:88:99:AA:BB",
    "pdst": "192.168.1.20"
  },
  "Payload": "Hello, this is a test payload!"
}
```