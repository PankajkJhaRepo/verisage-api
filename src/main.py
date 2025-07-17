from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.orchestrator import router as orchestrator_router
from src.config.settings import settings

app = FastAPI(
    title="Verisage API",
    description="AI Research Orchestrator API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orchestrator_router, prefix="/api/v1", tags=["orchestrator"])

@app.get("/")
async def root():
    return {"message": "Welcome to Verisage API - AI Research Orchestrator"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
