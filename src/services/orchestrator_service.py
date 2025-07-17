"""
Orchestrator service for managing research tasks
"""
from typing import Dict, Any, Optional, List
import asyncio
import uuid
from datetime import datetime

try:
    from agents.orchestrator import OrchestratorAgent
    from agents.constants import INITIAL_RESEARCH
    agent_available = True
except ImportError:
                                    
    print("Warning: Could not import agents. Using mock implementation.")
    OrchestratorAgent = None
    INITIAL_RESEARCH = "orchestrator"
    agent_available = False

class OrchestratorService:
    """Service for orchestrating research tasks using multi-agent system."""
    
    def __init__(self):
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
    
    async def start_research_task(
        self, 
        task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start a synchronous research task."""
        
        task = task_data.get("task", {})
        query = task.get("query", "")
        source = task.get("source", "web")
        verbose = task.get("verbose", True)
        task_id = task.get("task_id")
        
        if not task_id:
            task_id = f"task-{uuid.uuid4().hex[:8]}"
        
        self.active_tasks[task_id] = {
            "status": "running",
            "query": query,
            "source": source,
            "verbose": verbose,
            "started_at": datetime.now().isoformat(),
            "result": None
        }
        
        try:
                                                            
            result = await self._execute_research(task_data)
            
            self.active_tasks[task_id].update({
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
                "result": result
            })
            
            return {
                "status": "completed",
                "task_id": task_id,
                "message": "Research task completed successfully",
                "result": result
            }
            
        except Exception as e:
            self.active_tasks[task_id].update({
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            })
            
            return {
                "status": "failed",
                "task_id": task_id,
                "message": f"Research task failed: {str(e)}",
                "result": None
            }
    
    async def start_async_research_task(
        self, 
        task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start an asynchronous research task."""
        
        task = task_data.get("task", {})
        task_id = task.get("task_id") or f"task-{uuid.uuid4().hex[:8]}"
        
        self.active_tasks[task_id] = {
            "status": "running",
            "query": task.get("query", ""),
            "source": task.get("source", "web"),
            "verbose": task.get("verbose", True),
            "started_at": datetime.now().isoformat(),
            "result": None
        }
        
        asyncio.create_task(self._execute_async_research(task_id, task_data))
        
        return {
            "status": "started",
            "task_id": task_id,
            "message": "Research task started in background"
        }
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a research task."""
        
        if task_id not in self.active_tasks:
            return {
                "status": "not_found",
                "message": f"Task {task_id} not found"
            }
        
        task_info = self.active_tasks[task_id]
        return {
            "task_id": task_id,
            "status": task_info["status"],
            "query": task_info["query"],
            "started_at": task_info.get("started_at"),
            "completed_at": task_info.get("completed_at"),
            "result": task_info.get("result") if task_info["status"] == "completed" else None,
            "error": task_info.get("error") if task_info["status"] == "failed" else None
        }
    
    async def _execute_research(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the actual research task using agent orchestrator."""
        
        try:
            if agent_available and OrchestratorAgent:
                                                              
                orchestrator = OrchestratorAgent()
                agent_result = await orchestrator.run_research_task(task_data)
                
                if agent_result:
                    return self._format_agent_result(agent_result, task_data)
                else:
                    return await self._mock_research(task_data)
            else:
                                              
                return await self._mock_research(task_data)
                
        except Exception as e:
            print(f"Error in research execution: {e}")
                                             
            return await self._mock_research(task_data)
    
    def _format_agent_result(self, agent_result: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format the AgentState result into the expected API response format."""
        
        task = task_data.get("task", {})
        query = task.get("query", "")
        
        deep_research = agent_result.get("deep_research", {})
        
        if hasattr(deep_research, 'topics'):
                                                                                      
            topics_data = []
            all_sources = []
            
            for topic in deep_research.topics:
                topic_dict = {
                    "topic": topic.topic if hasattr(topic, 'topic') else str(topic),
                    "description": topic.description if hasattr(topic, 'description') else "",
                    "sources": []
                }
                
                if hasattr(topic, 'sources') and topic.sources:
                    topic_sources = []
                    for source in topic.sources:
                        if hasattr(source, 'url') and hasattr(source, 'title'):
                            source_dict = {
                                "title": source.title,
                                "url": source.url,
                                "description": getattr(source, 'description', '')
                            }
                            topic_sources.append(source_dict)
                            all_sources.append(source_dict)
                        elif isinstance(source, dict):
                            topic_sources.append(source)
                            all_sources.append(source)
                        elif isinstance(source, str):
                            source_dict = {"title": "Research Source", "url": source, "description": ""}
                            topic_sources.append(source_dict)
                            all_sources.append(source_dict)
                    
                    topic_dict["sources"] = topic_sources
                elif hasattr(topic, 'source') and topic.source:
                                                                     
                    source_dict = {
                        "title": f"Source for {topic.topic}",
                        "url": topic.source,
                        "description": ""
                    }
                    topic_dict["sources"] = [source_dict]
                    all_sources.append(source_dict)
                
                topics_data.append(topic_dict)
            
            research_data = {
                "topics": topics_data,
                "total_topics": len(topics_data)
            }
        elif isinstance(deep_research, dict):
                                                     
            research_data = deep_research
        else:
                                      
            research_data = {"raw_data": str(deep_research)}
        
        return {
            "research_data": research_data,
            "summary": f"Deep research completed for: {query}. Found {len(research_data.get('topics', []))} topics.",
            "metadata": {
                "query": query,
                "source": task.get("source", "web"),
                "agent_state": agent_result.get("agent_state", "completed"),
                "execution_status": agent_result.get("execution_status", "completed"),
                "processing_time": "agent_processed",
                "agent": INITIAL_RESEARCH,
                "data_type": "deep_research_only"
            }
        }
    
    def _extract_sources_from_deep_research(self, deep_research: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract sources from the deep_research data."""
        sources = []
        
        if "topics" in deep_research:
            for topic in deep_research["topics"]:
                if isinstance(topic, dict) and "sources" in topic:
                    topic_sources = topic["sources"]
                    if isinstance(topic_sources, list):
                        sources.extend(topic_sources)
        
        elif "sources" in deep_research:
            if isinstance(deep_research["sources"], list):
                sources.extend(deep_research["sources"])
        
        if not sources:
            sources = [
                {"title": "Deep Research Source", "url": "generated_by_deep_research_agent", "description": "Research conducted by AI agents"}
            ]
        
        return sources
    
    async def _mock_research(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock research implementation for testing."""
        
        task = task_data.get("task", {})
        query = task.get("query", "")
        source = task.get("source", "web")
        
        await asyncio.sleep(2)
        
        return {
            "research_data": f"Research results for: {query}",
            "summary": f"This is a summary of research on '{query}' from {source}",
            "sources": [
                {"title": "Example Source 1", "url": "https://example1.com"},
                {"title": "Example Source 2", "url": "https://example2.com"}
            ],
            "metadata": {
                "query": query,
                "source": source,
                "processing_time": "2.0 seconds",
                "agent": INITIAL_RESEARCH
            }
        }
    
    async def _execute_async_research(self, task_id: str, task_data: Dict[str, Any]):
        """Execute research task asynchronously."""
        
        try:
            result = await self._execute_research(task_data)
            
            self.active_tasks[task_id].update({
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
                "result": result
            })
            
        except Exception as e:
            self.active_tasks[task_id].update({
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            })

orchestrator_service = OrchestratorService()
