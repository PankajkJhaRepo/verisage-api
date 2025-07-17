# Verisage API

AI Research Orchestrator API for multi-agent research tasks.

## Project Structure

```
verisage-api/
+-- src/
�   +-- main.py                 # FastAPI application entry point
�   +-- api/
�   �   +-- routes/
�   �       +-- orchestrator.py # API endpoints for research tasks
�   +-- models/
�   �   +-- request_models.py   # Pydantic models for requests/responses
�   +-- services/
�   �   +-- orchestrator_service.py # Business logic for orchestrator
�   +-- config/
�       +-- settings.py         # Application configuration
+-- agents/                     # Multi-agent system (copied from MultiAgent)
+-- memory/                     # Shared memory modules
+-- requirements.txt            # Python dependencies
+-- README.md                  # This file
```

## API Endpoints

### POST /api/v1/research
Start a research task with the orchestrator agent.

**Request Body:**
```json
{
    "query": "What is the advantage of AI and LLM in medical science?",
    "source": "web",
    "verbose": true,
    "task_id": "task-123"
}
```

**Response:**
```json
{
    "status": "completed",
    "task_id": "task-123",
    "message": "Research task completed successfully",
    "result": {
        "research_data": "...",
        "summary": "...",
        "sources": []
    }
}
```

### GET /api/v1/research/{task_id}/status
Get the status of a research task.

### POST /api/v1/research/async
Start a research task asynchronously in the background.

## Installation

python -m pip install virtualenv
python.exe -m pip install --upgrade pip

python -m virtualenv verisage

.\verisage\Scripts\activate
python -m pip install -r .\requirements.txt
pip install --no-cache-dir -r requirements.txt

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API:
```bash
cd src
python main.py

python -m src.main
```

3. Test the API:
```bash

python -m pytest . -s -v --tb=short
```

The API will be available at `http://localhost:8000`

## Usage Example

```bash
curl -X POST "http://localhost:8000/api/v1/research" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is the advantage of AI and LLM in medical science?",
       "source": "web",
       "verbose": true
     }'
```

## Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
