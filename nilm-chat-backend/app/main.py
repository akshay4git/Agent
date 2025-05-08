from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.router import api_router
from app.config import settings
from app.database import engine, Base
from app.services.llm_service import llm_service


# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "documentation": "/docs",
    }

@app.on_event("startup")
async def startup_event():
    # Initialize the Flan-T5 model on startup
    if settings.LLM_PROVIDER == "flan-t5":
        print(f"Initializing Flan-T5 model: {settings.MODEL_NAME}")
        await llm_service.initialize_model()
        print("Model initialization complete")
        


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)