"""
Conversation
Sentence
Label

User
"""


# attribute of Conversation
# 1. user_id
# 1. user_name
# 2. created_at

# temp code for importing
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

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

    # def __repr__(self):
    #     return f"<Conversation(id={self.id}, user_id={self.user_id}, created_at={self.created_at}, updated_at={self.updated_at})>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "conversation": self.conversation,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "notes": self.notes,
            "deleted": self.deleted
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
            "conversation_id": self.conversation_id
        }

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    # conversations = relationship("Conversation", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, user_name={self.user_name}, created_at={self.created_at})>"


# Class Label has following attributes
# id, sentence_id, type, userid, score, text, created_at, updated_at, notes
class Label(Base):
    __tablename__ = 'label'
    id = Column(Integer, primary_key=True)
    sentence_id = Column(Integer, ForeignKey('sentence.id'), nullable=True)

    type = Column(String(50), nullable=True)
    userid = Column(Integer, ForeignKey('user.id'), nullable=True)
    
    score = Column(Integer, nullable=True)
    text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    notes = Column(Text, nullable=True)

# init all
def initialize_db(engine):
    Base.metadata.create_all(engine)


from app.db.db import get_engine
engine = get_engine()

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


DBHOST = os.getenv("DBHOST")
DBPASS = os.getenv("DBPASS")

Session = sessionmaker(bind=engine)

class ConversationManager:
    def __init__(self, sentences = []):
        self.session = Session()
        self.sentences = sentences

    def create_conversation(self, user_name, conversation, notes=None):
        """Create a new conversation in the database."""
        new_conversation = Conversation(user_name=user_name, conversation=conversation, notes=notes)

        # add sentences to table
        for sentence in self.sentences:
            new_conversation.sentences.append(sentence)

        self.session.add(new_conversation)
        self.session.commit()
        return new_conversation

    def add_sentence(self, from_user, text, type=None, model=None, notes=None):
        """Add a sentence to the conversation."""
        sentence = Sentence(from_user=from_user, text=text, type=type, model=model, notes=notes)
        self.sentences.append(sentence)
        return sentence

    def get_sentence_by_conversation(self, conversation_id, return_json=False):
        """Get sentences by conversation id."""
        sentences = self.session.query(Sentence).filter(Sentence.conversation_id == conversation_id).all()
        if return_json:
            return [sentence.to_dict() for sentence in sentences]
        return sentences


    def update_conversation(self, conversation_id, updated_conversation, notes=None):
        """Update an existing conversation."""
        conversation = self.session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            conversation.conversation = updated_conversation
            self.session.commit()
        return conversation

    def delete_conversation(self, conversation_id):
        """Delete a conversation from the database."""
        conversation = self.session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            self.session.delete(conversation)
            self.session.commit()

    def close_session(self):
        """Close the database session."""
        self.session.close()

    
    # get conversation, sentence, and label by id
    def get_conversation(self, conversation_id):
        """Get conversation by id."""
        return self.session.query(Conversation).filter(Conversation.id == conversation_id).first()

    def list_conversations(self):
        """List all conversations."""
        return self.session.query(Conversation).all()

    def list_active_conversations(self, return_json=False, limit = 20):
        """List all active conversations."""
        conversations = self.session.query(Conversation).filter(Conversation.deleted == 0).limit(20).all()

        if return_json:
            return [conversation.to_dict() for conversation in conversations]
        return conversations

    def list_active_conversations_by_user(self, user_name, return_json=False, order = 'desc'):
        """List all deleted conversations by user."""
        conversations =  self.session.query(Conversation).filter(Conversation.deleted == 0, Conversation.user_name == user_name).order_by(Conversation.created_at.desc()).all()

        if return_json:
            return [conversation.to_dict() for conversation in conversations]

        return conversations

    def get_conversation_with_sentences(self, conversation_id):
        """Get conversation and its sentences by conversation id, join them into one data."""
        conversation = self.session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            return None
        
        sentences = self.session.query(Sentence).filter(Sentence.conversation_id == conversation_id).all()
        conversation_data = {
            "id": conversation.id,
            "user_name": conversation.user_name,
            "conversation": conversation.conversation,
            "notes": conversation.notes,
            "sentences": [{"from_user": sentence.from_user, "text": sentence.text, "type": sentence.type, "model": sentence.model, "notes": sentence.notes} for sentence in sentences]
        }
        
        return conversation_data

    def get_conv_sentence(self, conversation_id):
        """Get sentences by conversation id."""
        return self.session.query(Sentence).filter(Sentence.conversation_id == conversation_id).all()

    # Add label to conversation or sentences
    def add_label(self, sentence_id, type = 'score', userid = None, score = None, text = None, notes = None):
        """Add label to conversation or sentences."""
        label = Label(sentence_id=sentence_id, type=type, userid=userid, score=score, text=text, notes=notes)
        self.session.add(label)
        self.session.commit()
        return label



# Assuming there's a User class defined somewhere that looks something like this:
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     conversations = relationship("Conversation", back_populates="user")


if __name__ == "__main__":
    
    
    # 
    initialize_db(engine)
    # Create a new conversation
    CM = ConversationManager()
    
    # user_name = "TestUser"
    # conversation = "This is a test conversation."
    # new_conversation = CM.create_conversation(user_name, conversation)
    # print(f"New conversation created: {new_conversation}")

    # updated_conversation = "This is an updated test conversation."
    # updated = CM.update_conversation(new_conversation.id, updated_conversation)
    # if updated:
    #     print(f"Conversation updated: {updated.conversation}")
    # else:
    #     print("Failed to update conversation.")

    # # CM.delete_conversation(new_conversation.id)
    # # print(f"Conversation with ID {new_conversation.id} deleted.")

    # CM.close_session()
    # print("Session closed.")



    ## Test 2 conversation with different sentences

    s1 = Sentence(from_user="user1", text="This is a test sentence.", type="test")
    s2 = Sentence(from_user="user2", text="This is another test sentence.", type="test")

    CM.sentences.append(s1)
    CM.sentences.append(s2)

    # Create a new conversation with the sentences
    user_name = "user1"
    conversation_text = "This is a conversation that includes several sentences."
    new_conversation = CM.create_conversation(user_name, conversation_text)
    


    print(f"New conversation created: {new_conversation}")


    ## Test 3 add label to sentence
    label = CM.add_label(s1.id, type='score', userid=1, score=5, text="This is a test label.")
    print(f"Label added to sentence: {label}")


    # init tables but not overwrite if already exist
