from typing import List, Dict, Any, TypedDict, Optional

class AgentState(TypedDict, total=False):
    """
    Represents the state of a research workflow.
    """
    task: Dict[str, Any]
    agent_state: str                                                    
    initial_research: Any                                                                 
    deep_research: Dict[str, Any]                                         
    final_report: Dict[str, Any]                             
    human_feedback: Optional[Dict[str, Any]]                         
    publication_result: Optional[Dict[str, Any]]                       