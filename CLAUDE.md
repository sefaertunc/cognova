# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AITestKit is an AI-powered test development toolkit that uses Claude API to:
- **Generate test code** from natural language descriptions (Claude Opus 4.5)
- **Analyze test failures** and suggest fixes (Claude Sonnet 4.5)
- **Validate prompt quality** through regression testing (Claude Haiku 4.5)

Core principle: AI generates, human reviews and approves. AI does not self-learn; humans improve prompts based on output.

**Important:** When working with the user on this project, provide guidance, suggestions, and architectural advice. The user implements code themselves - your role is to guide, not to write implementations unless explicitly requested.

## Quick Reference

```bash
# Install (Docker-based distribution)
curl -fsSL https://raw.githubusercontent.com/sefaertunc/aitestkit/main/scripts/install.sh | bash

# Development (local)
pip install -e ".[dev]"
pytest tests/ -v                    # Run tests
ruff check src/ tests/              # Lint
mypy src/                           # Type check
black src/ tests/                   # Format

# CLI (requires ANTHROPIC_API_KEY)
aitestkit init                               # Initialize project
aitestkit scenario init login.yaml           # Create scenario template
aitestkit scenario validate scenarios/*.yaml # Validate scenarios
aitestkit generate -s scenarios/login.yaml -f pytest  # Generate tests
aitestkit feedback approve tests/generated/test_login.py
aitestkit analyze ./failed_test.log
aitestkit regression --all
aitestkit frameworks --list                  # List supported frameworks
aitestkit memory search "login auth"         # Search past generations
aitestkit info                               # Show configuration
```

## Architecture

```
src/aitestkit/
├── cli.py                 # Click-based CLI entry point
├── config.py              # Pydantic configuration
├── errors.py              # Error definitions and exit codes
├── scenario/              # Scenario YAML handling
│   ├── loader.py          # Load and parse scenarios
│   ├── validator.py       # Three-tier validation
│   └── migrator.py        # Schema migration
├── generator/             # Test code generation (Opus 4.5)
│   └── scot.py            # SCoT prompting
├── analyzer/              # Failure analysis (Sonnet 4.5)
├── regression/            # Prompt regression testing (Haiku 4.5)
├── feedback/              # Feedback storage system
│   ├── storage.py         # Memvid + JSON fallback
│   └── patterns.py        # Pattern detection
├── memory/                # Semantic memory (Memvid)
│   ├── memvid_store.py    # Vector database
│   └── retrieval.py       # CEDAR-style retrieval
├── judge/                 # LLM-as-Judge validation
├── utils/claude_client.py # Anthropic API wrapper
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

## Commenting Strategy

**Core principle: Comments explain WHY, not WHAT.** If code needs a comment to explain what it does, refactor the code instead.

### What to Comment

| Type | When | Example |
|------|------|---------|
| Docstrings | Public APIs only | `"""Load scenario from YAML file."""` |
| Why comments | Non-obvious decisions, workarounds | `# Retry: API has transient failures` |
| Warnings | Gotchas, side effects | `# WARNING: Mutates input dict` |
| TODO/FIXME | With issue reference only | `# TODO(#42): Add retry logic` |

### What NOT to Comment

```python
# BAD - States the obvious
self.client = Anthropic()  # Create Anthropic client
if not api_key:  # Check if API key is missing
    raise ValueError("API key required")  # Raise error

# GOOD - Code is self-explanatory
self.client = Anthropic()
if not api_key:
    raise ValueError("API key required")
```

### Rules

1. **No obvious comments** - Don't describe what code does
2. **No inline comments on simple lines** - `x = 5  # Set x to 5` is noise
3. **No commented-out code** - Use git history
4. **Docstrings for public API only** - Private helpers rarely need them
5. **Update or delete** - Outdated comments are worse than none

## Git Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Formatting (no code change)
- `refactor` - Code restructuring (no feature/fix)
- `test` - Adding/updating tests
- `chore` - Maintenance tasks, dependencies

**Examples:**
```bash
feat(generator): add playwright framework support
fix(analyzer): handle empty log files gracefully
docs: update CLAUDE.md with commit conventions
refactor(cli): extract common options to decorator
test(regression): add benchmark scenarios for auth flows
chore: update anthropic dependency to 0.41.0
```

**Note:** Do not add `Co-Authored-By` lines to commit messages.

## Environment Variables

- `ANTHROPIC_API_KEY` - Required for Claude API access
- `AITESTKIT_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `AITESTKIT_MODEL_CODE_GEN` - Override code generation model
- `AITESTKIT_MODEL_ANALYSIS` - Override analysis model
- `AITESTKIT_MODEL_REGRESSION` - Override regression model

## Project Documentation

### Primary Specification

**[.dev-docs/MASTER_SPEC.md](.dev-docs/MASTER_SPEC.md)** - The single source of truth for the project (gitignored, local only).

This comprehensive document includes:
- Vision and mission statements
- Complete architecture overview
- Feature specifications (P0-P3 priorities)
- Implementation plan by phase
- Data schemas (JSON, YAML)
- CLI reference
- Prompt system design (CTCO framework)
- GitHub Actions workflows
- Testing strategy

### Feature Backlog

**[.dev-docs/BACKLOG.md](.dev-docs/BACKLOG.md)** - GitHub issue-style feature backlog extracted from MASTER_SPEC.md (gitignored, local only).

Track implementation progress for all 40 features across 4 priority levels (P0-P3).

### Implementation Guidance

**[.dev-docs/SKILL.md](.dev-docs/SKILL.md)** - Detailed implementation guidance (gitignored, local only).

This includes:
- Complete class structures and method signatures
- Architecture diagrams and data flows
- Prompt template content
- Testing patterns and mocking examples
- Implementation checklist by phase
- Debugging tips

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

### Session Content
- Decisions made with reasoning
- Key discussions and conclusions
- Alternatives considered and rejected
- Implementation progress
- Open questions and next steps

### Querying
Use `memvid search "query"` to find past context when needed.
