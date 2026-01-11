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

## Environment Variables

- `ANTHROPIC_API_KEY` - Required for Claude API access
- `AITESTKIT_PROMPTS_DIR` - Override prompts directory
- `AITESTKIT_OUTPUT_DIR` - Override output directory
- `AITESTKIT_DEFAULT_FRAMEWORK` - Default framework (pytest/robot/playwright)

## Project Documentation

### Primary Specification

**[docs/MASTER_SPEC.md](docs/MASTER_SPEC.md)** - The single source of truth for the project.

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

**[docs/BACKLOG.md](docs/BACKLOG.md)** - GitHub issue-style feature backlog extracted from MASTER_SPEC.md.

Track implementation progress for all 27 features across 4 priority levels.

### Implementation Guidance

**[docs/development/claude/SKILL.md](docs/development/claude/SKILL.md)** - Detailed implementation guidance.

This includes:
- Complete class structures and method signatures
- Architecture diagrams and data flows
- Prompt template content
- Testing patterns and mocking examples
- Implementation checklist by phase
- Debugging tips
