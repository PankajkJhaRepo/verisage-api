from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from typing import Dict, Any, Union
import json

def SearchUsingTavilyEnhanced(search_input: Union[str, Dict[str, Any]]) -> str:
    """
    Enhanced search for topics using Tavily Search API with context and token management.
    
    Args:
        search_input: Can be either:
            - str: Simple topic string (backward compatibility)
            - dict: Enhanced input with query, topic, description, max_results, include_raw_content, etc.
    
    Returns:
        str: Search results from Tavily
    """
    load_dotenv()

    max_results = 3                                        
    include_raw_content = False                                            
    
    if isinstance(search_input, str):
        search_query = search_input
    elif isinstance(search_input, dict):
                                                     
        topic = search_input.get('topic', '')
        query = search_input.get('query', '')
        description = search_input.get('description', '')
        
        max_results = search_input.get('max_results', 3)
        include_raw_content = search_input.get('include_raw_content', False)
        
        search_parts = []
        
        if query:
            search_parts.append(f"Query: {query}")
        if topic:
            search_parts.append(f"Topic: {topic}")
        if description:
                                                                         
            desc_preview = description[:200] + "..." if len(description) > 200 else description
            search_parts.append(f"Context: {desc_preview}")
        
        search_query = " | ".join(search_parts) if search_parts else topic or query
    else:
                                             
        search_query = str(search_input)

    search = TavilySearchResults(
        max_results=max_results,                               
        include_answer=True,
        include_raw_content=include_raw_content,                                        
        include_images=False,
        search_depth="advanced",
                              
    )

    try:
        result = search.invoke({
            "args": {"query": search_query},
            "type": "tool_call", 
            "id": "enhanced_search", 
            "name": "tavily"
        })
        
        search_metadata = {
            "search_query_used": search_query,
            "original_input_type": type(search_input).__name__,
            "enhanced_search": isinstance(search_input, dict)
        }
        
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict):
                result[0]["_search_metadata"] = search_metadata
        
        return result
        
    except Exception as e:
        print(f"Error in enhanced Tavily search: {e}")
                                  
        basic_search = TavilySearchResults(max_results=5)
        return basic_search.invoke({
            "args": {"query": search_query},
            "type": "tool_call", 
            "id": "fallback_search", 
            "name": "tavily"
        })

def SearchUsingTavily(topic: str) -> str:
    """
    Original search function for backward compatibility.
    """
    return SearchUsingTavilyEnhanced(topic)
