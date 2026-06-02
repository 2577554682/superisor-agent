# Superisor Agent

A **multi-agent orchestration framework** built with LangChain and DeepSeek, featuring a hierarchical supervisor pattern that intelligently delegates tasks to specialized sub-agents.

## Overview

Superisor Agent implements a **Supervisor + Sub-agents** architecture:

- A **Supervisor Agent** acts as the central dispatcher, analyzing user intent and routing tasks
- **Specialized sub-agents** handle domain-specific operations (search, email, etc.)
- Sub-agents can use **MCP (Model Context Protocol) servers** to access external tools and data sources

The supervisor decides which sub-agent to invoke based on the context — for example, checking weather to decide whether to query train tickets, then composing and sending an appropriate email.

## Architecture

```
┌────────────────────────────────────────────┐
│           Supervisor Agent                 │
│  (Intent routing & task orchestration)     │
├────────────────┬───────────────────────────┤
│  Search Agent  │      Email Agent          │
│  (Bing / 12306 │  (QQ SMTP mailing)        │
│   via MCP)     │                           │
└────────────────┴───────────────────────────┘
```

### Layers

| Layer | Module | Responsibility |
|-------|--------|----------------|
| **LLM** | `my_llm.py` | LLM initialization (DeepSeek via LangChain) |
| **Config** | `config.py` | Centralized configuration from environment variables |
| **Tools** | `tools.py` | Atomic tools (email sending via SMTP) |
| **Agent Factory** | `agent_factory.py` | Creates sub-agents and the supervisor |
| **Stream Output** | `stream_output.py` | Streaming handler for agent output |
| **Entry** | `main.py` | Application entry point with async orchestration |

## Features

- **Multi-agent orchestration** — supervisor delegates to sub-agents based on intent
- **MCP integration** — connect to external MCP servers for search, data retrieval, etc.
- **Async streaming** — real-time streaming of agent reasoning and output
- **Tool calling** — pluggable tool layer (SMTP email, web search, 12306 train queries)
- **Environment-based config** — secrets managed via `.env`, never hardcoded

## Prerequisites

- Python 3.10+
- A [DeepSeek](https://platform.deepseek.com/) API key
- (Optional) A [ModelScope](https://www.modelscope.cn/) token for MCP server access
- (Optional) A QQ email account with SMTP service enabled for email sending

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/superisor-agent.git
cd superisor-agent
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```ini
# Required
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# Optional — for MCP server access
MODELSCOPE_TOKEN=your-modelscope-token

# Optional — for email sending (QQ SMTP)
SMTP_USER=your-email@qq.com
SMTP_PASS=your-smtp-authorization-code
```

> **Security:** The `.env` file is listed in `.gitignore` and **must never be committed**.

### 3. Run

```bash
python main.py
```

The demo will execute an example workflow:
1. Query today's weather for a city
2. Decide whether to retrieve train tickets based on the weather
3. Send an appropriate email notification

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | Yes | DeepSeek platform API key |
| `DEEPSEEK_BASE_URL` | Yes | DeepSeek API base URL |
| `MODELSCOPE_TOKEN` | No | Token for ModelScope-hosted MCP servers |
| `SMTP_USER` | No | QQ email address (for SMTP) |
| `SMTP_PASS` | No | QQ SMTP authorization code |

### Customizing MCP servers

Edit `config.py` to add or modify MCP server configurations:

```python
@classmethod
def get_mcp_config(cls) -> dict:
    return {
        "your-mcp-server": {
            "transport": "streamable_http",
            "url": "https://mcp.example.com/path",
            "headers": {"Authorization": f"Bearer {cls.YOUR_TOKEN}"},
        },
    }
```

## Project Structure

```
superisor_agent/
├── superisor_agent_demo/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── tools.py            # Atomic tools (email, etc.)
│   ├── agent_factory.py    # Agent builder (factory pattern)
│   ├── stream_output.py    # Streaming output handler
│   └── main.py             # Application entry point
├── env_utils.py            # Environment loader
├── my_llm.py               # LLM initialization
├── .env                    # Local secrets (gitignored)
├── .gitignore
└── README.md
```

## Extending

### Add a new tool

1. Define a `@tool` function in `tools.py`
2. Create a corresponding sub-agent in `agent_factory.py`
3. Register it with the supervisor

### Add an MCP server

1. Add the server config to `Config.get_mcp_config()` in `config.py`
2. The `MultiServerMCPClient` will load its tools automatically

## License

MIT
