import typer


clear = lambda: print("\n"*10)
new_line = lambda: print("\n")

def display_menu(options: list[str], title:str=""):
    '''
    Helper function for displaying a terminal menu, providing auto numbering and optional title\n
    options: list[str] - each string within the list will become an option in the terminal menu\n
    title: str (optional) - creates a title for the terminal menu\n
    '''
    if title != "":
        print(title)

    for option in options:
        print(f"{options.index(option)+1}) {option}")

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