
from typing import Any, Dict
from agents.researcher.deep_researcher.memory.deep_researcher_state import ResearchState

class Planner_Agent:
    """Agent responsible for planning the initial research."""
    
    def __init__(self):
                                                                  
        print("Planner Agent initialized.")

    def plan_research(self, state: ResearchState) -> Dict[str, Any]:
                                                  
        print("Planning research...")
        task = state.get("task")

        print(f"Task: {task}")

        return {
            "task": task,
        }
