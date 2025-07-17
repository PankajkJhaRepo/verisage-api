"""
API routes for orchestrator endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import uuid
import asyncio
from typing import Dict, Any

from src.models.request_models import ResearchTaskRequest, ResearchTaskResponse, ErrorResponse
from src.services.orchestrator_service import OrchestratorService

router = APIRouter()
orchestrator_service = OrchestratorService()

@router.post(
    "/research",
    response_model=ResearchTaskResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Start a research task",
    description="Submit a research query to be processed by the orchestrator agent"
)
async def start_research_task(request: ResearchTaskRequest) -> ResearchTaskResponse:
    """
    Start a new research task with the orchestrator agent.
    
    - **query**: The research question to investigate
    - **source**: Source type for research (web, internal, rag)
    - **verbose**: Enable detailed logging
    - **task_id**: Optional custom task identifier
    """
    try:
                                          
        if not request.task_id:
            request.task_id = f"task-{uuid.uuid4()}"
        
        task_data = {
            "task": {
                "query": request.query,
                "source": request.source,
                "verbose": request.verbose,
                "task_id": request.task_id
            }
        }
        
        result = await orchestrator_service.start_research_task(task_data)
        
        return ResearchTaskResponse(
            status=result["status"],
            task_id=result["task_id"],
            message=result["message"],
            result=result.get("result")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process research task: {str(e)}"
        )

@router.get(
    "/research/{task_id}/status",
    response_model=Dict[str, Any],
    summary="Get research task status",
    description="Get the status of a research task by task ID"
)
async def get_task_status(task_id: str):
    """
    Get the status of a research task.
    
    - **task_id**: The task identifier
    """
    try:
        status = orchestrator_service.get_task_status(task_id)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found or error retrieving status: {str(e)}"
        )

@router.post(
    "/research/async",
    response_model=Dict[str, str],
    summary="Start asynchronous research task",
    description="Submit a research task to run in the background"
)
async def start_async_research_task(
    request: ResearchTaskRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """
    Start a research task asynchronously in the background.
    
    - **query**: The research question to investigate
    - **source**: Source type for research (web, internal, rag)
    - **verbose**: Enable detailed logging
    - **task_id**: Optional custom task identifier
    """
    try:
                                          
        if not request.task_id:
            request.task_id = f"task-{uuid.uuid4()}"
        
        task_data = {
            "task": {
                "query": request.query,
                "source": request.source,
                "verbose": request.verbose,
                "task_id": request.task_id
            }
        }
        
        result = await orchestrator_service.start_async_research_task(task_data)
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start background research task: {str(e)}"
        )
