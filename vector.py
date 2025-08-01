import os
import glob
import google.generativeai as genai
from sqlalchemy import create_engine, Column, Integer, Text, String
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "AIzaSyAdPm4YOGSz01SEqJHJ5nA33lTWOizxhQ4")

# ✅ PostgreSQL connection (adjust as needed)
DATABASE_URL = "postgresql://guardrails_usr:asdfasdf@34.143.247.40:5432/guardrails_vec_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# ✅ Define SQLAlchemy model
Base = declarative_base()

class SentenceEmbedding(Base):
    __tablename__ = "expo_table2"
    id = Column(Integer, primary_key=True)
    filename = Column(String)           # Optional: save filename
    text = Column(Text)
    embedding = Column(Vector(768))     # Gemini 004 returns 768-dimensional vectors

# Create table if it doesn't exist
Base.metadata.create_all(bind=engine)

# ✅ Gather all markdown files
file_paths = glob.glob("prompt_*.md")
file_contents = []

for path in file_paths:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:  # Skip empty files
            file_contents.append((path, content))

if not file_contents:
    print("⚠️ No non-empty prompt_*.md files found.")
    exit()

# ✅ Embed using Gemini TextEmbedding-004
response = genai.embed_content(
     model="models/embedding-001",  # ✅ CORRECT
    content=[text for _, text in file_contents],
    task_type="retrieval_document"  # "retrieval_query" for queries
)

embeddings = response["embedding"]

# ✅ Store results in DB
for (filename, content), vector in zip(file_contents, embeddings):
    row = SentenceEmbedding(
        filename=filename,
        text=content,
        embedding=vector
    )
    session.add(row)

session.commit()
session.close()

print(f"✅ Stored {len(file_contents)} embedded files into PostgreSQL.")
