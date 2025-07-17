"""
Custom output parser for the React agent that can handle JSON responses
"""
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.exceptions import OutputParserException
import re
import json
from typing import Union
import logging

logger = logging.getLogger(__name__)

class FlexibleReActOutputParser(ReActSingleInputOutputParser):
    """
    Enhanced React output parser that can handle both standard React format 
    and direct JSON responses from the LLM
    """
    
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        """
        Parse the LLM output, handling both React format and direct JSON responses
        """
                                                
        json_response = self._extract_json_response(text)
        if json_response:
            logger.info("Found JSON response, treating as final answer")
            return AgentFinish(
                return_values={"output": json_response},
                log=text
            )
        
        try:
            return super().parse(text)
        except OutputParserException as e:
                                                                             
            if self._looks_like_final_answer(text):
                logger.info("Treating unparseable output as final answer")
                return AgentFinish(
                    return_values={"output": text},
                    log=text
                )
            else:
                                                 
                raise e
    
    def _extract_json_response(self, text: str) -> str:
        """
        Extract JSON response from text with flexible backtick handling
        """
                                                                             
        json_match = re.search(r'`{3,}json\s*(\{.*?\})\s*`{3,}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            if self._is_valid_json(json_str):
                logger.info("Found valid JSON in code blocks")
                return text                                                           
        
        json_match = re.search(r'`{3,}\s*(\{.*?"topics".*?\})\s*`{3,}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            if self._is_valid_json(json_str):
                logger.info("Found valid JSON in plain code blocks")
                return text
        
        json_match = re.search(r'\{[^{}]*"topics"[^{}]*\[[^\]]*\][^{}]*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            if self._is_valid_json(json_str):
                logger.info("Found valid JSON without code blocks")
                return text
        
        return None
    
    def _is_valid_json(self, json_str: str) -> bool:
        """
        Check if a string is valid JSON
        """
        try:
            parsed = json.loads(json_str.strip())
            return isinstance(parsed, dict) and "topics" in parsed
        except (json.JSONDecodeError, ValueError):
            return False
    
    def _looks_like_final_answer(self, text: str) -> bool:
        """
        Check if the text looks like a final answer (contains structured data)
        """
                                        
        has_json_structure = (
            '{' in text and '}' in text and 
            ('topics' in text or 'topic' in text)
        )
        
        has_research_content = any(keyword in text.lower() for keyword in [
            'description', 'source', 'research', 'study', 'analysis'
        ])
        
        return has_json_structure or has_research_content
