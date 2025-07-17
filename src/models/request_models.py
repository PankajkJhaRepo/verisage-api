"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum

class SourceType(str, Enum):
    """Enum for research source types"""
    WEB = "web"
    INTERNAL = "internal"
    RAG = "rag"

class ResearchTaskRequest(BaseModel):
    """Request model for research tasks"""
    query: str = Field(..., description="The research query to process", min_length=1)
    source: SourceType = Field(default=SourceType.WEB, description="Source type for research")
    verbose: bool = Field(default=True, description="Enable verbose logging")
    task_id: Optional[str] = Field(default=None, description="Optional task identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the advantage of AI and LLM in medical science?",
                "source": "web",
                "verbose": True,
                "task_id": "task-123"
            }
        }

class ResearchTaskResponse(BaseModel):
    """Response model for research tasks"""
    status: str = Field(..., description="Task status")
    task_id: str = Field(..., description="Task identifier")
    message: str = Field(..., description="Status message")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Research results")
    
class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Error details")
    task_id: Optional[str] = Field(default=None, description="Task identifier if applicable")
