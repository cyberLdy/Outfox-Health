from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import os
from openai import OpenAI
from dotenv import load_dotenv

from app.database import get_db
from app.schemas import AskRequest, AskResponse
from app.prompts import SYSTEM_PROMPT

load_dotenv()

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    db: AsyncSession = Depends(get_db)
):
    """Natural language interface for healthcare queries"""
    
    try:
        # Get SQL from OpenAI
        response = client.chat.completions.create(
            model="gpt-4.1-nano",  # Changed to nano model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.question}
            ],
            max_tokens=200
        )
        
        sql_query = response.choices[0].message.content.strip()
        
        # Check if it's an out-of-scope response
        if "I can only help with" in sql_query:
            return AskResponse(
                answer=sql_query,
                sql_query=None
            )
        
        # For now, return the generated SQL
        return AskResponse(
            answer=f"Generated SQL: {sql_query}",
            sql_query=sql_query
        )
        
    except Exception as e:
        return AskResponse(
            answer=f"Error: {str(e)}",
            sql_query=None
        )