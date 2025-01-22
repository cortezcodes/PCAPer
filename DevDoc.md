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