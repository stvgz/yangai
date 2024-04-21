from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

# from ai.model.user import User

Base = declarative_base()


class Conversation(Base):
    __tablename__ = 'conversation'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50))
    conversation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    notes = Column(Text, nullable=True)
    deleted = Column(Integer, default=0)
    sentences = relationship("Sentence", back_populates="conversation")

    # role_info
    role_info = Column(Text, nullable=True)

    # labels
    label_score = Column(Integer, nullable=True)
    label_text = Column(Text, nullable=True)
    label_from_user = Column(String(50), nullable=True)
    label_created_at = Column(DateTime, nullable=True)

    # user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    # user = relationship("User", back_populates="conversation")

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "conversation": self.conversation,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "notes": self.notes,
            "deleted": self.deleted,
            "label_score": self.label_score,
            "label_text": self.label_text,
            "label_from_user": self.label_from_user,
            "label_created_at": self.label_created_at,
            'role_info': self.role_info
        }


class Sentence(Base):
    __tablename__ = 'sentence'
    id = Column(Integer, primary_key=True)
    from_user = Column(String(50), nullable=True)
    to_user = Column(String(50), nullable=True)
    text = Column(Text, nullable=False)
    type = Column(String(50), nullable=True)
    model = Column(String(50), nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    notes = Column(Text, nullable=True)
    conversation_id = Column(Integer, ForeignKey('conversation.id'), nullable=True)
    conversation = relationship("Conversation", back_populates="sentences")

    # labels
    label_score = Column(Integer, nullable=True)
    label_text = Column(Text, nullable=True)
    label_from_user = Column(String(50), nullable=True)
    label_created_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "from_user": self.from_user,
            "to_user": self.to_user,
            "text": self.text,
            "type": self.type,
            "model": self.model,
            "created": self.created,
            "notes": self.notes,
            "conversation_id": self.conversation_id,
            "label_score": self.label_score,
            "label_text": self.label_text,
            "label_from_user": self.label_from_user,
            "label_created_at": self.label_created_at
            
        }


