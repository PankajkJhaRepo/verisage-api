
from typing import Any, Dict
from agents.constants import HUMAN_FEEDBACK
from agents.researcher.deep_researcher.graph import init_deep_research_team
from agents.researcher.memory.researcher_state import ResearchState
from agents.researcher.initial_researcher.chains.initial_research_chain import RelatedTopics

from  .initial_researcher.graph import init_research_team
import datetime
from langgraph.checkpoint.memory import MemorySaver

class ResearchAgent:
    """A simple research agent that can gather information based on requests."""
    
    def __init__(self, websocket=None, stream_output=False, headers=None):
        print("Init ResearchAgent")
    
    async def run_initial_research(self,research_state: ResearchState):
        print("Running initial research...")
        task = research_state.get("task")
        query = task.get("query")
                                                 
        source = task.get("source", "web")
        task_id = task.get("task_id", "default-task-id")
        print(f"Running initial research on query: {query} with source: {source} and task_id: {task_id}")
                                                   
        research_report =  await self.get_research_report(query=query, task_id=task_id)
                                                                             
        print(f"Type of research report: {type(research_report)}")
        print(f"Task {task}")
        return {"task": task, "initial_research": research_report,
                "execution_status": "InitialResearch"}
    
    async def get_research_report(self,query: str, task_id:str):
                                   
        researcher_workflow  = init_research_team()
                                            
        memory = MemorySaver()
        researcher = researcher_workflow.compile(checkpointer=memory,interrupt_before=[HUMAN_FEEDBACK])
        researcher.get_graph().draw_mermaid_png(output_file_path="initial_researcher.png")

        thread = {"configurable":{"thread_id": task_id}}
        initial_input = {"query": query}
        response= await researcher.ainvoke(initial_input,thread)
        print("Response:", response)
        print(researcher.get_state(thread).next)
        while True:
                                                         
            user_input = "accept"                                     
            feedback = {HUMAN_FEEDBACK: user_input}
            response = researcher.update_state(thread,feedback,as_node=HUMAN_FEEDBACK)
            print("Response after feedback:", response)
            print(researcher.get_state(thread).next)
            print("Final state:", researcher.get_state(thread))
            response= await researcher.ainvoke(None,thread,)
            print("Response after second input:", response)
            if user_input.lower() == "accept":
                print("Feedback accepted, proceeding to next step.")
                break
        
        research_result = response["research_result"]
                                                                              
        return research_result;

    async def get_deep_research_report(self, task:dict,initial_research: RelatedTopics):
                                             
        query = task.get("query")
        source = task.get("source", "web")
        task_id = task.get("task_id", "default-task-id")
        print(f"Running deep research on query: {query} with source: {source} and task_id: {task_id}")
        
        try:
                                                             
            deep_researcher_workflow  = init_deep_research_team()

            memory = MemorySaver()
                                                                                                                       
            deep_researcher = deep_researcher_workflow.compile(checkpointer=memory)
            deep_researcher.get_graph().draw_mermaid_png(output_file_path="deep_researcher.png")
            print("Deep Researcher Workflow initialized.")
            
            researched_topics = []        
                                                                                                         
            thread = {"configurable":{"thread_id": f"{task_id}-deep"}}
            
            for i, topic in enumerate(initial_research.topics):
                print(f"Processing topic {i+1}/{len(initial_research.topics)}: {topic.topic}")
                                                    
                research_task: Dict[str, Any] = {
                    "query": query,
                    "source": source,
                    "task_id": f"{task_id}-topic-{i}",
                    "topic": topic
                }            
                
                deep_research_input = {
                    "task": research_task,
                    "research_from": "WebSearch",                 
                    "research_state": "Planning",
                    "human_feedback": "",
                    "research_result": RelatedTopics(topics=[]),                        
                    "hallucination_score": True,
                    "research_reviewer_score": True,
                    "response_grader_score": True
                }

                try:
                    response = await deep_researcher.ainvoke(deep_research_input, thread)
                    print(f"Deep research response for topic {i+1}: {type(response)}")
                    print(f"Response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
                    
                    if isinstance(response, dict) and 'research_result' in response and response['research_result']:
                        research_result = response['research_result']
                        if hasattr(research_result, 'topics') and research_result.topics:
                            researched_topics.extend(research_result.topics)
                            print(f"Added {len(research_result.topics)} topics from deep research")
                        else:
                            print(f"Research result has no topics, keeping original topic: {topic.topic}")
                            researched_topics.append(topic)
                    else:
                                                                        
                        researched_topics.append(topic)
                        print(f"No deep research result in response, keeping original topic: {topic.topic}")
                        
                except Exception as topic_error:
                    print(f"Error processing topic {i+1}: {topic_error}")
                    import traceback
                    traceback.print_exc()
                                                                    
                    researched_topics.append(topic)
            
            related_topics = RelatedTopics(topics=researched_topics)
            print(f"Deep research completed with {len(researched_topics)} total topics.")
            return related_topics
            
        except Exception as e:
            print(f"Error in deep research workflow: {e}")
            print("Falling back to initial research results...")
                                                                
            return initial_research
        
    async def run_parallel_deep_research(self, research_state: ResearchState):
                                                      
        print("Running parallel deep research...")
        task = research_state.get("task")
        print(f"Task in deep_research: {task}")
        
        try:
                                                                                                   
            if isinstance(task, dict) and "task" in task:
                actual_task = task["task"]                                     
            else:
                actual_task = task                                   
                
            query = actual_task.get("query") if actual_task else None
                                                     
            source = actual_task.get("source", "web") if actual_task else "web"
            task_id = actual_task.get("task_id", "default-task-id") if actual_task else "default-task-id"
            initial_research = research_state.get("initial_research", None)
            
            if not initial_research:
                print("❌ No initial research found in state!")
                return {"task": actual_task, "deep_research": RelatedTopics(topics=[]),
                        "execution_status": "DeepResearchFailed", "error": "No initial research data"}
            
            if not initial_research.topics:
                print("⚠️ No topics found in initial research!")
                return {"task": actual_task, "deep_research": RelatedTopics(topics=[]),
                        "execution_status": "DeepResearchSkipped", "error": "No topics to research"}
            
            print(f"📊 Starting deep research on {len(initial_research.topics)} topics...")
            
            deep_research_report = await self.get_deep_research_report(
                task=actual_task, initial_research=initial_research)
            
            print(f"📋 Deep research results:")
            for i, topic in enumerate(deep_research_report.topics, 1):
                print(f"  {i}. {topic.topic}")
                print(f"     Description: {topic.description[:100]}...")

            return {"task": actual_task, "deep_research": deep_research_report,
                    "execution_status": "DeepResearch"}
                    
        except Exception as e:
            print(f"❌ Error in deep research: {e}")
            import traceback
            traceback.print_exc()
            return {"task": actual_task if 'actual_task' in locals() else task, 
                    "deep_research": RelatedTopics(topics=[]),
                    "execution_status": "DeepResearchError", "error": str(e)}

if __name__ == "__main__":
                                                
    async def run_complete_research():
        agent = ResearchAgent()
        
        initial_state = {
            "task": {
                "query": "What is the advantage of AI and LLM in medical science ?", 
                "source": "web", 
                "verbose": True, 
                "task_id": "task-123"
            }
        }
        
        print("🔍 Starting Initial Research Phase...")
        initial_result = await agent.run_initial_research(initial_state)
        print(f"✅ Initial Research Completed!")
        print(f"Initial research status: {initial_result.get('execution_status')}")
        
        deep_research_state = {
            "task": initial_result["task"],
            "initial_research": initial_result["initial_research"],
            "execution_status": initial_result["execution_status"]
        }
        
        print("\n🔬 Starting Deep Research Phase...")
        deep_result = await agent.run_parallel_deep_research(deep_research_state)
        print(f"✅ Deep Research Completed!")
        print(f"Deep research status: {deep_result.get('execution_status')}")
        
        print("\n📊 Research Pipeline Summary:")
        print(f"Initial topics found: {len(initial_result['initial_research'].topics)}")
        print(f"Deep research topics: {len(deep_result['deep_research'].topics)}")
        
        return {
            "initial_research": initial_result,
            "deep_research": deep_result
        }
    
    import asyncio
    final_results = asyncio.run(run_complete_research())
