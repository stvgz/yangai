
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain.embeddings import OpenAIEmbeddings
# Load environment variables from .env file
load_dotenv(override=True)
# Set up MongoDB connection details
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# MONGO_URI = os.environ["MONGO_URI"]
MONGO_URI = os.environ["MONGO_URI"]
DB_NAME = "pdfchatbot"
COLLECTION_NAME = "advancedRAGParentChild"


# Initialize OpenAIEmbeddings with the API key
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)


# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]