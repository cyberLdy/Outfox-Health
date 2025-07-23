from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

from app.database import get_db
from app.models import Provider, Procedure, Rating
from app.schemas import AskRequest, AskResponse
from app.prompts import SYSTEM_PROMPT
from app.utils.location import calculate_distance

load_dotenv()

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_sql_query(sql: str) -> str:
    """Remove markdown code blocks and clean SQL"""
    sql = re.sub(r'```sql\s*', '', sql)
    sql = re.sub(r'```\s*', '', sql)
    sql = sql.strip()
    return sql

# Add debugging to app/routers/ai_assistant.py in execute_with_location_filter

async def execute_with_location_filter(db: AsyncSession, sql: str, question: str):
    """Execute SQL and filter by distance if location is specified"""
    # Check for explicit distance
    explicit_distance = re.search(r'within (\d+) (?:miles|mi) of (\d{5})', question.lower())
    # Check for implicit distance (near ZIP)
    implicit_distance = re.search(r'near (\d{5})', question.lower())
    
    if explicit_distance:
        miles = float(explicit_distance.group(1))
        zip_code = explicit_distance.group(2)
        radius_km = miles * 1.60934
    elif implicit_distance:
        miles = 50  # Default 50 miles for "near [ZIP]"
        zip_code = implicit_distance.group(1)
        radius_km = miles * 1.60934
    else:
        # No location filter needed
        result = await db.execute(text(sql))
        return result.fetchall()
    
    print(f"📍 Filtering for locations within {miles} miles of {zip_code}")
    
    # Execute and filter by distance
    result = await db.execute(text(sql))
    all_rows = result.fetchall()
    
    print(f"📊 Got {len(all_rows)} rows from database")
    
    filtered_rows = []
    checked_count = 0
    for row in all_rows:
        # Find zip_code in row (it should be at index 3 based on SELECT order)
        provider_zip = row[3] if len(row) > 3 else None
        
        if provider_zip:
            distance = calculate_distance(zip_code, provider_zip)
            distance_miles = distance * 0.621371
            checked_count += 1
            
            if checked_count <= 5:  # Debug first 5
                print(f"  - {row[0]} ({provider_zip}): {distance_miles:.1f} miles")
            
            if distance <= radius_km:
                filtered_rows.append(row)
    
    print(f"✅ Filtered to {len(filtered_rows)} results within {miles} miles")
    
    return filtered_rows

def format_answer(question: str, rows: list, sql_query: str) -> str:
    """Format SQL results into natural language based on the question"""
    if not rows:
        return "No results found for your query."
    
    question_lower = question.lower()
    
    # For "cheapest" queries, always return single result
    if "cheapest" in question_lower or "who is cheapest" in question_lower:
        row = rows[0]  # Already sorted by price ascending
        
        # Find the price column (usually the largest number)
        price = None
        name = row[0]
        city = row[1] if len(row) > 1 else ""
        state = row[2] if len(row) > 2 else ""
        
        for val in row:
            try:
                num = float(val)
                if num > 1000:  # Likely a price
                    price = num
                    break
            except:
                continue
        
        if price:
            return f"Based on data, the cheapest hospital is {name} in {city}, {state} with an average covered charge of ${price:,.2f}"
        else:
            return f"Based on data, the cheapest hospital is {name} in {city}, {state}"
    
    # For other queries, format accordingly...
    # (rest of formatting logic)
    
    return "Based on data, " + str(rows[0])

@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    db: AsyncSession = Depends(get_db)
):
    """Natural language interface for healthcare queries"""
    
    try:
        # Get SQL from OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.question}
            ],
            max_tokens=200,
            temperature=0  # Set to 0 for most consistent results
        )
        
        sql_query = response.choices[0].message.content.strip()
        
        # Check if it's an out-of-scope response
        if "I can only help with" in sql_query:
            return AskResponse(
                answer="I can only help with hospital pricing and quality information. Please ask about medical procedures, costs, or hospital ratings.",
                sql_query=None
            )
        
        # Clean the SQL query
        clean_sql = clean_sql_query(sql_query)
        
        # Execute with location filtering if needed
        try:
            rows = await execute_with_location_filter(db, clean_sql, request.question)
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