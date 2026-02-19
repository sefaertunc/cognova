# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Cognova is an MCP server for IDE integration that uses Claude API to:
- **Generate test code** from YAML scenarios (Sonnet 4.5 standard / Opus 4.6 high quality)
- **Analyze test failures** and suggest fixes (Sonnet 4.5)
- **Validate generated code** through deterministic rules + LLM-as-Judge (Haiku 4.5)
- **Repair broken tests** with context-aware fix loops (Sonnet/Opus)
- **Self-heal existing tests** after code changes (suggest mode default)

Core principle: AI generates, deterministic rules validate, humans approve.
Learning loop: auto-fix (count=1) → constraint injection (count≥3) → MAPS rule induction (count≥10). Human approval required at Tier 3.

**Important:** When working with the user on this project, provide guidance, suggestions, and architectural advice. The user implements code themselves.

## Quick Reference

### Installation (IDE Config)
```json
{
  "mcpServers": {
    "Cognova": {
      "command": "uvx",
      "args": ["cognova-mcp@latest"],
      "env": { "ANTHROPIC_API_KEY": "sk-ant-..." }
    }
  }
}
```

### Development (local)
```bash
pip install -e ".[dev]"
pytest .dev-tests/ -v
ruff check src/
mypy src/
```

## Architecture

```
src/cognova/
├── mcp_server.py              # FastMCP entry point (12 tools)
├── config.py                  # Pydantic configuration
├── errors.py                  # Error definitions
├── scenario/                  # Scenario YAML handling
│   ├── loader.py
│   ├── validator.py
│   └── migrator.py
├── context/                   # Project analysis (tree-sitter)
│   ├── analyzer.py            # Orchestrator
│   ├── parser.py              # tree-sitter parsing
│   ├── graph.py               # Dependency graph
│   └── hasher.py              # Structural hashing
├── generator/                 # Test generation
│   ├── generator.py           # Main pipeline
│   ├── context_builder.py     # Prompt context assembly
│   ├── scot.py                # SCoT reasoning
│   ├── edge_cases.py          # Edge-case generation
│   └── fault_guided.py        # Fault-guided generation (ACH)
├── rules/                     # Deterministic validation
│   ├── engine.py              # 3-layer rule engine
│   ├── validator.py           # Rule definitions
│   ├── learner.py             # 3-tier learning
│   └── default_rules.json     # Shipped rules
├── repair/                    # Test repair
│   ├── classifier.py          # Failure classification
│   └── repairer.py            # Repair loop (3 attempts, $0.50 cap)
├── healing/                   # Self-healing
│   ├── healer.py              # Suggest mode
│   └── auto_healer.py         # Auto mode (cosmetic only)
├── judge/                     # LLM-as-Judge (Haiku)
│   └── validator.py
├── analyzer/                  # Failure analysis (Sonnet)
│   └── analyzer.py            # Pipeline 8 (analyze_failure tool)
├── feedback/                  # Feedback storage
│   ├── storage.py             # LanceDB + JSON
│   ├── patterns.py            # Pattern detection
│   └── rejection_options.py   # Structured rejection options
├── memory/                    # Semantic memory
│   ├── lancedb_store.py       # Vector storage
│   ├── embeddings.py          # MiniLM + UniXcoder (local)
│   └── retrieval.py           # CEDAR retrieval
├── providers/                 # LLM provider abstraction
│   ├── base.py                # Protocol
│   ├── registry.py            # Provider registry
│   └── claude.py              # Claude implementation
├── regression/                # Prompt regression
│   └── regression.py          # Pipeline 7 (validate_prompt_change tool)
├── utils/
│   ├── cost_tracker.py        # Per-operation cost logging
│   └── update_checker.py      # PyPI version check
├── prompts/                   # Templates and benchmarks
├── queue.py                   # Generation queue (sequential gate)
└── web_server.py              # Web panel server (v4.1 planned, not implemented)
```

## Model Configuration

| Role | Default Model | High Quality | Cost (per MTok) |
|------|--------------|-------------|-----------------|
| Generation | Sonnet 4.5 | Opus 4.6 | $3/$15 or $5/$25 |
| Analysis | Sonnet 4.5 | — | $3/$15 |
| Validation | Haiku 4.5 | — | $1/$5 |

## Key Conventions

- Python 3.11+
- Line length: 100 (ruff, black)
- Type hints required (mypy strict)
- All source files are placeholders until implemented
- Tests in .dev-tests/ (unit/, integration/, manual/)
- ANTHROPIC_API_KEY is the only required env var
- No Docker, no CLI, no wrapper scripts
- MCP server is the only entry point
- v4.1 planned: Local web panel (localhost:8420) as visual companion to IDE MCP

## Commenting Strategy

**Core principle: Comments explain WHY, not WHAT.** If code needs a comment to explain what it does, refactor the code instead.

### What to Comment

| Type | When | Example |
|------|------|---------|
| Docstrings | Public APIs only | `"""Load scenario from YAML file."""` |
| Why comments | Non-obvious decisions, workarounds | `# Retry: API has transient failures` |
| Warnings | Gotchas, side effects | `# WARNING: Mutates input dict` |
| TODO/FIXME | With issue reference only | `# TODO(#42): Add retry logic` |

### Rules

1. **No obvious comments** - Don't describe what code does
2. **No inline comments on simple lines** - `x = 5  # Set x to 5` is noise
3. **No commented-out code** - Use git history
4. **Docstrings for public API only** - Private helpers rarely need them
5. **Update or delete** - Outdated comments are worse than none

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| ANTHROPIC_API_KEY | Yes | API key from console.anthropic.com |

## Testing

```bash
# Run all tests
pytest .dev-tests/ -v
```

**Hidden dev directories (gitignored):**
- `.dev-docs/` — Working documentation
- `.dev-memory/` — Development notes and context

## Git Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:** feat, fix, docs, style, refactor, test, chore

**Note:** Do not add `Co-Authored-By` lines to commit messages.

## Project Documentation

### Primary Specification

**[.dev-docs/MASTER_SPEC.md](.dev-docs/MASTER_SPEC.md)** - The single source of truth for the project (gitignored, local only).

### Feature Backlog

**[.dev-docs/BACKLOG.md](.dev-docs/BACKLOG.md)** - GitHub issue-style feature backlog (gitignored, local only).

### Implementation Guidance

**[.dev-docs/SKILL.md](.dev-docs/SKILL.md)** - Detailed implementation guidance (gitignored, local only).

## Development Workflow - Hat System

### Available Hats

| Hat | Trigger | Focus |
|-----|---------|-------|
| PM | "PM hat" | Task tracking, priorities, timeline, blockers |
| Guide | "guide me" | Implementation approach, structure, NO code writing |
| QA | "QA hat" | Critical review against MASTER_SPEC, find issues |
| Doc | "doc hat" | Documentation, guides, README updates |
| Debug | "stuck on" | Problem-solving, error analysis, unblocking |
| Architect | "architect hat" | System design, data flow, component relationships |
| Test | "test hat" | Test strategy, coverage, test case design |
| DevOps | "devops hat" | CI/CD, GitHub Actions, automation, deployment |
| Research | "research hat" | Compare options, explore approaches, analysis |

### Standard Workflow
PM -> Guide -> [User implements] -> QA -> PM

### Hat Rules
- Stay in role throughout interaction
- Guide hat provides approach only, never writes implementation code
- QA hat validates against MASTER_SPEC requirements
- All hats reference project documentation for consistency

## Dev Memory Protocol

### Location
`.dev-memory/` in project root (gitignored)

### Structure
```
.dev-memory/
├── sessions/      # Session summary files
├── decisions/     # Key decision records
├── memory.mv      # Memvid index
└── README.md      # Folder documentation
```

### Session Save Triggers
1. **Explicit**: User says "save session"
2. **Implicit**: Assistant offers at major breakpoints
