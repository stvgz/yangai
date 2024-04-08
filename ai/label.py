# Label of conversation
# for customers: if the customer looks like a real customer
# for user: if he/she acting like a great user


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .conversation import Conversation

class Label(Base):
    __tablename__ = 'label'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    conversation_id = Column(Integer, ForeignKey('conversation.id'))
    conversation = relationship("Conversation", back_populates="labels")
