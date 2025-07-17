
import asyncio
from langgraph.graph import StateGraph, END
import time
import datetime

from .human import HumanAgent
from .planner import PlannerAgent
from .publisher import PublisherAgent
from .researcher.research import ResearchAgent
from .writer import WriterAgent
from memory.agent_state import AgentState
                                   
class OrchestratorAgent:
    def __init__(self):
        """Agent responsible for managing and coordinating other agents."""
                                                       
    def _generate_task_id(self):
                                                                
        return int(time.time())
    
    def _initialize_agents(self):
        return {
            "writer": WriterAgent(),
            "planner": PlannerAgent(),
            "research": ResearchAgent(),
            "publisher": PublisherAgent(),
            "human": HumanAgent()
        }

    def init_research_team(self):
        """Initialize the research team with various agents."""
        agents = self._initialize_agents()
        return self._create_workflow(agents)
    
    def _create_workflow(self, agents):
        workflow = StateGraph(AgentState)

        workflow.add_node("researcher", agents["research"].run_initial_research)
        
        workflow.add_node("deep_researcher", agents["research"].run_parallel_deep_research)
        workflow.add_node("writer", agents["writer"].run)
        workflow.add_node("publisher", agents["publisher"].run)
        workflow.add_node("human", agents["human"].review_plan)

        self._add_workflow_edges(workflow)

        return workflow
    
    def _add_workflow_edges(self, workflow):
        workflow.add_edge('researcher', 'deep_researcher')
        
        workflow.add_edge('deep_researcher', 'writer')
        
        workflow.add_edge('writer', 'publisher')
        workflow.set_entry_point("researcher")
        workflow.add_edge('publisher', END)

    async def _log_research_start(self):
        message = f"Starting the research process for query '{self.task.get('query')}'..."
        print(message)

    async def run_research_task(self,state: AgentState):
        """Run a research task by coordinating with other agents."""
        research_team = self.init_research_team()
        app = research_team.compile()
                                                                               
        task = state.get("task", {})
        task_id = task.get("task_id", "default-task-id")

        config = {
            "configurable": {
                "thread_id": task_id
            }
        }
        print(f"Running research task with request: {state}")

        result = await app.ainvoke({"task": state}, config=config)
        print(f"Research task completed with result: {result}")
        return result

if __name__ == "__main__":
                                                   
    orchestrator = OrchestratorAgent()
    asyncio.run(orchestrator.run_research_task({"task": {"query": "What is the advantage of AI and LLM in medical science ?", "source": "web", "verbose": True, "task_id": "task-123"}}))
    print("Workflow created successfully.")
                                                                   