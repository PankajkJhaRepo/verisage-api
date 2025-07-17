from typing import Any, Dict
from pydantic import BaseModel
from agents.researcher.initial_researcher.memory.initial_research_state import InitialResearchState
from agents.researcher.initial_researcher.chains.initial_research_chain import RelatedTopics

class InitialPlannerAgent:
    """Agent responsible for planning the initial research."""
    
    def __init__(self):
                                                                  
        print("Initial Planner Agent initialized.")
    
    def plan_initial_research(self, state: InitialResearchState) -> Dict[str, Any]:
                                                  
        print("Planning initial research...")
        query = state.get("query")
        research_result = state.get("research_result")
        print(f"Query: {query}")
        print(f"Research Result: {research_result}")

        return {
            "research_result": research_result,
            "research_state": "InitialPlanner",
        }