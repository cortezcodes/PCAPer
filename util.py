import typer
from rich.console import Console
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