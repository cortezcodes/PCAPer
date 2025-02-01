import typer
from rich.console import Console
from rich.table import Table
import os

console = Console()
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
new_line = lambda: print("\n")


def display_menu(options: list[str], title:str=""):
    '''
    Helper function for displaying a terminal menu, providing auto numbering and optional title\n
    options: list[str] - each string within the list will become an option in the terminal menu\n
    title: str (optional) - creates a title for the terminal menu\n
    '''
    if title != "":
        console.print(title)

    for option in options:
        console.print(f"[blue]{options.index(option)+1})[/blue] {option}")

def menu_selector(question: str):
    '''
    wrapper around the typer.prompt that includes error handling.
    returns an int from the user or -1 if invalid response. 
    '''
    try:
       return int(typer.prompt(question))
    except ValueError as e:
        new_line()
        print("[red]ERROR:[/red] Invalid input.")
        new_line()
        return -1
    
def ensure_filepath(file_path: str):
    '''
    Ensures a given filepath exists. If any directory within the filepath does not exist, than it creates it. 
    '''
    # Get the directory name from the file path
    directory = os.path.dirname(file_path)
    
    # Create the directories if they don't exist
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def create_table(type: str,title:str, columns:list, templates:list):
    '''
    Generic table generator based on the type of protocol template being displayed
    '''
    table = Table(title=title)
    for column in columns:
        table.add_column(column, justify="center")

    temp_num: int = 1
    for template in templates:
        if type == "udp":
            table.add_row(str(temp_num),
                        template.type, 
                        template.data["smac"],
                        template.data["sip"],
                        str(template.data["sport"]),
                        template.data["dmac"],
                        template.data["dip"],
                        str(template.data["dport"]),
                        template.data["payload"])
        elif type == "tcp":
            table.add_row(str(temp_num),
                        template.type, 
                        template.data["smac"],
                        template.data["sip"],
                        str(template.data["sport"]),
                        template.data["dmac"],
                        template.data["dip"],
                        str(template.data["dport"]),
                        template.data["flags"],
                        str(template.data["seq"]),
                        str(template.data["ack"]),
                        template.data["payload"])
        temp_num += 1
    
    return table
