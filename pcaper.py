import time
import typer
from util import display_menu, menu_selector, clear, new_line

def main(): 
    clear()
    while True:
        display_menu(["Create PCAP", "Create PCAP from Template", "Exit"], title="Welcome to PCAPer!")
        new_line()
        selection = menu_selector("<")
        new_line()

        match selection:
            case 1:
                create_pcap_prompt()
            case 2:
               print("Create PCAP from template")
            case 3:
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

if __name__ == "__main__":
    typer.run(main)