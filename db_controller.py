import json
from sqlite3 import IntegrityError
from rich.console import Console
from db import init_db
from sqlalchemy.orm import Session

from models import PacketTemplate
from protocols import UDPPacket

console = Console()

def startConnection():
    '''
    Initializes database if one does not already exist and returns a session object.
    '''
    # Initialize the database (create tables)
    sessionLocal: Session = init_db()
    # Create a database session
    return sessionLocal()

def create_packet_template(packet:UDPPacket):
    '''
    Creates a packet template
    '''
    session = startConnection()
    new_packet_template = PacketTemplate(type=packet.type, name=packet.name, data=packet.get_dict(), description=packet.description)
    try:
        session.add(new_packet_template)
        session.commit()
        return True
    except Exception as e:
        console.print("[red]Template name must be unique.[/red]")
        return False

def get_templates(type: str="all"):
    '''
    returns all templates of a given type. default is all templates available. 
    '''
    session: Session = startConnection()
    if type != "all":
        templates = session.query(PacketTemplate).filter(PacketTemplate.type == type).all()
    else:
        templates = session.query(PacketTemplate).all()
    return templates