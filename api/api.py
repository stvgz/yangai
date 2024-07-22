"""API for managing the application."""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from ai.model.init_db import engine
from ai.model.conversation import Conversation
from ai.model.conversation import Sentence
from ai.conversation import ConversationManager

# API models
# from api.api_model import ConversationBase, ConversationCreate, ConversationDisplay
# from api.api_model import SentenceBase, SentenceCreate, SentenceDisplay

app = FastAPI()

# 允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，或者指定具体的域名，如 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，如["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],  # 允许所有headers
)

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
@app.get("/conversations/")
def read_conversations(skip: int = 0, limit: int = 100, including_deleted = False,
                db: Session = Depends(get_db()),
                order_type = 'desc',
                order_by = 'id'
                ):
    query = db.query(Conversation)
    # Correcting the order by clause
    if order_type == 'desc':
        order_clause = getattr(Conversation, order_by).desc()
    else:
        order_clause = getattr(Conversation, order_by)

    # TODO: add order by

    if including_deleted:
        query = query.order_by(order_clause).offset(skip).limit(limit)
    else:
        query = query.filter(Conversation.deleted == 0).order_by(order_clause).offset(skip).limit(limit)

    conversations = query.all()
    return conversations

# get conversation list with sentences
@app.get("/conversation-by-id/{conversation_id}")
def read_conversation(conversation_id: int, db: Session = Depends(get_db())):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

# get conversation list with sentences
@app.get("/conversation-by-id-with-sentences/{conversation_id}")
def read_conversation(conversation_id: int, db: Session = Depends(get_db())):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    sentences = db.query(Sentence).filter(Sentence.conversation_id == conversation_id).order_by(Sentence.id).all()
    conversation.sentences = sentences
    
    return conversation


# update label of conversation and all sentences
@app.post("/label-conversation/", )
def update_conversation_label(conversation_id: int, label_conversation: str, 
                            label_sentence: List[str], db: Session = Depends(get_db())):

    # 获得conversation_id
    conversation_id = conversation_id
    cm = ConversationManager()
    # get conversation
    conversation = cm.get_conversation(conversation_id, return_json=True)
    # get sentences
    sentences = cm.get_sentence_by_conversation(conversation_id, return_json=True)
    # remove 1st sentence
    sentences = sentences[1:]
    # update score of conversation
    cm.add_label_conversation(conversation_id,label_from_user=user_name, 
                            label_score= conversation_score, 
                            label_text= conversation_label_text)

    # update score of sentences
    for idx, s_id in enumerate(sentence_ids):
        
        sentence_score = score_sentence[idx]
        cm.add_label_sentence(sentence_id=s_id, label_score= sentence_score, label_from_user= user_name)
    
    score_finished_result = 1

    cm.close_session()

    return score_finished_result


class ConversationLabel(BaseModel):
    conversation_id: int
    label_score: int
    label_text: str
    user_name: str

# update label of conversation only, not sentences
@app.post("/label-conversation-only/")
def update_conversation_label(conversation_label: ConversationLabel, db: Session = Depends(get_db())):

    cm = ConversationManager()

    conversation_id = conversation_label.conversation_id
    label_score = conversation_label.label_score
    label_text = conversation_label.label_text
    user_name = conversation_label.user_name

    # get conversation
    conversation = cm.get_conversation(conversation_id, return_json=True)
    # update score of conversation
    cm.add_label_conversation(conversation_id, label_from_user=user_name, 
                            label_score=label_score, 
                            label_text=label_text)

    # score_finished_result = 1

    cm.close_session()

    return {"status": "success"}


class SentenceLabel(BaseModel):
    sentence_id: int
    label_score: int
    label_text: str


@app.post("/label-sentence/")
def update_sentence_label(sentence_label: SentenceLabel, db: Session = Depends(get_db())):
    print("Received data:", sentence_label)
    sentence = db.query(Sentence).filter(Sentence.id == sentence_label.sentence_id).first()
    if sentence is None:
        raise HTTPException(status_code=404, detail="Sentence not found")
    sentence.label_score = sentence_label.label_score
    sentence.label_text = sentence_label.label_text
    db.commit()

    return {"sentence_id": sentence_label.sentence_id, "label_score": sentence_label.label_score, "label_text": sentence_label.label_text}
# check status of api
@app.get("/")
def read_root():
    import datetime

    return {"status": "API is running at " + str(datetime.datetime.now())}




# run api with reload
# uvicorn api.api:app --reload