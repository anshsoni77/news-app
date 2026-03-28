from dotenv import load_dotenv
import os

load_dotenv()

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()  # Load from .env

import os
embedding = OpenAIEmbeddings(openai_api_key="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")
db = Chroma(embedding_function=embedding, persist_directory="./chroma_db")

def add_to_db(title, text):
    doc = Document(page_content=text, metadata={"title": title})
    db.add_documents([doc])
    db.persist()

def get_similar_articles(query, k=3):
    return db.similarity_search(query, k=k)
