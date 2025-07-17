    
from typing import List, Literal, TypedDict

from agents.researcher.memory.research_topics import RelatedTopics

class InitialResearchState(TypedDict):
    query:str
                                                                                         
    research_from: Literal['WebSearch', 'KnowledgeBase' ]

    research_state: str
    human_feedback: str
    research_result: RelatedTopics                                                
    hallucination_score: bool
    research_reviewer_score: bool
    response_grader_score: bool
