from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from langchain.schema import AgentAction, AgentFinish
from typing import Union
import re

class CustomReActOutputParser(ReActSingleInputOutputParser):
    """Custom React output parser that handles JSON outputs better"""
    
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        """Parse the output from the agent"""
        try:
                                         
            return super().parse(text)
        except Exception as e:
                                                                                
            if self._is_json_response(text):
                                                                     
                return AgentFinish(
                    return_values={"output": text.strip()},
                    log=text
                )
            else:
                                                                             
                raise e
    
    def _is_json_response(self, text: str) -> bool:
        """Check if the text contains a valid JSON response"""
        import json
        
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            try:
                json.loads(json_match.group(1))
                return True
            except json.JSONDecodeError:
                pass
        
        json_match = re.search(r'\{.*?"topics".*?\}', text, re.DOTALL)
        if json_match:
            try:
                json.loads(json_match.group(0))
                return True
            except json.JSONDecodeError:
                pass
        
        return False
