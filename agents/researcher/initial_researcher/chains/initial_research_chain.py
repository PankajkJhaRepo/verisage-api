from dotenv import load_dotenv
import os
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from agents.researcher.initial_researcher.tools.tavily_search import SearchUsingTavily
from langchain import hub
from langchain.agents import (create_react_agent, Tool, AgentExecutor)
from langchain_core.runnables import RunnableLambda
from agents.researcher.memory.research_topics import RelatedTopics, Topic

def format_prompt_for_agent(inputs):
    """Format the topic into the prompt template and prepare for agent executor"""
    topic = inputs["topic"]
    history = inputs.get("history", None)
    
    if history is not None:
        formatted_prompt = prompt_template.format_prompt(topic=topic, history=str(history)).to_string()
                                                             
        agent_input = f"""Research Topic: {topic}

            Previous Research Context:
            {history}

            Task: {formatted_prompt}

            Please use the available tools to find comprehensive information, considering the previous research context."""
    else:
        formatted_prompt = prompt_template.format_prompt(topic=topic, history="No previous research history available.").to_string()
                            
        agent_input = f"""Research Topic: {topic}

        Task: {formatted_prompt}

        Please use the available tools to find comprehensive information."""
            
    return {"input": agent_input}

def parse_agent_response(response):
    """Parse the agent response and convert to RelatedTopics object"""
    import json
    import re
    
    output_text = response.get("output", "")
    
    try:
                                                              
        json_patterns = [
            r'```json\s*(\{.*?\})\s*```',                       
            r'```\s*(\{.*?\})\s*```',                                 
            r'(\{[^{}]*"topics"[^{}]*\[[^\]]*\][^{}]*\})',                                 
            r'\{.*?\}',                                              
        ]
        
        json_str = None
        for pattern in json_patterns:
            json_match = re.search(pattern, output_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                break
        
        if not json_str:
            print(f"No JSON found in response: {output_text[:200]}...")
            return RelatedTopics(topics=[])
        
        json_str = json_str.strip()
        
        json_str = re.sub(r',\s*}', '}', json_str)                          
        json_str = re.sub(r',\s*]', ']', json_str)                                    
        
        parsed_data = json.loads(json_str)
        
        if "topics" not in parsed_data:
            print("No 'topics' key found in parsed data")
            return RelatedTopics(topics=[])
        
        valid_topics = []
        for topic in parsed_data["topics"]:
            if isinstance(topic, dict) and all(key in topic for key in ["topic", "description", "source"]):
                valid_topics.append(Topic(**topic))
            else:
                print(f"Invalid topic format: {topic}")
        
        return RelatedTopics(topics=valid_topics)
        
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"Error parsing agent response: {e}")
        print(f"Response content: {output_text[:500]}...")
                                             
        return RelatedTopics(topics=[])

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY');
OPENAI_API_BASEURL = os.getenv('OPENAI_API_BASE');
OPENAI_MODEL = os.getenv('LLM_MODEL');

llm = ChatOpenAI(
    model_name=OPENAI_MODEL,
    openai_api_key= OPENAI_API_KEY,
    openai_api_base= OPENAI_API_BASEURL,
    temperature=0.0,                                                 
)

template = """Given the topic {topic}, generate a list of related topics with a brief description and source for each topic.

Previous research context (if available):
{history}

Use both web search tools and historical research tools to find comprehensive information.

Return the result in the following format:
    ```json
    {{
        "topics": [
            {{
                "topic": "<related topic>",
                "description": "<brief description of the related topic>",
                "source": "<source of the information>"
            }},
            ...
        ]
    }}
    ```"""

prompt_template = PromptTemplate(
        input_variables=["topic", "history"],
        template=template
        )

def search_historical_data(query: str) -> str:
    """Search through historical research data"""
                                                                                
    return f"Historical search for '{query}': No previous research found on this topic."

tools_for_agent = [
    Tool(
        name="Crawl Google for Related Topics",
        func=SearchUsingTavily,
        description="useful for when you need to find related topics on the web. Input should be a topic string.",
    ),
    Tool(
        name="Search Historical Research",
        func=search_historical_data,
        description="useful for searching through previous research results and historical data. Input should be a search query string.",
    )
]

react_prompt = hub.pull("hwchase17/react")

agent = create_react_agent(
    llm=llm,
    tools=tools_for_agent,
    prompt=react_prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools_for_agent, 
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
    early_stopping_method="generate"
)

research_chain = (
    RunnableLambda(format_prompt_for_agent) 
    | agent_executor
    | RunnableLambda(parse_agent_response)
)
