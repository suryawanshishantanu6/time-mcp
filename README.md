# time-mcp

A minimal agentic AI system that answers time-related and general questions using a tool-augmented LLM pipeline.

## Features
- **Flask API**: Provides the current timestamp.
- **MCP Agent Server**: Reasoning agent that detects user intent, calls tools (like the time API), engineers prompts, and interacts with an LLM via OpenRouter (OpenAI-compatible API).
- **Streamlit UI**: Simple chat interface to talk to the AI agent.

---

## Setup

### 1. Clone and Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variable
Set your OpenRouter API key (get one from https://openrouter.ai):
```bash
export OPENROUTER_API_KEY=sk-...your-key...
```

### 3. Run the Servers
Open three terminals (or use background processes):

#### Terminal 1: Flask Time API
```bash
python flask_api.py
```

#### Terminal 2: MCP Agent Server
```bash
python mcp_server.py
```

#### Terminal 3: Streamlit UI
```bash
streamlit run streamlit_ui.py
```

The Streamlit UI will open in your browser (default: http://localhost:8501)

---

## Usage
- Ask the agent any question in the Streamlit UI.
- If you ask about the time (e.g., "What is the time?"), the agent will call the Flask API, fetch the current time, and craft a beautiful, natural response using the LLM.
- For other questions, the agent will answer using the LLM only.

---

## Architecture
```
[Streamlit UI] → [MCP Agent Server] → [Tools (e.g., Time API)]
                            ↓
                        [LLM via OpenRouter]
```
- The MCP agent detects intent, calls tools as needed, engineers prompts, and sends them to the LLM.
- Easily extensible to add more tools (just add to the MCPAgent class).

---

## Customization
- **Add more tools**: Implement new methods in `MCPAgent` and update `self.tools`.
- **Improve intent detection**: Extend `detect_intent()` in `MCPAgent`.
- **Change LLM model**: Update the `model` field in `call_llm()`.

---

## Requirements
- Python 3.7+
- See `requirements.txt` for dependencies.

---

## Credits
- Built using Flask, Streamlit, OpenRouter, and Python.
- Inspired by agentic LLM design patterns.
