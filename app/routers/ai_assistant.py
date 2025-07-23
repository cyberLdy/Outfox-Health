from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

from app.database import get_db
from app.schemas import AskRequest, AskResponse
from app.prompts import SYSTEM_PROMPT

load_dotenv()

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_sql_query(sql: str) -> str:
    """Remove markdown code blocks and clean SQL"""
    # Remove ```sql and ``` markers
    sql = re.sub(r'```sql\s*', '', sql)
    sql = re.sub(r'```\s*', '', sql)
    # Remove any leading/trailing whitespace
    sql = sql.strip()
    return sql

def format_answer(question: str, rows: list, sql_query: str) -> str:
    """Format SQL results into natural language based on the question"""
    if not rows:
        return "No results found for your query."
    
    # Check question type
    question_lower = question.lower()
    
    # Check for "top N" pattern
    import re
    top_n_match = re.search(r'top (\d+)', question_lower)
    
    if top_n_match:
        # Handle "top N" queries
        n = int(top_n_match.group(1))
        answer = f"Here are the top {min(n, len(rows))} results:\n"
        for i, row in enumerate(rows[:n], 1):
            if "cheapest" in question_lower and len(row) >= 4:
                try:
                    price = float(row[3])
                    answer += f"{i}. {row[0]} in {row[1]}, {row[2]} - ${price:,.2f}\n"
                except:
                    answer += f"{i}. {row[0]} in {row[1]}, {row[2]}\n"
            else:
                answer += f"{i}. {row[0]} in {row[1]}, {row[2]}\n"
        return answer.strip()
    
    # Single result keywords
    single_result_keywords = ["the cheapest", "the most expensive", "the best", "the worst", "the highest", "the lowest"]
    is_single_result = any(keyword in question_lower for keyword in single_result_keywords)
    
    if is_single_result and len(rows) >= 1:
        # Format single result
        row = rows[0]
        if "cheapest" in question_lower:
            # Find the price column
            price = None
            for i in range(len(row)-1, -1, -1):
                try:
                    price = float(row[i])
                    if price > 1000:  # Likely a price, not a rating
                        break
                except (ValueError, TypeError):
                    continue
            
            if price:
                return f"The cheapest hospital is {row[0]} in {row[1]}, {row[2]} with an average covered charge of ${price:,.2f}"
            else:
                return f"The cheapest hospital is {row[0]} in {row[1]}, {row[2]}"
        elif "best rating" in question_lower:
            rating = row[-1] if len(row) > 3 else "N/A"
            return f"The hospital with the best rating is {row[0]} in {row[1]}, {row[2]} with a rating of {rating}/10"
        else:
            return f"Result: {row[0]} in {row[1]}, {row[2]}"
    else:
        # Multiple results without "top N"
        answer = f"Found {len(rows)} results. Here are the top 5:\n"
        for row in rows[:5]:
            answer += f"- {row[0]} in {row[1]}, {row[2]}\n"
    
    return answer.strip()

@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    db: AsyncSession = Depends(get_db)
):
    """Natural language interface for healthcare queries"""
    
    try:
        # Get SQL from OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
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
        
        # Clean the SQL query
        clean_sql = clean_sql_query(sql_query)
        
        # Execute the SQL query
        try:
            result = await db.execute(text(clean_sql))
            rows = result.fetchall()
            
            # Format answer based on question and results
            answer = format_answer(request.question, rows, clean_sql)
                        
        except Exception as db_error:
            answer = f"Database error: {str(db_error)}"
            
        return AskResponse(
            answer=answer,
            sql_query=clean_sql
        )
        
    except Exception as e:
        return AskResponse(
            answer=f"Error: {str(e)}",
            sql_query=None
        )