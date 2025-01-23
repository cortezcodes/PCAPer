import time
import typer
from rich.console import Console
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
               print("Create PCAP from template")
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
    new_line()
    confirmed = False
    src_mac: str = ""
    src_ip: str = ""
    src_port: int = None
    src_mac: str = ""
    dst_ip: str = ""
    dst_port: int = None
    payload: str = ""
    filepath: str = ""
        
    while not confirmed:
        src_mac = typer.prompt("Source Mac", default="00:11:22:33:44:55")
        src_ip = typer.prompt("Source IP", default="1.1.1.1")
        src_port = typer.prompt("Source Port", default=12345)
        dst_mac = typer. prompt("Destination Mac", default="66:77:88:99:AA:BB")
        dst_ip = typer.prompt("Destination IP", default="2.2.2.2")
        dst_port = typer.prompt("Destination Port", default=80)
        payload = typer.prompt("Payload", default="Have you ever...dreamed?")
        filepath = typer.prompt("PCAP filename", default="./pcap_files/udp_output.pcap")
        clear()
        confirmed = typer.confirm(f"Src IP: {src_ip}\nSrc Port: {src_port}\nDest IP: {dst_ip}\n" +
                                  f"Dest Port: {dst_port}\nPayload: {payload}\nFilepath: {filepath}\n")
        
    udp_generator(src_mac=src_mac, dest_mac=dst_mac,src_ip=src_ip, src_port=src_port, dest_ip=dst_ip, dest_port=dst_port, payload=payload, output_file=filepath)

    

if __name__ == "__main__":
    typer.run(main)