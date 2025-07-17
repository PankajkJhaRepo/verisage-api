from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

def SearchUsingTavily(topic:str) -> str:
    """
    Search for any topic using Tavily Search API.
    """
    load_dotenv()

    search = TavilySearchResults(
        max_results=5,
        include_answer=True,
        include_raw_content=False,
        include_images=False,
        search_depth="advanced",
                              
    )

    result= search.invoke({"args":{"query":topic},"type": "tool_call", "id": "foo", "name": "tavily"})

    return result