
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    user_name = Column(String, ForeignKey('users.name'))
    conversation = Column(String)
    # user = relationship("User", back_populates="conversations")

def initialize_db(engine):
    Base.metadata.create_all(engine)

# Call the initialize_db function to create the tables
initialize_db(engine)

