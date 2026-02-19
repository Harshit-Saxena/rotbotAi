# rotbot

**The open agent framework for every platform.**

rotbot is an ultra-lightweight AI agent framework inspired by [nanobot](https://github.com/HKUDS/nanobot). It delivers full agent capabilities — multi-platform chat, tool calling, RAG, persistent memory, and MCP support — in a clean, extensible architecture.

## Key Features

- **Multi-Platform**: Discord, Telegram, Signal, CLI — one agent, every platform
- **BYOK (Bring Your Own Key)**: Ollama (free, local) + OpenAI, Claude, Gemini, DeepSeek, Groq, OpenRouter, and any OpenAI-compatible API
- **Agent Loop**: Unified Perceive-Think-Act architecture with bounded iteration
- **Tool System**: Built-in tools + MCP protocol for external tool servers
- **RAG**: Lightweight retrieval-augmented generation with BM25 search (no vector DB needed)
- **Persistent Memory**: JSONL sessions, MEMORY.md for long-term facts, auto-consolidation
- **Skills**: Dynamic markdown-based skills, on-demand loading
- **Security**: 5-layer guardrails (input/output filtering, content safety, operational security)
- **Pip Installable**: `pip install rotbot-ai`

## Quick Start

### 1. Install

```bash
pip install rotbot-ai

# Or from source
git clone https://github.com/rotbot-ai/rotbot.git
cd rotbot-ai
pip install -e .
```

### 2. Setup

```bash
rotbot onboard
```

### 3. Chat

```bash
rotbot agent
```

That's it! You have a working AI assistant.

## Configuration

Config file: `~/.rotbot/config.json`

### Set your provider

**Ollama (free, local):**
```json
{
  "providers": {
    "ollama": {
      "base_url": "http://localhost:11434",
      "default_model": "llama3.1:8b"
    }
  }
}
```

**OpenAI:**
```json
{
  "providers": {
    "openai": {
      "apiKey": "sk-xxx",
      "default_model": "gpt-4o"
    }
  }
}
```

**Claude (Anthropic):**
```json
{
  "providers": {
    "anthropic": {
      "apiKey": "sk-ant-xxx",
      "default_model": "claude-sonnet-4-5-20250929"
    }
  }
}
```

**Gemini (Google):**
```json
{
  "providers": {
    "gemini": {
      "apiKey": "AIza-xxx",
      "default_model": "gemini-2.0-flash"
    }
  }
}
```

Or use `rotbot provider add` for interactive setup.

## Chat Channels

| Channel | What you need |
|---------|--------------|
| CLI | Nothing (built-in) |
| Discord | Bot token + Message Content intent |
| Telegram | Bot token from @BotFather |
| Signal | signal-cli daemon on port 7583 |

```bash
# Install channel dependencies
pip install rotbot-ai[discord]    # Discord
pip install rotbot-ai[telegram]   # Telegram
pip install rotbot-ai[all]        # Everything
```

Enable channels in config.json, then:

```bash
rotbot gateway    # Start all enabled channels
```

## MCP Support

Connect external tool servers via Model Context Protocol:

```json
{
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
      }
    }
  }
}
```

## RAG (Knowledge Base)

rotbot includes a lightweight RAG system with BM25 keyword search:

```python
from rotbot.core.rag import RAGStore

store = RAGStore(collection="docs")
store.ingest_file("knowledge.pdf")
store.ingest_directory("./docs/", extensions=[".md", ".txt"])

results = store.search("how to deploy")
context = store.build_context("deployment steps")
```

## Architecture

```
rotbot/
├── core/          # Agent loop, message bus, sessions, memory, config, RAG
├── providers/     # LLM backends (Ollama, OpenAI-compatible BYOK)
├── channels/      # Platform adapters (CLI, Discord, Telegram, Signal)
├── tools/         # Built-in tools + MCP client
├── shared/        # Security guardrails, context analyzer, think parser
├── skills/        # Dynamic markdown-based skills
├── cron/          # Scheduled tasks
└── cli/           # CLI commands (onboard, agent, gateway, provider, status)
```

### Message Flow

```
User → Channel → MessageBus → AgentLoop
  → Build Context (memory + skills + tools)
  → Call LLM Provider (streaming)
  → Execute Tools (if needed, bounded iteration)
  → Guardrails Filter
  → MessageBus → Channel → User
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `rotbot onboard` | Interactive setup wizard |
| `rotbot agent` | CLI chat mode |
| `rotbot agent -m "..."` | Single message mode |
| `rotbot gateway` | Start all enabled channels |
| `rotbot provider add` | Add a provider interactively |
| `rotbot provider list` | List configured providers |
| `rotbot status` | Show system status |

## Chat Commands

| Command | Description |
|---------|-------------|
| `/chat` | General mode |
| `/coder` | Coding mode |
| `/think` | Reasoning mode (with `<think>` tags) |
| `/reset` | Clear conversation |
| `/setmodel <name>` | Set custom model |
| `/model` | Show current model |
| `/deepthink` | Toggle reasoning display |
| `/help` | Show help |

## License

MIT
