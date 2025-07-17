from typing import Any, Dict
from agents.researcher.initial_researcher.memory.initial_research_state import InitialResearchState

class Response_Grader_Agent:
    """Agent responsible for grading responses to research questions."""
    
    def __init__(self):
                                                                  
        print("Response Grader Agent initialized.")
    
    def grade_response(self,state: InitialResearchState) -> Dict[str, Any]:
                                                       
        print("Running response grading...")
        query = state.get("query")
        research_result = state.get("research_result")

        return {
            "response_grader_score": True,                                        
        }