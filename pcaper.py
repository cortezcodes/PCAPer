import time
import typer
from pcap_generator import udp_generator
from util import display_menu, menu_selector, clear, new_line

def main(): 
    clear()
    while True:
        display_menu(["Create PCAP", "Create PCAP from Template","Create PCAP from File", "Exit"], title="Welcome to PCAPer!")
        new_line()
        selection = menu_selector("<")
        new_line()

        match selection:
            case 1:
                create_pcap_prompt()
            case 2:
               print("Create PCAP from template")
            case 3:
                print("Create PCAP from File")
            case 4:
                print("Goodbye")
                time.sleep(1)
                break
            case _:
                print("[red]Invalid:[/red] Bad input, please try again.")

        new_line()

def create_pcap_prompt():
    '''
    Prompter for handling creating a new pcap file
    '''
    display_menu(["UDP", "TCP", "ICMP", "IGMP", "ARP Request", "ARP Respone"], title="Select a protocol")
    new_line()
    selection = menu_selector("<")
    match selection:
        case 1:
            create_udp_prompt()

def create_udp_prompt():
    '''
    Prompter for handling gathering parameters to build a UDP pcap.
    '''
    new_line()
    confirmed = False
    src_ip: str = ""
    src_port: int = None
    dst_ip: str = ""
    dst_port: int = None
    payload: str = ""
    filename: str = ""
    filepath: str = "./PCAPs/"
        
    while not confirmed:
        src_ip = typer.prompt("Source IP")
        src_port = typer.prompt("Source Port", default=12345)
        dst_ip = typer.prompt("Destination IP")
        dst_port = typer.prompt("Destination Port", default=80)
        payload = typer.prompt("Payload", default="Have you ever...dreamed?")
        filename = typer.prompt("PCAP filename", default="PCAPer_output.pcap")
        filepath = typer.prompt("File location", default="./PCAPs/")
        clear()
        confirmed = typer.confirm(f"Src IP: {src_ip}\nSrc Port: {src_port}\nDest IP: {dst_ip}\nDest Port: {dst_port}\nPayload: {payload}\n"+
                                  f"Filename: {filename}\nFilepath: {filepath}")
        
    udp_generator(src_ip=src_ip, src_port=src_port, dest_ip=dst_ip, dest_port=dst_port, payload=payload)

    

if __name__ == "__main__":
    typer.run(main)