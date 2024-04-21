"""
Conversation manager
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from ai.model.conversation import Conversation, Sentence

# from ai.model.label import Label
# from ai.model.label import LabelSentence

from app.db.db import get_engine

DBHOST = os.getenv("DBHOST")
DBPASS = os.getenv("DBPASS")

engine = get_engine()


class ConversationManager:
    def __init__(self, sentences = []):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.sentences = sentences

    def create_conversation(self, user_name, conversation, role_info = None, notes=None):
        """Create a new conversation in the database."""
        new_conversation = Conversation(user_name=user_name, 
                        conversation=conversation,
                        role_info = role_info,
                         notes=notes)

        # add sentences to table
        for sentence in self.sentences:
            new_conversation.sentences.append(sentence)

        self.session.add(new_conversation)
        self.session.commit()
        return new_conversation

    def add_sentence(self, text, from_user = None,type=None, model=None, notes=None):
        """Add a sentence to the conversation.
        This is a temporary sentence that will be added to the conversation.
        Not saved to the database yet.
        """
        sentence = Sentence(from_user=from_user, text=text, type=type, model=model, notes=notes)
        self.sentences.append(sentence)
        return sentence

    def create_sentence(self, conversation_id = None, from_user = None, text = None, type=None, model=None, notes=None):
        """Create a new sentence in the database."""
        new_sentence = Sentence(conversation_id=conversation_id, from_user=from_user, text=text, type=type, model=model, notes=notes)
        self.session.add(new_sentence)
        self.session.commit()
        return new_sentence


    def get_sentence(self, sentence_id):
        """Get sentence by id."""
        return self.session.query(Sentence).filter(Sentence.id == sentence_id).first()

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
    def get_conversation(self, conversation_id, return_json=False):
        """Get conversation by id."""
        if return_json:
            return self.session.query(Conversation).filter(Conversation.id == conversation_id).first().to_dict()
        return self.session.query(Conversation).filter(Conversation.id == conversation_id).first()

    def list_conversations(self, return_json=False, limit = 100, desc = True):
        """List all conversations."""

        result = self.session.query(Conversation).order_by(Conversation.created_at.desc()).limit(limit).all()

        if return_json:
            # sort by id
            result.sort(key=lambda x: x.id, reverse=True)
            return [conversation.to_dict() for conversation in result]
        return result

    def list_active_conversations(self, return_json=False, limit = 20):
        """List all active conversations."""
        conversations = self.session.query(Conversation).filter(Conversation.deleted == 0).limit(limit).all()

        if return_json:
            return [conversation.to_dict() for conversation in conversations]
        return conversations

    def list_active_conversations_by_user(self, user_name, return_json=False, order = 'desc'):
        """List all deleted conversations by user.
        Only return the active conversations.
        Convesation only, not include sentences.
        """
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

    # Add label to conversation
    def add_label_conversation(self, conversation_id, label_from_user = None, label_score = None, label_text = None, notes = None):
        """Add label to conversation or sentences."""

        # update conversation with label
        conversation = self.session.query(Conversation).filter(Conversation.id == conversation_id).first()
        conversation.label_score = label_score
        conversation.label_text = label_text
        conversation.label_from_user = label_from_user
        conversation.label_created_at = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        self.session.commit()

        return conversation_id

    # Add label to sentences
    def add_label_sentence(self, sentence_id, label_score = 1, label_text = 'default label', label_from_user = None):
        """Add label to conversation or sentences."""

        # update sentence with label
        sentence = self.session.query(Sentence).filter(Sentence.id == sentence_id).first()
        sentence.label_score = label_score
        sentence.label_text = label_text
        sentence.label_from_user = label_from_user
        sentence.label_created_at = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        self.session.commit()

        return sentence_id




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
