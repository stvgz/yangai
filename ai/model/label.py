# # Label of conversation
# # for customers: if the customer looks like a real customer
# # for user: if he/she acting like a great user


# from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
# from sqlalchemy.orm import relationship
# from .conversation import Conversation, Sentence
# # from .sentence import Sentence
# import datetime

# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()


# class Label(Base):
#     """Label on conversation"""
#     __tablename__ = 'label'
#     id = Column(Integer, primary_key=True)

#     type = Column(String(50), nullable=True)
#     userid = Column(Integer, ForeignKey('user.id'), nullable=True)
#     conversation_id = Column(Integer, ForeignKey('conversation.id'))
#     label_score = Column(Integer)
#     label_content = Column(String)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
#     notes = Column(Text, nullable=True)


# class LabelSentence(Base):
#     """Label on sentence"""
#     __tablename__ = 'label_sentence'

#     id = Column(Integer, primary_key=True)
#     sentence_id = Column(Integer, ForeignKey('sentence.id'), nullable=True)
#     label_score = Column(Integer)
#     label_content = Column(String)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
#     notes = Column(Text, nullable=True)