import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Testing OpenAI API...")

try:
    # Simple test completion
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, the API is working!' in exactly those words."}
        ],
        max_tokens=50
    )
    
    print("✅ API Key is valid!")
    print(f"Response: {response.choices[0].message.content}")
    print(f"Model used: {response.model}")
    print(f"Tokens used: {response.usage.total_tokens}")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {str(e)}")