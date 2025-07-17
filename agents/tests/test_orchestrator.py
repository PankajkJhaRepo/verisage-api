import sys
import os
from pathlib import Path
import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agents.orchestrator import OrchestratorAgent

@pytest.fixture
def orchestrator_request() -> Dict[str, Any]:
    """Fixture to create a sample request"""
    return {
        "task_id": "test-123",
        "query": "Write a summary about AI",
        "max_sections": 3,
        "publish_format": "markdown",
        "include_human_feedback": False,
        "follow_guidelines": True,
        "model": "gpt-4",
        "guidelines": ["Keep it simple", "Be concise"],
        "verbose": True
    }

@pytest.fixture
def orchestrator():
    """Fixture to create an OrchestratorAgent instance"""
    return OrchestratorAgent()

def test_orchestrator_initialization(orchestrator):
    """Test if orchestrator is initialized correctly"""
    assert isinstance(orchestrator, OrchestratorAgent)

def test_generate_task_id(orchestrator):
    """Test if task_id is generated correctly"""
    task_id = orchestrator._generate_task_id()
    assert isinstance(task_id, int)
    assert task_id > 0

def test_initialize_agents(orchestrator):
    """Test if agents are initialized correctly"""
    agents = orchestrator._initialize_agents()
    expected_agents = ["writer", "planner", "research", "publisher", "human"]
    assert all(agent in agents for agent in expected_agents)
    assert len(agents) == len(expected_agents)

def test_init_research_team(orchestrator):
    """Test if research team workflow is created correctly"""
    workflow = orchestrator.init_research_team()
    assert workflow is not None
                                                  
    expected_nodes = ["researcher", "deep_researcher", "writer", "publisher", "human"]
    actual_nodes = list(workflow.nodes.keys())
    print(f"Expected nodes: {expected_nodes}")
    print(f"Actual nodes: {actual_nodes}")
    assert all(node in workflow.nodes for node in expected_nodes)
