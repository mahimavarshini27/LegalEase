import os

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    effective_date: str
    key_terms: str


@app.get("/")
def home():
    return {"message": "LegalEase Backend is Running!"}


@app.post("/generate")
def generate_document(request: DocumentRequest):

    prompt = f"""
You are an AI assistant helping users create legal document drafts.

Create a clear, structured draft for the following document:

Document Type: {request.document_type}
Parties: {request.parties}
Effective Date: {request.effective_date}
Key Terms: {request.key_terms}

Use professional legal-document formatting.
Include appropriate headings and clauses.
Do not invent personal details that were not provided.
Clearly state that the generated document should be reviewed
by a qualified legal professional before use.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return {
        "document": response.text
    }