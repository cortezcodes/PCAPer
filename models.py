from sqlalchemy import Boolean, Column, Date, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class PacketTemplate(Base):
    __tablename__="packet_templates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    date_created = Column(DateTime, default=func.now(), nullable=False)
    last_modified = Column(DateTime, default=func.now(), nullable=False)
    data = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<PacketTemplate(type='{self.type}', data='{self.data}')>"