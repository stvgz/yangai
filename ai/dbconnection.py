
# attribute of Conversation
# 1. user_id
# 1. user_name
# 2. created_at


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

# temp code for importing
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from app.db.db import get_engine
engine = get_engine()

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DBHOST = os.getenv("DBHOST")
DBPASS = os.getenv("DBPASS")


# Database setup
# engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Assuming there's a User class defined somewhere that looks something like this:
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     conversations = relationship("Conversation", back_populates="user")


if __name__ == "__main__":
    # Create a new conversation
    # CM = ConversationManager()
    
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
    pass