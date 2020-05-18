from db import Base
from sqlalchemy import Column, Integer, String


class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    server = Column(String)

    def __str__(self):
        return f'Server(name={self.name})'

    def __repr__(self):
        return str(self)
