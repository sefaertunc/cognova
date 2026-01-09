# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AITestKit is an AI-powered test development toolkit that uses Claude API to:
- **Generate test code** from natural language descriptions (Claude Opus 4.5)
- **Analyze test failures** and suggest fixes (Claude Sonnet 4.5)
- **Validate prompt quality** through regression testing (Claude Haiku 4.5)

Core principle: AI generates, human reviews and approves. AI does not self-learn; humans improve prompts based on output.

## Quick Reference

```bash
# Install
pip install -e ".[dev]"

# Development
pytest tests/ -v                    # Run tests
ruff check src/ tests/              # Lint
mypy src/                           # Type check
black src/ tests/                   # Format

# CLI (requires ANTHROPIC_API_KEY)
aitestkit generate "Test scenario" -f pytest
aitestkit analyze ./failed_test.log
aitestkit regression --all
aitestkit info
```

## Architecture

```
src/aitestkit/
├── cli.py                 # Click-based CLI entry point
├── config.py              # Pydantic configuration
├── utils/claude_client.py # Anthropic API wrapper
├── generator/             # Test code generation (Opus 4.5)
├── analyzer/              # Failure analysis (Sonnet 4.5)
├── regression/            # Prompt regression testing (Haiku 4.5)
└── prompts/               # Prompt templates and benchmarks
```

## Model Configuration

| Task | Model | Model ID |
|------|-------|----------|
| Code generation | Opus 4.5 | claude-opus-4-5-20250514 |
| Failure analysis | Sonnet 4.5 | claude-sonnet-4-5-20250514 |
| Regression tests | Haiku 4.5 | claude-haiku-4-5-20250514 |

## Key Conventions

- Python 3.11+ required
- Line length: 100 characters (ruff, black)
- Type hints required (mypy strict mode)
- Test frameworks: pytest, Robot Framework, Playwright
- Generated code must NOT contain: `time.sleep`, `TODO`, `pass  #`

## Environment Variables

- `ANTHROPIC_API_KEY` - Required for Claude API access
- `AITESTKIT_PROMPTS_DIR` - Override prompts directory
- `AITESTKIT_OUTPUT_DIR` - Override output directory
- `AITESTKIT_DEFAULT_FRAMEWORK` - Default framework (pytest/robot/playwright)

## Detailed Implementation Guide

For comprehensive implementation specifications, code examples, and detailed module documentation, see:

**[docs/development/claude/SKILL.md](docs/development/claude/SKILL.md)**

This includes:
- Complete class structures and method signatures
- Architecture diagrams and data flows
- Prompt template content
- Testing patterns and mocking examples
- Implementation checklist by phase
- Debugging tips
