# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# import datetime



# Base = declarative_base()


# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     user_name = Column(String(50), nullable=False)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     conversations = relationship("ai.model.conversation.Conversation", back_populates="user")

#     def __repr__(self):
#         return f"<User(id={self.id}, user_name={self.user_name}, created_at={self.created_at})>"

