from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import providers, ai_assistant  # Add ai_assistant

app = FastAPI(title="Healthcare Cost Navigator")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Healthcare Cost Navigator API", "endpoints": ["/providers", "/ask"]}

# Include routers
app.include_router(providers.router)
app.include_router(ai_assistant.router)  # Add this line