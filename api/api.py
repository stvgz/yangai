"""API for managing the application."""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from ai.model.user import User
from ai.model.label import Label, LabelSentence
from ai.model.init_db import engine
from ai.model.conversation import Conversation

# API models
from api.api_model import ConversationBase, ConversationCreate, ConversationDisplay
from api.api_model import SentenceBase, SentenceCreate, SentenceDisplay

app = FastAPI()

# Dependency
def get_db():
    def _get_db():
        db = Session(bind=engine)
        try:
            yield db
        finally:
            db.close()
    
    return _get_db


# get conversation list
@app.get("/conversations/", response_model=List[ConversationDisplay])
def read_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db())):
    
        conversations = db.query(Conversation).offset(skip).limit(limit).all()
        return conversations

# get conversation list with sentences
@app.get("/conversations/{conversation_id}", response_model=ConversationDisplay)
def read_conversation(conversation_id: int, db: Session = Depends(get_db())):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

# get sentence of a conversation
@app.get("/conversations/{conversation_id}/sentences/", response_model=List[SentenceDisplay])
def read_sentences(conversation_id: int, db: Session = Depends(get_db())):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation.sentences


# check status of api
@app.get("/")
def read_root():
    import datetime

    return {"status": "API is running at " + str(datetime.datetime.now())}



# run api with reload
# uvicorn api.api:app --reload