import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from rich import print
import time

# Configure the database URL
DATABASE_URL = "sqlite:///pcaper.db"


# Function to initialize the database (create tables)
def init_db():
    # Create the engine
    engine = create_engine(DATABASE_URL)
    if not os.path.exists("pcaper.db"):
        Base.metadata.create_all(bind=engine)
        print("[green]Database initialized[/green]")
        time.sleep(1)

    return  sessionmaker(bind=engine)