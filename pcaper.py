import json
from sqlite3 import IntegrityError
import time
from typing import List
import typer
from rich.console import Console
from rich.table import Table
from db_controller import create_packet_template, get_templates
from models import PacketTemplate
from pcap_generator import udp_generator
from util import display_menu, menu_selector, clear, new_line

console = Console()

def main(): 
    clear()
    while True:
        display_menu(["Create PCAP", "Create PCAP from Template","Create PCAP from File", "Exit"], title="Welcome to PCAPer!")
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
                print("Create PCAP from File")
            case 4:
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
            case 7:
                clear()
                break
            case _:
                clear()
                console.print("[red]Invalid:[/red] Bad input, please try again.\n")

def udp_templates_prompt():
    '''
    Displays the udp template table and provides prompts for creation
    '''
    table =Table(title="UDP Templates")
    table.add_column("#", justify="center")
    table.add_column("Type", justify="center")
    table.add_column("Source MAC", justify="center")
    table.add_column("Source IP", justify="center")
    table.add_column("Source Port", justify="center")
    table.add_column("Destination MAC", justify="center")
    table.add_column("Destination IP", justify="center")
    table.add_column("Destination Port", justify="center")
    table.add_column("Payload", justify="center")

    udp_templates: List[PacketTemplate] = get_templates("udp")
    temp_num: int = 1
    for template in udp_templates:
        table.add_row(str(temp_num),
                      template.type, 
                      template.data["smac"],
                      template.data["sip"],
                      str(template.data["sport"]),
                      template.data["dmac"],
                      template.data["dip"],
                      str(template.data["dport"]),
                      template.data["payload"])
        temp_num += 1

    console.print(table)

    #TODO Create menu for selecting a template to make a pcap from template


    
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
            case 7:
                clear()
                break
            case _:
                clear()
                console.print("[red]Invalid:[/red] Bad input, please try again.\n")

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
        filepath = typer.prompt("PCAP filename", default="./pcap_files/udp_output.pcap")
        clear()
        console.print(f"Src IP: {src_ip}\nSrc Port: {src_port}\nDest IP: {dst_ip}\n" +
                                  f"Dest Port: {dst_port}\nPayload: [green]{payload}[/green]\nFilepath: {filepath}\n\n")
        confirmed = typer.confirm("Confirm")
        
        if not confirmed:
            exit = typer.confirm("Would you like to go back to the main menu?")
            if exit:
                clear()
                return
            clear()
        
    make_template: bool = typer.confirm("Would you like to make this packet into a template?")    

    output_file = udp_generator(src_mac=src_mac, dest_mac=dst_mac,src_ip=src_ip, 
                                src_port=src_port, dest_ip=dst_ip, dest_port=dst_port, 
                                payload=payload, output_file=filepath)
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
                    "payload": payload
                    }
            create_packet_template_prompter(type="udp", data=data)



def create_packet_template_prompter(type: str, data: json):
    '''
    Provides the prompts for creating a packet template
    '''
    isCreated = False
    while not isCreated:
        new_line()
        console.print("[green]PCAP Template Creation Tool[/green]")
        name = typer.prompt("Packet Template Name")
        description =typer.prompt("Description of Packet", default="")
        isCreated = create_packet_template(type=type, name=name, data=data, description=description)
        if isCreated:
            clear()
            console.print("[green]PCAP template created successfully[/green]") 


if __name__ == "__main__":
    typer.run(main)