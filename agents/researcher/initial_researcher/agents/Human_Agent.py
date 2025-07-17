from typing import Any, Dict
from agents.constants import HUMAN_FEEDBACK
from agents.researcher.initial_researcher.memory.initial_research_state import InitialResearchState

class HumanAgent:
    """Agent responsible for human feedback in the research process."""
    
    def __init__(self):
                                                                  
        print("Human Agent initialized.")
    
    def get_human_feedback(self,state: InitialResearchState) -> Dict[str, Any]:
                                                
        print("Running human feedback...")
                                              