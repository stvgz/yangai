from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Prompt(Base):
    __tablename__ = 'prompt'

    id = Column(Integer, primary_key=True)
    prompt_text = Column(Text)
    created_at = Column(DateTime)
    active = Column(Boolean)