# AITestKit

AI-powered test generation toolkit — MCP server for IDE integration.

## What It Does

- Generates test code from YAML scenario descriptions using Claude AI
- Supports 25+ testing frameworks (pytest, Jest, JUnit, Playwright, Robot, etc.)
- Learns from feedback to improve output over time
- Repairs broken tests and self-heals after code changes

## Quick Start

Add to your IDE's MCP config:

```json
{
  "mcpServers": {
    "AITestKit": {
      "command": "uvx",
      "args": ["aitestkit-mcp@latest"],
      "env": { "ANTHROPIC_API_KEY": "sk-ant-..." }
    }
  }
}
```

Then ask your IDE agent: "Initialize AITestKit for this project"

## Requirements

- Python 3.11+
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com/settings/keys))

## License

MIT
