import json
from sqlite3 import IntegrityError
import time
from typing import List
import typer
from rich.console import Console
from rich.table import Table
from db_controller import create_packet_template, get_templates
from models import PacketTemplate
from pcap_generator import tcp_generator
from protocols.UDPPacket import UDPPacket
from util import create_table, display_menu, menu_selector, clear, new_line

console = Console()

def main(): 
    clear()
    while True:
        display_menu(["Create PCAP", "Create PCAP from Template","Create PCAP from File", "Manage Templates","Exit"], title="Welcome to PCAPer!")
        new_line()
        selection = menu_selector("<")
        new_line()

        match selection:
            case 1:
                clear()
                create_pcap_prompt()
            case 2:
               create_pcap_from_template_prompt()
            case 3:
                print("Create PCAP from File - coming soon")
            case 4:
                print("Manage Templates - Coming soon")
            case 5:
                clear()
                print("Goodbye")
                break
            case _:
                clear()
                console.print("[red]Invalid:[/red] Bad input, please try again.")

        new_line()

def create_pcap_from_template_prompt():
    '''
    Create pcap from a saved template
    '''
    clear()
    while True:
        display_menu(["UDP", "TCP", "ICMP", "IGMP", "ARP Request", "ARP Respone", "all", "Back to Main Menu"], title="Select a protocol")
        new_line()
        selection = menu_selector("<")
        match selection:
            case 1:
                udp_templates_prompt()
                break
            case 2:
                tcp_templates_prompt()
                break
            case 7:
                clear()
                break
            case _:
                clear()
                console.print("[red]Invalid:[/red] Bad input, please try again.\n")

def udp_templates_prompt():
    '''
    Displays the udp template table and provides prompts for pcap creation from template
    '''
    clear()
    title="UDP Templates"
    columns = ["#","Type","Source MAC","Source IP","Source Port", "Destination MAC", "Destination IP", "Destination Port","Length", "Checksum", "Payload"]


    udp_templates: List[PacketTemplate] = get_templates("udp")
    table = create_table(type="udp", title=title, columns=columns, templates=udp_templates)

    console.print(table)

    # Template Selection Prompting
    template_selected: bool = False
    while not template_selected:
        selection = typer.prompt("Select a template by # or -1 to go back")
        if int(selection) == -1:
            clear()
            return
        try:
            template = udp_templates[int(selection)-1]
            template_selected = True
        except Exception as e:
            print("Invalid selection, please try again.")
            template_selected = False

    filepath = typer.prompt("PCAP filename", default="./pcap_files/udp_output.pcap")
    udp_packet = UDPPacket(src_mac=template.data["smac"],
                  src_ip=template.data["sip"],
                  src_port=template.data["sport"],
                  dest_mac=template.data["dmac"],
                  dest_ip=template.data["dip"],
                  dest_port=template.data["dport"],
                  length=template.data["length"],
                  checksum=template.data["checksum"],
                  payload=template.data["payload"])
    udp_packet.generate_packet(filepath=filepath)

    clear()

def tcp_templates_prompt():
    '''
    Displays the udp template table and provides prompts for pcap creation from templat
    '''
    clear()
    title="TCP Templates"
    columns = ["#","Type","Source MAC","Source IP","Source Port", "Destination MAC", "Destination IP", "Destination Port","Flag", "Payload"]


    tcp_templates: List[PacketTemplate] = get_templates("tcp")
    table = create_table(type="tcp", title=title, columns=columns, templates=tcp_templates)

    console.print(table)

    # Template Selection Prompting
    template_selected: bool = False
    while not template_selected:
        selection = typer.prompt("Select a template by # or -1 to go back")
        if int(selection) == -1:
            clear()
            return
        try:
            template = tcp_templates[int(selection)-1]
            template_selected = True
        except Exception as e:
            print("Invalid selection, please try again.")
            template_selected = False

    filepath = typer.prompt("PCAP filename", default="./pcap_files/udp_output.pcap")
    udp_generator(src_mac=template.data["smac"],
                  src_ip=template.data["sip"],
                  src_port=template.data["sport"],
                  dest_mac=template.data["dmac"],
                  dest_ip=template.data["dip"],
                  dest_port=template.data["dport"],
                  payload=template.data["payload"],
                  output_file=filepath)

    clear()

def create_pcap_prompt():
    '''
    Prompter for handling creating a new pcap file
    '''
    while True:
        display_menu(["UDP", "TCP", "ICMP", "IGMP", "ARP Request", "ARP Respone", "Back to Main Menu"], title="Select a protocol")
        new_line()
        selection = menu_selector("<")
        match selection:
            case 1:
                create_udp_prompt()
                break
            case 2:
                create_tcp_prompt()
                break
            case 7:
                clear()
                break
            case _:
                clear()
                console.print("[red]Invalid:[/red] Bad input, please try again.\n")

def create_tcp_prompt():
    '''
    Prompter for handling gathering parameters to build a TCP
    '''
    clear()
    confirmed = False
        
    while not confirmed:
        console.print("[green]TCP Packet Configuration[/green]")
        src_mac = typer.prompt("Source Mac", default="00:11:22:33:44:55")
        src_ip = typer.prompt("Source IP", default="1.1.1.1")
        src_port = typer.prompt("Source Port", default=12345)
        flag = typer.prompt("TCP Flage (S = SYN or A = ACK)", default="")
        dst_mac = typer. prompt("Destination Mac", default="66:77:88:99:AA:BB")
        dst_ip = typer.prompt("Destination IP", default="2.2.2.2")
        dst_port = typer.prompt("Destination Port", default=80)
        payload = typer.prompt("Payload", default="")
        filepath = typer.prompt("PCAP filepath", default="./pcap_files/tcp_output.pcap")
        clear()
        console.print(f"Src IP: {src_ip}\nSrc Port: {src_port}\nDest IP: {dst_ip}\n" +
                                  f"Dest Port: {dst_port}\nFlag: {flag}\nPayload: [green]{payload}[/green]\nFilepath: {filepath}\n\n")
        confirmed = typer.confirm("Confirm")
        
        if not confirmed:
            exit = typer.confirm("Would you like to go back to the main menu?")
            if exit:
                clear()
                return
            clear()
        
    make_template: bool = typer.confirm("Would you like to make this packet into a template?")    

    output_file = tcp_generator(src_mac=src_mac, dest_mac=dst_mac,src_ip=src_ip, 
                                src_port=src_port, dest_ip=dst_ip, dest_port=dst_port, 
                                flag=flag, payload=payload, output_file=filepath)
    if output_file:
        clear()
        console.print(f"pcap file created at {output_file}")
    
    if make_template:
            data = {"smac":src_mac,
                    "sip":src_ip,
                    "sport":src_port,
                    "dmac":dst_mac,
                    "dip":dst_ip,
                    "dport": dst_port,
                    "flag": flag,
                    "payload": payload,
                    }
            create_packet_template_prompter(type="tcp", data=data)
            console.print("[green]Template created.[/green]")

def create_udp_prompt():
    '''
    Prompter for handling gathering parameters to build a UDP pcap.
    '''
    clear()
    confirmed = False
        
    while not confirmed:
        console.print("[green]UDP Packet Configuration[/green]")
        src_mac = typer.prompt("Source Mac", default="00:11:22:33:44:55")
        src_ip = typer.prompt("Source IP", default="1.1.1.1")
        src_port = typer.prompt("Source Port", default=12345)
        dst_mac = typer. prompt("Destination Mac", default="66:77:88:99:AA:BB")
        dst_ip = typer.prompt("Destination IP", default="2.2.2.2")
        dst_port = typer.prompt("Destination Port", default=80)
        payload = typer.prompt("Payload", default="Have you ever...dreamed?")
        checksum = typer.prompt("Checksum", default="")
        length = typer.prompt("Length", default="")
        filepath = typer.prompt("PCAP filepath", default="./pcap_files/udp_output.pcap")

        clear()
        udp_packet:UDPPacket = UDPPacket(src_ip=src_ip, src_mac=src_mac, src_port=src_port, 
                               dst_ip=dst_ip, dst_mac=dst_mac, dst_port=dst_port,
                               payload=payload, length=length, checksum=checksum)
        
        console.print(str(udp_packet)+f"\nfilepath: {filepath}\n\n")
        confirmed = typer.confirm("Confirm")
        
        if not confirmed:
            exit = typer.confirm("Would you like to go back to the main menu?")
            if exit:
                clear()
                return
            clear()
        
    make_template: bool = typer.confirm("Would you like to make this packet into a template?")    
    udp_packet.generate_packet(filepath)

    clear()
    console.print(f"pcap file created")
    
    if make_template:
        create_packet_template_prompter(udp_packet)

def create_packet_template_prompter(packet: UDPPacket):
    '''
    Provides the prompts for creating a packet template
    '''
    isCreated = False
    while not isCreated:
        new_line()
        console.print("[green]PCAP Template Creation Tool[/green]")
        packet.name = typer.prompt("Packet Template Name")
        packet.description =typer.prompt("Description of Packet", default="")
        isCreated = create_packet_template(packet)
        if isCreated:
            clear()
            console.print("[green]PCAP template created successfully[/green]") 


if __name__ == "__main__":
    typer.run(main)