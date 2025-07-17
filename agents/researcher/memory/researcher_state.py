from typing import List, Dict, Any, TypedDict

from agents.researcher.memory.research_topics import RelatedTopics

class ResearchState(TypedDict):
    """
    Represents the state of a research .
    """
    task: dict
    initial_research: RelatedTopics                                                
    deep_research: RelatedTopics                                         
    execution_status: str                                                 