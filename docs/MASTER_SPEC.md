# AITestKit Master Specification
## AI-Powered Multi-Framework Test Generation Toolkit
### Version 2.0 | January 11, 2026

---

# Table of Contents

1. [Vision & Mission](#1-vision--mission)
2. [Core Principles](#2-core-principles)
3. [Architecture Overview](#3-architecture-overview)
4. [Feature Specification](#4-feature-specification)
5. [Implementation Plan](#5-implementation-plan)
6. [GitHub Actions](#6-github-actions)
7. [Data Schemas](#7-data-schemas)
8. [CLI Reference](#8-cli-reference)
9. [Prompt System](#9-prompt-system)
10. [Configuration](#10-configuration)
11. [Testing Strategy](#11-testing-strategy)
12. [Appendices](#appendices)

---

# 1. Vision & Mission

## 1.1 Vision Statement

**Transform test development from a manual, repetitive task into an AI-accelerated, quality-assured process where humans focus on strategy and AI handles implementation.**

AITestKit envisions a future where QA engineers define *what* to test in natural language, and AI generates production-ready test code across any framework, while maintaining quality through automated validation and human oversight.

## 1.2 Mission Statement

**Provide an open-source, framework-agnostic CLI toolkit that leverages Claude AI to generate, analyze, and validate test code, with a continuous feedback loop that improves output quality over time.**

## 1.3 Project Objectives

| Objective | Description | Success Metric |
|-----------|-------------|----------------|
| **Multi-Framework Support** | Support 25+ testing frameworks across 6 categories | All priority 0 frameworks working |
| **Quality Generation** | Generate production-ready test code | 85%+ approval rate on first generation |
| **Human-in-the-Loop** | Maintain human oversight on all AI output | 100% of generated code reviewed before use |
| **Continuous Improvement** | Learn from rejections to improve prompts | Measurable score improvement over time |
| **Zero Config Start** | Users can start with minimal setup | `pip install` + API key = working tool |
| **Framework Validation** | Auto-lint generated tests | Framework-specific linting on approval |

## 1.4 Target Users

| User Type | Use Case | Primary Features |
|-----------|----------|------------------|
| **QA Engineers** | Generate tests from scenarios | `generate`, `feedback`, `analyze` |
| **Test Leads** | Maintain prompt quality | `regression`, prompt management |
| **Developers** | Quick test scaffolding | `generate` with dry-run |
| **DevOps** | CI/CD integration | GitHub Actions, auto-lint |

## 1.5 Non-Goals (Out of Scope)

The following are explicitly NOT part of AITestKit's scope:

- **Test Execution**: AITestKit generates tests, it does not run them
- **Test Management**: No test case management or reporting features
- **Self-Learning AI**: AI does not automatically update prompts; humans do
- **GUI Interface**: CLI-only; no web or desktop UI planned
- **Cloud Service**: Local tool only; no SaaS offering

---

# 2. Core Principles

## 2.1 The Human-in-the-Loop Model

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   AI GENERATES  ──►  HUMAN REVIEWS  ──►  HUMAN APPROVES/REJECTS        │
│                                                                         │
│   AI does NOT self-learn. Humans learn from AI output and improve it.  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Why This Model?**

| AI Limitation | Impact | Our Mitigation |
|---------------|--------|----------------|
| Cannot understand business context | May test wrong things | Human defines scenarios |
| Misses edge cases | False confidence | Human review required |
| Hallucination risk | Invalid test code | Linting + human validation |
| No strategic thinking | Tests structure, not intent | Human guides strategy |

## 2.2 Responsibility Matrix

**Human Responsibilities (Cannot Be Delegated):**
- Define WHAT to test (test strategy, scenarios)
- Quality perspective and risk assessment
- Edge case identification from domain knowledge
- Review and approve all AI-generated code
- Decide when prompts need improvement
- Final judgment on test quality

**AI Responsibilities (Delegation Appropriate):**
- Generate test code from human-defined scenarios
- Apply consistent patterns across many tests
- Parse and summarize failure logs
- Suggest potential root causes
- Generate documentation
- Handle repetitive code writing
- Follow established templates precisely

## 2.3 The Feedback Loop

```
                    ┌──────────────────┐
                    │  PROMPT LIBRARY  │◄────────────────┐
                    │ (Version Control)│                 │
                    └────────┬─────────┘                 │
                             │                           │
                             │ Used by                   │
                             ▼                           │
                    ┌──────────────────┐                 │
                    │  AI GENERATION   │                 │
                    │  (Claude API)    │                 │
                    └────────┬─────────┘                 │
                             │                           │
                             │ Produces                  │
                             ▼                           │
                    ┌──────────────────┐                 │
                    │     OUTPUT       │                 │
                    │  (Test Files)    │                 │
                    └────────┬─────────┘                 │
                             │                           │
                             │ Reviewed by               │
                             ▼                           │
                    ┌──────────────────┐                 │
                    │  HUMAN REVIEW    │─────────────────┤
                    │                  │                 │
                    │  ✓ Approve       │                 │
                    │  ✗ Reject+Reason │                 │
                    └────────┬─────────┘                 │
                             │                           │
                             │ Patterns emerge           │
                             ▼                           │
                    ┌──────────────────┐                 │
                    │  PATTERN DETECT  │                 │
                    │  (3+ = pattern)  │─────────────────┘
                    └──────────────────┘
                             │
                             ▼
                    Humans update prompts
                    based on patterns
```

## 2.4 Model Selection Strategy

| Model | Use Case | Cost (per 1M tokens) | Rationale |
|-------|----------|----------------------|-----------|
| **Claude Opus 4.5** | Code generation | $5 in / $25 out | Best coding quality (80.9% SWE-bench) |
| **Claude Sonnet 4.5** | Failure analysis | $3 in / $15 out | Good balance of quality/cost |
| **Claude Haiku 4.5** | Prompt regression | $1 in / $5 out | Fast, cheap for high volume |

**Task-to-Model Mapping:**

| Task | Model | Trigger |
|------|-------|---------|
| Generate test file | Opus 4.5 | `aitestkit generate` |
| Analyze test failure | Sonnet 4.5 | `aitestkit analyze` |
| Validate prompt change | Haiku 4.5 | PR to prompts/** |
| Quick syntax check | Haiku 4.5 | Internal validation |

---

# 3. Architecture Overview

## 3.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER'S PROJECT                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐    ┌─────────────────────────────────────────────┐    │
│  │   User's    │    │              .aitestkit/                    │    │
│  │   Tests     │    │  ┌─────────────┐  ┌──────────────────────┐  │    │
│  │             │    │  │ config.yaml │  │      feedback/       │  │    │
│  │ tests/      │    │  └─────────────┘  │  ├─ pending.json     │  │    │
│  │ ├─ login.py │    │                   │  ├─ approved.json    │  │    │
│  │ ├─ api.robot│    │                   │  ├─ rejected.json    │  │    │
│  │ └─ ...      │    │                   │  └─ patterns.json    │  │    │
│  └─────────────┘    │                   └──────────────────────┘  │    │
│                     │  ┌──────────────────────┐                   │    │
│                     │  │      history/        │                   │    │
│                     │  │  └─ generations.json │                   │    │
│                     │  └──────────────────────┘                   │    │
│                     └─────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ CLI Commands
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          AITESTKIT CLI                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ generate │  │ feedback │  │ analyze  │  │regression│  │   info   │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │             │             │             │             │        │
│       └─────────────┴──────┬──────┴─────────────┴─────────────┘        │
│                            │                                           │
│                            ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      CORE MODULES                                │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │   │
│  │  │ generator/ │  │ analyzer/  │  │ regression/│  │ frameworks/│ │   │
│  │  │            │  │            │  │            │  │            │ │   │
│  │  │ context    │  │ log_parser │  │ scorer     │  │ registry   │ │   │
│  │  │ output     │  │ analyzer   │  │ runner     │  │ base       │ │   │
│  │  │ generator  │  │            │  │ benchmarks │  │ (25 FWs)   │ │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                            │                                           │
│                            ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    UTILITIES                                     │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐ │   │
│  │  │ claude_client  │  │    config      │  │     prompts/       │ │   │
│  │  │                │  │                │  │  templates/        │ │   │
│  │  │ • generate()   │  │ • Settings     │  │  context/          │ │   │
│  │  │ • analyze()    │  │ • get_settings │  │  benchmarks/       │ │   │
│  │  │ • usage_stats  │  │ • model IDs    │  │  examples/         │ │   │
│  │  └────────────────┘  └────────────────┘  └────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ API Calls
                                    ▼
                    ┌───────────────────────────┐
                    │     ANTHROPIC API         │
                    │                           │
                    │  Opus 4.5 (generation)    │
                    │  Sonnet 4.5 (analysis)    │
                    │  Haiku 4.5 (regression)   │
                    └───────────────────────────┘
```

## 3.2 Directory Structure

```
aitestkit/                              # Package root
├── src/aitestkit/
│   ├── __init__.py                     # Package exports
│   ├── cli.py                          # Click CLI entry point
│   ├── config.py                       # Pydantic settings ✅ COMPLETE
│   │
│   ├── frameworks/                     # Framework registry
│   │   ├── __init__.py
│   │   ├── base.py                     # FrameworkAdapter ABC ✅ COMPLETE
│   │   └── registry.py                 # 25 frameworks ✅ COMPLETE
│   │
│   ├── generator/                      # Test generation
│   │   ├── __init__.py
│   │   ├── context_builder.py          # Build prompt context
│   │   ├── output_parser.py            # Parse AI response
│   │   └── generator.py                # Main generation logic
│   │
│   ├── analyzer/                       # Failure analysis
│   │   ├── __init__.py
│   │   ├── log_parser.py               # Parse test logs
│   │   └── analyzer.py                 # AI-powered analysis
│   │
│   ├── regression/                     # Prompt regression
│   │   ├── __init__.py
│   │   ├── scorer.py                   # Score AI output
│   │   ├── runner.py                   # Run regression tests
│   │   └── benchmarks/                 # Benchmark scenarios
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── claude_client.py            # Anthropic API wrapper
│   │
│   └── prompts/                        # Prompt templates
│       ├── templates/
│       │   ├── code-generation/
│       │   │   ├── system.md           # System prompt
│       │   │   ├── unit/               # Unit test templates
│       │   │   ├── e2e/                # E2E test templates
│       │   │   ├── bdd/                # BDD test templates
│       │   │   ├── performance/        # Perf test templates
│       │   │   ├── security/           # Security test templates
│       │   │   └── api/                # API test templates
│       │   └── failure_analysis/
│       │       └── system.md
│       ├── context/                    # Reusable context files
│       ├── examples/                   # Few-shot examples
│       └── benchmarks/                 # Regression benchmarks
│
├── tests/                              # Production test suite
├── dev_tests/                          # Development tests ✅ 7 passing
├── docs/
│   ├── MASTER_SPEC.md                  # This document
│   ├── BACKLOG.md                      # Feature backlog
│   └── guides/                         # User guides
│
├── .github/
│   └── workflows/
│       ├── test.yml                    # CI: lint + test
│       ├── release.yml                 # Auto changelog + release notes
│       ├── prompt-regression.yml       # Prompt quality gate
│       └── lint-approved.yml           # Auto-lint approved tests
│
├── CLAUDE.md                           # Claude Code instructions
├── CHANGELOG.md                        # Auto-generated
├── RELEASE_NOTES.md                    # AI-generated
└── pyproject.toml                      # Project config ✅ COMPLETE
```

## 3.3 Data Flow Diagrams

### 3.3.1 Test Generation Flow

```
┌─────────┐     ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  User   │────►│ CLI         │────►│ Context      │────►│ Claude API  │
│ Scenario│     │ (generate)  │     │ Builder      │     │ (Opus 4.5)  │
└─────────┘     └─────────────┘     └──────────────┘     └──────┬──────┘
                                                                │
                                                                ▼
┌─────────┐     ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ pending │◄────│ Output      │◄────│ Output       │◄────│ AI Response │
│ .json   │     │ File        │     │ Parser       │     │             │
└─────────┘     └─────────────┘     └──────────────┘     └─────────────┘
```

### 3.3.2 Feedback Flow

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│   User      │────►│ CLI          │────►│ Update        │
│ (approve/   │     │ (feedback)   │     │ JSON files    │
│  reject)    │     │              │     │               │
└─────────────┘     └──────────────┘     └───────┬───────┘
                                                 │
                    ┌────────────────────────────┴────────────────────────┐
                    │                                                     │
                    ▼                                                     ▼
           ┌──────────────┐                                      ┌──────────────┐
           │ If APPROVE:  │                                      │ If REJECT:   │
           │              │                                      │              │
           │ • Move to    │                                      │ • Log reason │
           │   approved   │                                      │ • Pattern    │
           │ • Trigger    │                                      │   detection  │
           │   lint       │                                      │              │
           └──────────────┘                                      └──────────────┘
```

### 3.3.3 Prompt Regression Flow

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│  PR with    │────►│ GitHub       │────►│ Load          │
│  prompt     │     │ Actions      │     │ benchmarks    │
│  changes    │     │              │     │               │
└─────────────┘     └──────────────┘     └───────┬───────┘
                                                 │
                                                 ▼
                                        ┌───────────────┐
                                        │ Run OLD vs    │
                                        │ NEW prompt    │
                                        │ (Haiku 4.5)   │
                                        └───────┬───────┘
                                                │
                         ┌──────────────────────┴──────────────────────┐
                         │                                             │
                         ▼                                             ▼
                ┌──────────────┐                              ┌──────────────┐
                │ Score ≥ Old  │                              │ Score < Old  │
                │              │                              │ (Regression) │
                │ ✓ PASS       │                              │ ✗ BLOCK PR   │
                │ Allow merge  │                              │              │
                └──────────────┘                              └──────────────┘
```

---

# 4. Feature Specification

## 4.1 Feature Priority Levels

| Priority | Label | Description | Target |
|----------|-------|-------------|--------|
| **P0** | Core MVP | Essential for basic functionality | v1.0 release |
| **P1** | Important | Significant value, not blocking | v1.1 release |
| **P1.5** | GitHub Actions | CI/CD automation features | v1.0 release |
| **P2** | Nice-to-have | Quality of life improvements | v1.2+ |
| **P3** | Future | Long-term roadmap | v2.0+ |

## 4.2 P0 - Core MVP Features

### F01: CLI Framework

**Status:** 🔲 Placeholder exists
**Module:** `cli.py`

**Description:** Click-based command-line interface with Rich console output. Entry point for all user interactions.

**Commands:**
| Command | Description | Options |
|---------|-------------|---------|
| `generate` | Generate test from scenario | `-f/--framework`, `-o/--output`, `--dry-run`, `--context` |
| `feedback` | Submit review feedback | `approve`, `reject --reason` |
| `analyze` | Analyze failure logs | `-o/--output`, `--format` |
| `regression` | Run prompt regression | `--all`, `--category`, `--prompt` |
| `frameworks` | List frameworks | `--list`, `--category`, `--language` |
| `info` | Show configuration | (none) |
| `init` | Initialize project | `--force` |

**Implementation Details:**
```python
# Entry point structure
@click.group()
@click.version_option(version="1.0.0")
def main():
    """AITestKit - AI-Powered Test Generation Toolkit"""
    pass

@main.command()
@click.argument("scenario")
@click.option("-f", "--framework", type=click.Choice(get_framework_choices()))
@click.option("-o", "--output", type=click.Path())
@click.option("--dry-run", is_flag=True)
def generate(scenario: str, framework: str, output: str, dry_run: bool):
    """Generate test code from natural language scenario."""
    pass
```

---

### F02: Framework Registry

**Status:** ✅ Complete
**Module:** `frameworks/registry.py`

**Description:** Central registry of 25 testing frameworks across 6 categories with metadata for generation.

**Frameworks by Category:**

| Category | Count | Frameworks |
|----------|-------|------------|
| Unit | 4 | pytest, jest, junit, nunit |
| E2E | 4 | playwright-py, playwright-ts, cypress, selenium-py |
| BDD | 5 | pytest-bdd, cucumber-java, cucumber-js, behave, robot |
| Performance | 5 | locust, k6, jmeter, gatling, artillery |
| Security | 3 | nuclei, zap, bandit |
| API | 4 | httpx, postman, rest-assured, supertest |

**Priority Distribution:**
- Priority 0 (Core): 11 frameworks - implement first
- Priority 1 (Standard): 8 frameworks
- Priority 2 (Extended): 6 frameworks

---

### F03: Config Management

**Status:** ✅ Complete
**Module:** `config.py`

**Description:** Pydantic-based configuration with environment variable support and sensible defaults.

**Settings:**
| Setting | Type | Default | Env Var |
|---------|------|---------|---------|
| `anthropic_api_key` | str | Required | `ANTHROPIC_API_KEY` |
| `model_code_gen` | str | `claude-opus-4-5-20251101` | `AITESTKIT_MODEL_CODE_GEN` |
| `model_analysis` | str | `claude-sonnet-4-5-20250929` | `AITESTKIT_MODEL_ANALYSIS` |
| `model_regression` | str | `claude-haiku-4-5-20251001` | `AITESTKIT_MODEL_REGRESSION` |
| `max_tokens` | int | 4096 | `AITESTKIT_MAX_TOKENS` |
| `temperature` | float | 0.3 | `AITESTKIT_TEMPERATURE` |
| `output_dir` | Path | `./generated` | `AITESTKIT_OUTPUT_DIR` |

---

### F04: Claude Client

**Status:** 🔲 Empty file exists
**Module:** `utils/claude_client.py`

**Description:** Wrapper for Anthropic API with model selection, usage tracking, and cost calculation.

**Key Classes:**
```python
@dataclass
class UsageStats:
    input_tokens: int
    output_tokens: int
    model: str
    cost_usd: float
    timestamp: datetime

class ClaudeClient:
    def generate(self, system: str, user: str, model: ModelType) -> tuple[str, UsageStats]
    def generate_code(self, system: str, user: str) -> tuple[str, UsageStats]  # Uses Opus
    def analyze(self, system: str, user: str) -> tuple[str, UsageStats]  # Uses Sonnet
    def quick_check(self, system: str, user: str) -> tuple[str, UsageStats]  # Uses Haiku
    def get_total_cost(self) -> float
```

---

### F05: Test Generation

**Status:** 🔲 Empty files exist
**Module:** `generator/`

**Description:** Core test generation logic using Claude API with context building and output parsing.

**Components:**

1. **ContextBuilder** (`context_builder.py`)
   - Loads prompt templates
   - Loads framework-specific context
   - Loads few-shot examples
   - Assembles final prompt

2. **OutputParser** (`output_parser.py`)
   - Extracts code from AI response
   - Validates basic structure
   - Suggests filename based on framework

3. **Generator** (`generator.py`)
   - Orchestrates generation flow
   - Handles multi-file frameworks (BDD)
   - Records to generation history

**Generation Result:**
```python
@dataclass
class GenerationResult:
    success: bool
    code: str
    filename: str
    framework: str
    usage: UsageStats
    secondary_code: str | None = None  # For BDD step files
    secondary_filename: str | None = None
    warnings: list[str] = field(default_factory=list)
```

---

### F06: Prompt Templates

**Status:** 🔲 Empty files exist
**Module:** `prompts/`

**Description:** CTCO-framework prompt templates for each supported framework.

**Template Structure (CTCO Framework):**
```markdown
# Context
You are a Senior QA Engineer specializing in {framework} testing...

# Task
Generate a complete, production-ready test file for the following scenario:
{scenario}

# Constraints
DO:
- Include proper error handling
- Use explicit waits (no time.sleep)
- Follow {framework} best practices
- Include documentation/comments

DON'T:
- Use hardcoded credentials
- Include TODO comments
- Leave empty test bodies
- Use deprecated APIs

# Output
Provide a complete {extension} file that can be executed immediately.
Include:
- All necessary imports
- Proper test structure
- Assertions with meaningful messages
```

---

### F07: Human Review Flow

**Status:** 🔲 Not started
**Module:** CLI + feedback storage

**Description:** Option B workflow - generate to file, user reviews externally, submits feedback via CLI.

**Workflow:**
```
1. User runs: aitestkit generate "Login test scenario" -f pytest
2. Tool generates: ./generated/test_login.py
3. Tool records in: .aitestkit/feedback/pending.json
4. User reviews file externally (IDE, editor)
5. User runs: aitestkit feedback approve test_login.py
   OR: aitestkit feedback reject test_login.py --reason "Missing edge cases"
6. Tool updates: approved.json or rejected.json
7. If approved: triggers lint workflow
```

---

### F08: Feedback Storage

**Status:** 🔲 Not started
**Module:** `.aitestkit/` directory

**Description:** Project-local storage for feedback, history, and patterns. JSON-based for simplicity.

**Directory Structure:**
```
.aitestkit/
├── config.yaml           # Project-level overrides (optional)
├── feedback/
│   ├── pending.json      # Generated, awaiting review
│   ├── approved.json     # Approved files (triggers lint)
│   ├── rejected.json     # Rejected with reasons
│   └── patterns.json     # Identified rejection patterns
└── history/
    └── generations.json  # All generation history
```

**See Section 7 for detailed JSON schemas.**

---

### F09: Few-Shot Examples

**Status:** 🔲 Not started
**Module:** `prompts/examples/`

**Description:** Approved test examples used as few-shot prompts to improve generation quality.

**Structure:**
```
prompts/examples/
├── unit/
│   ├── pytest_auth.py
│   └── jest_api.test.ts
├── e2e/
│   ├── playwright_login.py
│   └── cypress_checkout.cy.js
├── bdd/
│   ├── robot_dlp.robot
│   └── cucumber_auth.feature
└── ...
```

**Example Loading:**
```python
class ContextBuilder:
    def load_examples(self, framework: str, count: int = 2) -> list[str]:
        """Load few-shot examples for the framework."""
        pass
```

---

## 4.3 P1 - Important Features

### F10: Failure Analysis

**Status:** 🔲 Empty files exist
**Module:** `analyzer/`

**Description:** AI-powered analysis of test failure logs to identify root causes and suggest fixes.

**Components:**
```python
class FailureCategory(Enum):
    ENVIRONMENT = "environment"
    TEST_BUG = "test_bug"
    PRODUCT_BUG = "product_bug"
    FLAKY = "flaky"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"

@dataclass
class AnalysisResult:
    root_cause: str
    confidence: float  # 0.0 - 1.0
    category: FailureCategory
    suggested_fix: str
    similar_failures: list[str]
```

---

### F11: Pattern Identification

**Status:** 🔲 Not started
**Module:** Feedback analysis

**Description:** Automatically identify patterns in rejection reasons to guide prompt improvements.

**Algorithm:**
```python
def identify_patterns(rejections: list[Rejection], threshold: int = 3) -> list[Pattern]:
    """
    Group rejections by similarity.
    If 3+ rejections share similar reasons → Pattern identified.
    """
    # 1. Extract keywords from rejection reasons
    # 2. Cluster by keyword similarity
    # 3. If cluster size >= threshold, create Pattern
    pass
```

---

### F12: Prompt Regression

**Status:** 🔲 Empty files exist
**Module:** `regression/`

**Description:** Automated validation that prompt changes don't degrade output quality.

**Components:**

1. **Scorer** (`scorer.py`)
   - Structural score (40 points): sections, setup/teardown, docs
   - Content score (40 points): required elements, tags, libraries
   - Quality score (20 points): no hardcoded waits, error handling, BDD style

2. **Runner** (`runner.py`)
   - Loads benchmark scenarios
   - Runs old vs new prompt
   - Compares scores
   - Reports pass/fail

3. **Benchmarks** (`benchmarks/`)
   - YAML scenario files
   - Expected elements
   - Minimum scores

**Scoring Thresholds:**
- Minimum passing score: 85/100
- Regression tolerance: 5 points (new score can be up to 5 points lower than old)

---

### F13: Cost Tracking

**Status:** 🔲 Not started
**Module:** `utils/claude_client.py`

**Description:** Track API usage and costs for budgeting.

**Features:**
- Per-call cost calculation
- Session total
- Export to JSON/CSV
- Monthly budget warnings (optional)

---

### F14: Generation History

**Status:** 🔲 Not started
**Module:** `.aitestkit/history/`

**Description:** Track all generation attempts for analytics and debugging.

**History Entry:**
```json
{
  "id": "gen_20260111_143022_abc123",
  "timestamp": "2026-01-11T14:30:22Z",
  "scenario": "Test user login with valid credentials",
  "framework": "pytest",
  "output_file": "test_login.py",
  "status": "approved",
  "usage": {
    "input_tokens": 1500,
    "output_tokens": 800,
    "cost_usd": 0.0425
  }
}
```

---

### F17: Project Init

**Status:** 🔲 Not started (Elevated from P2)
**Module:** CLI command

**Description:** Initialize a project with `.aitestkit/` directory and optional config.

**Command:**
```bash
aitestkit init [--force]
```

**Creates:**
```
.aitestkit/
├── config.yaml           # With commented examples
├── feedback/
│   ├── pending.json      # Empty array
│   ├── approved.json     # Empty array
│   ├── rejected.json     # Empty array
│   └── patterns.json     # Empty object
└── history/
    └── generations.json  # Empty array
```

**Zero-Config Philosophy:**
- Tool works without `init` (uses defaults)
- `init` provides explicit structure for team projects
- Git-friendly (include in .gitignore or commit)

---

## 4.4 P1.5 - GitHub Actions Features

### F23: CI Test Workflow

**Status:** 🔲 Empty file exists
**File:** `.github/workflows/test.yml`

**Description:** Standard CI workflow for AITestKit development.

**Triggers:**
- Push to main/develop
- Pull requests to main

**Jobs:**
```yaml
jobs:
  lint:
    - ruff check
    - black --check
    - mypy

  test:
    strategy:
      matrix:
        python: [3.11, 3.12]
    steps:
      - pytest with coverage
      - Upload coverage report
```

---

### F24: Auto CHANGELOG

**Status:** 🔲 New feature
**File:** `.github/workflows/release.yml`

**Description:** Automatically generate CHANGELOG.md from conventional commits on each push to main.

**Implementation:**
- Use `BobAnkh/auto-generate-changelog` or similar
- Parse conventional commits: `feat:`, `fix:`, `docs:`, etc.
- Group by type
- Include PR/issue links

**Trigger:** Push to main branch

---

### F25: AI Version Log

**Status:** 🔲 New feature
**File:** `.github/workflows/release.yml` (same workflow)

**Description:** Generate human-readable release notes using Claude AI.

**Implementation:**
```yaml
- name: Generate AI Release Notes
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    # Get commits since last tag
    # Send to Claude Sonnet for summarization
    # Write to RELEASE_NOTES.md
```

**Output File:** `RELEASE_NOTES.md`

---

### F26: Prompt Regression Action

**Status:** 🔲 Empty file exists
**File:** `.github/workflows/prompt-regression.yml`

**Description:** Automatically validate prompt quality on PRs that modify prompt templates.

**Trigger:** PR modifying `src/aitestkit/prompts/templates/**`

**Behavior:**
- Run old vs new prompt against benchmarks
- Score comparison
- If regression detected (new score < old - 5): **Block PR**
- Post results as PR comment

---

### F27: Auto-Lint on Approve

**Status:** 🔲 New feature
**File:** `.github/workflows/lint-approved.yml`

**Description:** When user approves a generated test and pushes, automatically run framework-specific linting.

**Trigger:** Push that modifies `.aitestkit/feedback/approved.json`

**Framework-to-Linter Mapping:**
| Framework | Linter | Command |
|-----------|--------|---------|
| pytest, playwright-py, locust | ruff, black, mypy | `ruff check && black --check && mypy` |
| robot | robocop | `robocop` |
| jest, playwright-ts, cypress | eslint, prettier | `eslint && prettier --check` |
| junit, cucumber-java | checkstyle | `checkstyle` |
| BDD (.feature) | gherkin-lint | `gherkin-lint` |

**Workflow Logic:**
```yaml
- name: Read approved files
  run: |
    # Parse .aitestkit/feedback/approved.json
    # Get newly approved files
    # Determine framework from extension
    # Run appropriate linter

- name: Post lint results
  # Comment on commit or create issue if lint fails
```

---

## 4.5 P2 - Nice-to-Have Features

### F15: Demo Workflow

**File:** `.github/workflows/demo.yml`

**Description:** Interactive demo mode showing AITestKit capabilities.

---

### F16: Auto-Prompt Update

**Description:** Suggest prompt improvements based on rejection patterns.

---

### F18: Config Profiles

**Description:** Named configuration profiles for different use cases.

---

## 4.6 P3 - Future Features

### F19: Web Dashboard

**Description:** Browser-based UI for generation and review.

### F20: Team Collaboration

**Description:** Shared feedback and pattern learning across teams.

### F21: Custom Framework Support

**Description:** User-defined frameworks beyond the 25 built-in.

### F22: IDE Plugins

**Description:** VS Code and IntelliJ integrations.

---

# 5. Implementation Plan

## 5.1 Phase Overview

| Phase | Focus | Duration | Key Deliverables |
|-------|-------|----------|------------------|
| **Phase 1** | Foundation | Complete ✅ | Registry, Config, Project Structure |
| **Phase 2** | Core CLI | 1-2 weeks | CLI, Claude Client, Basic Generation |
| **Phase 3** | Generation | 1-2 weeks | Full Generator, Prompts, Output Parser |
| **Phase 4** | Feedback Loop | 1 week | Feedback Storage, Human Review Flow |
| **Phase 5** | Analysis | 1 week | Failure Analyzer, Pattern Detection |
| **Phase 6** | Regression | 1 week | Prompt Scoring, Benchmarks, Runner |
| **Phase 7** | GitHub Actions | 1 week | All 5 workflows |
| **Phase 8** | Polish | 1 week | Docs, Examples, Testing |

## 5.2 Phase 1: Foundation ✅ COMPLETE

**Status:** ✅ Completed (January 9, 2026)

**Deliverables:**
- [x] Framework Registry (25 frameworks, 6 categories)
- [x] Base Framework Interface
- [x] Pydantic Configuration
- [x] Project Structure
- [x] pyproject.toml with all dependencies
- [x] dev_tests with 7 passing tests

---

## 5.3 Phase 2: Core CLI

**Status:** 🔨 Next Up
**Target:** Week of January 13-17, 2026

### Tasks

| Task | Priority | Estimate | Dependencies |
|------|----------|----------|--------------|
| 2.1 Implement `claude_client.py` | P0 | 4h | Config complete |
| 2.2 Implement basic CLI structure | P0 | 2h | None |
| 2.3 Implement `frameworks` command | P0 | 1h | Registry complete |
| 2.4 Implement `info` command | P0 | 1h | Config complete |
| 2.5 Implement `init` command | P1 | 2h | None |
| 2.6 Write unit tests | P0 | 3h | All above |

### 2.1 Claude Client Implementation

```python
# src/aitestkit/utils/claude_client.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from anthropic import Anthropic

from aitestkit.config import get_settings, ModelType

# Pricing per 1M tokens (January 2026)
PRICING = {
    "opus": {"input": 5.00, "output": 25.00},
    "sonnet": {"input": 3.00, "output": 15.00},
    "haiku": {"input": 1.00, "output": 5.00},
}


@dataclass
class UsageStats:
    """Track API usage for a single call."""
    input_tokens: int
    output_tokens: int
    model: str
    cost_usd: float
    timestamp: datetime = field(default_factory=datetime.now)


class ClaudeClient:
    """Wrapper for Anthropic Claude API with model selection and cost tracking."""

    def __init__(self) -> None:
        settings = get_settings()
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.settings = settings
        self.usage_log: list[UsageStats] = []

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: ModelType = "sonnet",
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> tuple[str, UsageStats]:
        """Generate response from Claude."""
        model_id = self.settings.get_model_id(model)

        response = self.client.messages.create(
            model=model_id,
            max_tokens=max_tokens or self.settings.max_tokens,
            temperature=temperature or self.settings.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        usage = self._calculate_usage(model, response.usage)
        self.usage_log.append(usage)

        return response.content[0].text, usage

    def generate_code(self, system_prompt: str, user_prompt: str) -> tuple[str, UsageStats]:
        """Generate code using Opus 4.5 (best quality)."""
        return self.generate(system_prompt, user_prompt, model="opus", temperature=0.2)

    def analyze(self, system_prompt: str, user_prompt: str) -> tuple[str, UsageStats]:
        """Analyze using Sonnet 4.5 (good balance)."""
        return self.generate(system_prompt, user_prompt, model="sonnet", temperature=0.4)

    def quick_check(self, system_prompt: str, user_prompt: str) -> tuple[str, UsageStats]:
        """Quick check using Haiku 4.5 (fast and cheap)."""
        return self.generate(system_prompt, user_prompt, model="haiku", temperature=0.2)

    def _calculate_usage(self, model: ModelType, usage) -> UsageStats:
        """Calculate cost from token usage."""
        pricing = PRICING[model]
        cost = (
            (usage.input_tokens / 1_000_000) * pricing["input"]
            + (usage.output_tokens / 1_000_000) * pricing["output"]
        )
        return UsageStats(
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            model=model,
            cost_usd=cost,
        )

    def get_total_cost(self) -> float:
        """Get total cost of all API calls in this session."""
        return sum(entry.cost_usd for entry in self.usage_log)
```

### 2.2 CLI Structure

```python
# src/aitestkit/cli.py

import click
from rich.console import Console
from rich.table import Table

from aitestkit.frameworks.registry import (
    get_framework_choices,
    get_frameworks_by_category,
    format_framework_table,
    FrameworkCategory,
)
from aitestkit.config import get_settings

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="aitestkit")
def main() -> None:
    """AITestKit - AI-Powered Multi-Framework Test Generation Toolkit."""
    pass


@main.command()
@click.option("--list", "list_all", is_flag=True, help="List all frameworks")
@click.option(
    "--category", "-c",
    type=click.Choice([c.value for c in FrameworkCategory]),
    help="Filter by category"
)
@click.option("--language", "-l", help="Filter by programming language")
def frameworks(list_all: bool, category: str | None, language: str | None) -> None:
    """List supported testing frameworks."""
    # Implementation...
    pass


@main.command()
def info() -> None:
    """Show current configuration."""
    settings = get_settings()
    # Display settings with Rich
    pass


@main.command()
@click.option("--force", is_flag=True, help="Overwrite existing .aitestkit directory")
def init(force: bool) -> None:
    """Initialize AITestKit in the current project."""
    # Create .aitestkit/ directory structure
    pass


if __name__ == "__main__":
    main()
```

---

## 5.4 Phase 3: Generation

**Target:** Week of January 20-24, 2026

### Tasks

| Task | Priority | Estimate | Dependencies |
|------|----------|----------|--------------|
| 3.1 Create system prompt template | P0 | 3h | None |
| 3.2 Create framework-specific prompts | P0 | 4h | 3.1 |
| 3.3 Implement ContextBuilder | P0 | 4h | 3.2 |
| 3.4 Implement OutputParser | P0 | 3h | None |
| 3.5 Implement Generator | P0 | 4h | 3.3, 3.4, Claude Client |
| 3.6 Implement `generate` command | P0 | 3h | 3.5 |
| 3.7 Create few-shot examples | P1 | 4h | None |
| 3.8 Write tests | P0 | 4h | All above |

### Key Implementations

**ContextBuilder:**
```python
class ContextBuilder:
    def __init__(self, prompts_dir: Path):
        self.prompts_dir = prompts_dir

    def build(
        self,
        scenario: str,
        framework: str,
        context_files: list[Path] | None = None,
    ) -> tuple[str, str]:
        """Build system and user prompts."""
        system = self._load_system_prompt(framework)
        user = self._build_user_prompt(scenario, framework, context_files)
        return system, user
```

**OutputParser:**
```python
class OutputParser:
    def parse(self, response: str, framework: FrameworkInfo) -> ParseResult:
        """Extract code and metadata from AI response."""
        code = self._extract_code(response, framework.extension)
        filename = self._suggest_filename(code, framework)
        warnings = self._validate_basic_structure(code, framework)
        return ParseResult(code=code, filename=filename, warnings=warnings)
```

---

## 5.5 Phase 4: Feedback Loop

**Target:** Week of January 27-31, 2026

### Tasks

| Task | Priority | Estimate | Dependencies |
|------|----------|----------|--------------|
| 4.1 Create JSON schema definitions | P0 | 2h | None |
| 4.2 Implement feedback storage module | P0 | 4h | 4.1 |
| 4.3 Implement `feedback` command | P0 | 3h | 4.2 |
| 4.4 Update `generate` to record pending | P0 | 2h | 4.2 |
| 4.5 Write tests | P0 | 3h | All above |

---

## 5.6 Phase 5: Analysis

**Target:** Week of February 3-7, 2026

### Tasks

| Task | Priority | Estimate | Dependencies |
|------|----------|----------|--------------|
| 5.1 Create analysis prompt template | P0 | 2h | None |
| 5.2 Implement LogParser | P0 | 3h | None |
| 5.3 Implement Analyzer | P0 | 4h | 5.2, Claude Client |
| 5.4 Implement `analyze` command | P0 | 2h | 5.3 |
| 5.5 Implement pattern identification | P1 | 4h | Feedback storage |
| 5.6 Write tests | P0 | 3h | All above |

---

## 5.7 Phase 6: Regression

**Target:** Week of February 10-14, 2026

### Tasks

| Task | Priority | Estimate | Dependencies |
|------|----------|----------|--------------|
| 6.1 Create benchmark scenario format | P0 | 2h | None |
| 6.2 Create initial benchmarks | P0 | 4h | 6.1 |
| 6.3 Implement Scorer | P0 | 4h | None |
| 6.4 Implement Runner | P0 | 4h | 6.3, Claude Client |
| 6.5 Implement `regression` command | P0 | 2h | 6.4 |
| 6.6 Write tests | P0 | 3h | All above |

---

## 5.8 Phase 7: GitHub Actions

**Target:** Week of February 17-21, 2026

### Tasks

| Task | Priority | Estimate | Dependencies |
|------|----------|----------|--------------|
| 7.1 Implement test.yml | P0 | 2h | Tests exist |
| 7.2 Implement release.yml (changelog) | P1.5 | 3h | None |
| 7.3 Implement release.yml (AI notes) | P1.5 | 3h | Claude Client |
| 7.4 Implement prompt-regression.yml | P1.5 | 4h | Regression module |
| 7.5 Implement lint-approved.yml | P1.5 | 4h | Feedback storage |
| 7.6 Test workflows in PRs | P0 | 2h | All above |

---

## 5.9 Phase 8: Polish

**Target:** Week of February 24-28, 2026

### Tasks

| Task | Priority | Estimate | Dependencies |
|------|----------|----------|--------------|
| 8.1 Complete user documentation | P1 | 4h | All features |
| 8.2 Add more few-shot examples | P1 | 4h | Generator |
| 8.3 Add more benchmarks | P1 | 4h | Regression |
| 8.4 Integration testing | P0 | 4h | All features |
| 8.5 README and quick start | P0 | 2h | All features |
| 8.6 Final code review | P0 | 2h | All above |

---

# 6. GitHub Actions

## 6.1 Workflow Summary

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **CI Tests** | `test.yml` | Push, PR | Lint + test |
| **Release** | `release.yml` | Push to main | Changelog + AI notes |
| **Prompt Regression** | `prompt-regression.yml` | PR to prompts/** | Quality gate |
| **Lint Approved** | `lint-approved.yml` | Push with approved.json | Auto-lint |

## 6.2 CI Tests Workflow

```yaml
# .github/workflows/test.yml
name: CI Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -e ".[dev]"
      - name: Lint with ruff
        run: ruff check src/ tests/ dev_tests/
      - name: Check formatting with black
        run: black --check src/ tests/ dev_tests/
      - name: Type check with mypy
        run: mypy src/

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install -e ".[dev]"
      - name: Run tests with coverage
        run: pytest tests/ dev_tests/ -v --cov=aitestkit --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
```

## 6.3 Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate CHANGELOG
        uses: BobAnkh/auto-generate-changelog@v1.2.5
        with:
          REPO_NAME: "sefaertunc/AITestKit"
          ACCESS_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PATH: "CHANGELOG.md"
          COMMIT_MESSAGE: "docs(changelog): update changelog"
          TYPE: "feat:Features,fix:Bug Fixes,docs:Documentation,refactor:Refactoring,test:Tests,chore:Chores"

  ai-release-notes:
    runs-on: ubuntu-latest
    needs: changelog
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install anthropic

      - name: Generate AI Release Notes
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python scripts/generate_release_notes.py \
            --since-tag $(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0") \
            --output RELEASE_NOTES.md

      - name: Commit release notes
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add RELEASE_NOTES.md
          git diff --staged --quiet || git commit -m "docs: update AI-generated release notes"
          git push
```

## 6.4 Prompt Regression Workflow

```yaml
# .github/workflows/prompt-regression.yml
name: Prompt Regression

on:
  pull_request:
    paths:
      - "src/aitestkit/prompts/templates/**"

jobs:
  regression-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Detect changed prompts
        id: detect
        run: |
          CHANGED=$(git diff --name-only origin/main...HEAD -- 'src/aitestkit/prompts/templates/**')
          echo "changed_files=$CHANGED" >> $GITHUB_OUTPUT

      - name: Run regression tests
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          aitestkit regression \
            --changed-files "${{ steps.detect.outputs.changed_files }}" \
            --baseline-branch origin/main \
            --output regression_report.json

      - name: Check results
        id: check
        run: |
          python -c "
          import json
          with open('regression_report.json') as f:
              report = json.load(f)
          if not report['passed']:
              print('::error::Prompt regression detected!')
              exit(1)
          "

      - name: Post PR comment
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('regression_report.json'));

            let comment = '## Prompt Regression Test Results\n\n';
            comment += `| Scenario | Old Score | New Score | Status |\n`;
            comment += `|----------|-----------|-----------|--------|\n`;

            for (const result of report.results) {
              const status = result.passed ? '✅' : '❌';
              comment += `| ${result.scenario} | ${result.old_score} | ${result.new_score} | ${status} |\n`;
            }

            comment += `\n**Overall: ${report.passed ? 'PASSED ✅' : 'FAILED ❌ - PR Blocked'}**`;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

## 6.5 Lint Approved Workflow

```yaml
# .github/workflows/lint-approved.yml
name: Lint Approved Tests

on:
  push:
    paths:
      - ".aitestkit/feedback/approved.json"

jobs:
  lint-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2  # Need previous commit to diff

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install Python linters
        run: |
          pip install ruff black mypy robotframework-robocop

      - name: Install JS/TS linters
        run: |
          npm install -g eslint prettier @typescript-eslint/eslint-plugin

      - name: Get newly approved files
        id: approved
        run: |
          python scripts/get_newly_approved.py --output approved_files.json

      - name: Lint approved files
        run: |
          python scripts/lint_by_framework.py --files approved_files.json

      - name: Post lint results
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const results = fs.readFileSync('lint_results.txt', 'utf8');

            github.rest.repos.createCommitComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              commit_sha: context.sha,
              body: `## Lint Results for Approved Tests\n\n\`\`\`\n${results}\n\`\`\``
            });
```

---

# 7. Data Schemas

## 7.1 Feedback Schemas

### pending.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "timestamp", "scenario", "framework", "output_file"],
    "properties": {
      "id": {
        "type": "string",
        "pattern": "^gen_[0-9]{8}_[0-9]{6}_[a-z0-9]{6}$"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      },
      "scenario": {
        "type": "string"
      },
      "framework": {
        "type": "string"
      },
      "output_file": {
        "type": "string"
      },
      "usage": {
        "type": "object",
        "properties": {
          "input_tokens": { "type": "integer" },
          "output_tokens": { "type": "integer" },
          "cost_usd": { "type": "number" }
        }
      }
    }
  }
}
```

**Example:**
```json
[
  {
    "id": "gen_20260111_143022_abc123",
    "timestamp": "2026-01-11T14:30:22Z",
    "scenario": "Test user login with valid credentials",
    "framework": "pytest",
    "output_file": "generated/test_login.py",
    "usage": {
      "input_tokens": 1500,
      "output_tokens": 800,
      "cost_usd": 0.0425
    }
  }
]
```

### approved.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "approved_at", "output_file", "framework"],
    "properties": {
      "id": {
        "type": "string"
      },
      "approved_at": {
        "type": "string",
        "format": "date-time"
      },
      "output_file": {
        "type": "string"
      },
      "framework": {
        "type": "string"
      },
      "lint_status": {
        "type": "string",
        "enum": ["pending", "passed", "failed"]
      },
      "lint_output": {
        "type": "string"
      }
    }
  }
}
```

### rejected.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "rejected_at", "reason"],
    "properties": {
      "id": {
        "type": "string"
      },
      "rejected_at": {
        "type": "string",
        "format": "date-time"
      },
      "reason": {
        "type": "string"
      },
      "reason_category": {
        "type": "string",
        "enum": [
          "missing_edge_cases",
          "wrong_assertions",
          "incorrect_syntax",
          "not_following_patterns",
          "missing_error_handling",
          "wrong_framework_usage",
          "other"
        ]
      },
      "output_file": {
        "type": "string"
      },
      "framework": {
        "type": "string"
      }
    }
  }
}
```

### patterns.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "patterns": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "category": { "type": "string" },
          "description": { "type": "string" },
          "occurrence_count": { "type": "integer" },
          "first_seen": { "type": "string", "format": "date-time" },
          "last_seen": { "type": "string", "format": "date-time" },
          "affected_frameworks": {
            "type": "array",
            "items": { "type": "string" }
          },
          "suggested_prompt_fix": { "type": "string" }
        }
      }
    },
    "last_analyzed": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

## 7.2 History Schema

### generations.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "timestamp", "scenario", "framework", "status"],
    "properties": {
      "id": { "type": "string" },
      "timestamp": { "type": "string", "format": "date-time" },
      "scenario": { "type": "string" },
      "framework": { "type": "string" },
      "output_file": { "type": "string" },
      "status": {
        "type": "string",
        "enum": ["pending", "approved", "rejected"]
      },
      "rejection_reason": { "type": "string" },
      "usage": {
        "type": "object",
        "properties": {
          "input_tokens": { "type": "integer" },
          "output_tokens": { "type": "integer" },
          "cost_usd": { "type": "number" }
        }
      },
      "prompt_version": { "type": "string" }
    }
  }
}
```

## 7.3 Benchmark Schema

### benchmark_scenario.yaml

```yaml
# Schema for benchmark scenario files
scenario_id: string  # Unique identifier
name: string         # Human-readable name
category: string     # Framework category (unit, e2e, bdd, etc.)
framework: string    # Target framework

input:
  description: string  # Natural language scenario

expected_elements:
  must_contain:        # Strings that must appear in output
    - string
  must_have_imports:   # Required imports
    - string
  structure:
    has_setup: boolean
    has_teardown: boolean
    has_documentation: boolean
    min_test_count: integer
    min_assertion_count: integer

quality_checks:
  - string             # Quality criteria to check

baseline_score: integer  # Minimum acceptable score (0-100)
```

**Example:**
```yaml
scenario_id: "pytest_auth_001"
name: "Pytest Authentication Test"
category: "unit"
framework: "pytest"

input:
  description: |
    Test user authentication with valid and invalid credentials.
    Include tests for:
    1. Successful login with valid username/password
    2. Failed login with invalid password
    3. Failed login with non-existent user
    4. Account lockout after 3 failed attempts

expected_elements:
  must_contain:
    - "import pytest"
    - "def test_"
    - "assert"
  must_have_imports:
    - "pytest"
  structure:
    has_setup: true
    has_teardown: false
    has_documentation: true
    min_test_count: 4
    min_assertion_count: 4

quality_checks:
  - "No hardcoded credentials"
  - "Uses fixtures for test data"
  - "Has descriptive test names"
  - "Includes docstrings"

baseline_score: 85
```

---

# 8. CLI Reference

## 8.1 Command Overview

```
aitestkit [OPTIONS] COMMAND [ARGS]...

Commands:
  generate    Generate test code from natural language scenario
  feedback    Submit review feedback for generated tests
  analyze     Analyze test failure logs
  regression  Run prompt regression tests
  frameworks  List supported testing frameworks
  info        Show current configuration
  init        Initialize AITestKit in current project
```

## 8.2 generate

```
aitestkit generate [OPTIONS] SCENARIO

Generate test code from natural language scenario.

Arguments:
  SCENARIO  Natural language description of the test scenario [required]

Options:
  -f, --framework TEXT  Target testing framework [default: pytest]
  -o, --output PATH     Output file path [default: ./generated/<auto>]
  --context PATH        Additional context file(s) to include
  --dry-run            Show generated code without saving
  --no-record          Don't record in generation history
  -v, --verbose        Show detailed output
  --help               Show this message and exit

Examples:
  aitestkit generate "Test user login with valid credentials" -f pytest
  aitestkit generate "Test API rate limiting" -f httpx --dry-run
  aitestkit generate "Test shopping cart checkout" -f playwright-py -o tests/e2e/
```

## 8.3 feedback

```
aitestkit feedback [OPTIONS] COMMAND [ARGS]...

Submit review feedback for generated tests.

Commands:
  approve  Approve a generated test file
  reject   Reject a generated test file with reason

Options:
  --help  Show this message and exit
```

### feedback approve

```
aitestkit feedback approve [OPTIONS] FILE_PATH

Approve a generated test file.

Arguments:
  FILE_PATH  Path to the generated test file [required]

Options:
  --help  Show this message and exit

Example:
  aitestkit feedback approve generated/test_login.py
```

### feedback reject

```
aitestkit feedback reject [OPTIONS] FILE_PATH

Reject a generated test file with reason.

Arguments:
  FILE_PATH  Path to the generated test file [required]

Options:
  -r, --reason TEXT     Reason for rejection [required]
  -c, --category TEXT   Rejection category
  --help               Show this message and exit

Categories:
  missing_edge_cases, wrong_assertions, incorrect_syntax,
  not_following_patterns, missing_error_handling,
  wrong_framework_usage, other

Example:
  aitestkit feedback reject generated/test_login.py \
    --reason "Missing test for password reset" \
    --category missing_edge_cases
```

## 8.4 analyze

```
aitestkit analyze [OPTIONS] LOG_FILE

Analyze test failure logs using AI.

Arguments:
  LOG_FILE  Path to test failure log [required]

Options:
  -o, --output PATH     Output file for analysis report
  --format TEXT         Output format: markdown, json, console [default: console]
  --help               Show this message and exit

Example:
  aitestkit analyze test_results.log -o analysis.md --format markdown
```

## 8.5 regression

```
aitestkit regression [OPTIONS]

Run prompt regression tests.

Options:
  --all                    Run all benchmark scenarios
  --category TEXT          Run scenarios for specific category
  --prompt PATH           Test specific prompt file
  --changed-files TEXT    Test only changed prompts (CI mode)
  --baseline-branch TEXT  Branch to compare against [default: main]
  --output PATH           Output report file
  --help                  Show this message and exit

Example:
  aitestkit regression --all --output report.json
  aitestkit regression --category unit
  aitestkit regression --prompt src/aitestkit/prompts/templates/unit/pytest.md
```

## 8.6 frameworks

```
aitestkit frameworks [OPTIONS]

List supported testing frameworks.

Options:
  --list                  List all frameworks in table format
  -c, --category TEXT     Filter by category (unit, e2e, bdd, performance, security, api)
  -l, --language TEXT     Filter by programming language
  -p, --priority INTEGER  Filter by priority (0, 1, 2)
  --help                  Show this message and exit

Example:
  aitestkit frameworks --list
  aitestkit frameworks --category e2e
  aitestkit frameworks --language Python --priority 0
```

## 8.7 info

```
aitestkit info [OPTIONS]

Show current configuration.

Options:
  --help  Show this message and exit

Output includes:
  - API key status (configured/missing)
  - Model assignments
  - Default settings
  - Framework counts by priority
  - Project initialization status
```

## 8.8 init

```
aitestkit init [OPTIONS]

Initialize AITestKit in the current project.

Options:
  --force  Overwrite existing .aitestkit directory
  --help   Show this message and exit

Creates:
  .aitestkit/
  ├── config.yaml
  ├── feedback/
  │   ├── pending.json
  │   ├── approved.json
  │   ├── rejected.json
  │   └── patterns.json
  └── history/
      └── generations.json
```

---

# 9. Prompt System

## 9.1 Prompt Structure (CTCO Framework)

All prompts follow the **Context-Task-Constraints-Output** (CTCO) framework:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ CONTEXT                                                                 │
│ - Role definition                                                       │
│ - Domain expertise                                                      │
│ - Framework knowledge                                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TASK                                                                    │
│ - Clear objective                                                       │
│ - Input description                                                     │
│ - Expected steps                                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ CONSTRAINTS                                                             │
│ - DO rules (required behaviors)                                         │
│ - DON'T rules (prohibited behaviors)                                    │
│ - Quality requirements                                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ OUTPUT                                                                  │
│ - Expected format                                                       │
│ - Required sections                                                     │
│ - File structure                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## 9.2 System Prompt Template

```markdown
# Context

You are a Senior QA Engineer with 10+ years of experience in test automation. You specialize in writing clean, maintainable, production-ready test code.

Your expertise includes:
- {framework_name} testing framework
- {language} programming language
- Test design patterns and best practices
- BDD/TDD methodologies

# Task

Generate a complete, production-ready {framework_name} test file for the following scenario:

{scenario}

{additional_context}

# Constraints

## DO:
- Use descriptive test names that explain the expected behavior
- Include proper setup and teardown when needed
- Add meaningful assertions with clear failure messages
- Include docstrings/comments explaining test purpose
- Use fixtures/helpers for reusable test data
- Follow {framework_name} conventions and idioms
- Handle expected exceptions appropriately

## DON'T:
- Use `time.sleep()` - use explicit waits instead
- Leave empty test bodies or `pass` statements
- Include TODO or FIXME comments
- Use hardcoded credentials or sensitive data
- Ignore potential race conditions
- Use deprecated APIs

# Output

Provide a complete `{extension}` file that can be executed immediately.

Required sections:
1. Imports
2. Test fixtures/setup (if needed)
3. Test cases
4. Teardown (if needed)

Format: Return ONLY the code, wrapped in ```{language} code blocks.
```

## 9.3 Framework-Specific Prompts

Located in `prompts/templates/code-generation/{category}/{framework}.md`

Each extends the system prompt with framework-specific:
- Import patterns
- Test structure
- Assertion styles
- Configuration requirements

## 9.4 Prompt Versioning

Prompts are version-controlled in Git. Changes tracked via:

1. **CHANGELOG.md in prompts directory**
   ```markdown
   ## system.md v3 (2026-01-15)
   - Added: Explicit error handling requirement
   - Reason: 5 rejections due to missing try/catch

   ## system.md v2 (2026-01-10)
   - Added: BDD style requirement for E2E tests
   - Reason: Inconsistent test structure
   ```

2. **Git history**
   - All changes committed with conventional commits
   - `refactor(prompts): improve error handling guidance`

---

# 10. Configuration

## 10.1 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | - | Anthropic API key |
| `AITESTKIT_MODEL_CODE_GEN` | No | claude-opus-4-5-20251101 | Code generation model |
| `AITESTKIT_MODEL_ANALYSIS` | No | claude-sonnet-4-5-20250929 | Analysis model |
| `AITESTKIT_MODEL_REGRESSION` | No | claude-haiku-4-5-20251001 | Regression model |
| `AITESTKIT_MAX_TOKENS` | No | 4096 | Max tokens per request |
| `AITESTKIT_TEMPERATURE` | No | 0.3 | Generation temperature |
| `AITESTKIT_OUTPUT_DIR` | No | ./generated | Default output directory |

## 10.2 Project Configuration (.aitestkit/config.yaml)

```yaml
# .aitestkit/config.yaml
# Project-level configuration overrides

# Framework defaults
default_framework: pytest

# Output settings
output_dir: ./tests/generated
auto_lint: true

# Model overrides (optional)
models:
  code_generation: claude-opus-4-5-20251101
  analysis: claude-sonnet-4-5-20250929
  regression: claude-haiku-4-5-20251001

# Generation settings
generation:
  max_tokens: 4096
  temperature: 0.3
  include_examples: true
  example_count: 2

# Feedback settings
feedback:
  require_reason_on_reject: true
  pattern_threshold: 3  # rejections before pattern is identified

# Context files to always include
default_context:
  - ./docs/api_spec.yaml
  - ./docs/test_standards.md
```

## 10.3 Zero-Config Philosophy

AITestKit is designed to work with **minimal configuration**:

1. **Install:** `pip install aitestkit`
2. **Set API key:** `export ANTHROPIC_API_KEY=sk-...`
3. **Use:** `aitestkit generate "Test user login" -f pytest`

Optional enhancements:
- Run `aitestkit init` for project structure
- Create `.aitestkit/config.yaml` for team settings
- Add context files for domain-specific knowledge

---

# 11. Testing Strategy

## 11.1 Test Categories

| Category | Location | Purpose | CI Trigger |
|----------|----------|---------|------------|
| **Unit** | `tests/unit/` | Test individual modules | Every PR |
| **Integration** | `tests/integration/` | Test module interactions | Every PR |
| **Dev Tests** | `dev_tests/` | Development-time validation | Manual |
| **E2E** | `tests/e2e/` | Full workflow tests | Pre-release |

## 11.2 Test Coverage Requirements

| Module | Minimum Coverage | Priority |
|--------|------------------|----------|
| `config.py` | 90% | P0 |
| `frameworks/registry.py` | 90% | P0 |
| `utils/claude_client.py` | 85% | P0 |
| `generator/*.py` | 80% | P0 |
| `analyzer/*.py` | 80% | P1 |
| `regression/*.py` | 80% | P1 |
| `cli.py` | 75% | P0 |

**Overall target:** 80% coverage

## 11.3 Mocking Strategy

All tests that would call the Claude API must be mocked:

```python
@pytest.fixture
def mock_anthropic(mocker):
    """Mock Anthropic client to prevent real API calls."""
    mock_client = mocker.patch("anthropic.Anthropic")
    mock_response = mocker.MagicMock()
    mock_response.content = [mocker.MagicMock(text="Generated code here")]
    mock_response.usage = mocker.MagicMock(input_tokens=100, output_tokens=200)
    mock_client.return_value.messages.create.return_value = mock_response
    return mock_client
```

## 11.4 Test Fixtures

Standard fixtures in `conftest.py`:

```python
@pytest.fixture
def test_config(tmp_path: Path) -> Settings:
    """Create test configuration with temp paths."""
    pass

@pytest.fixture
def cli_runner() -> CliRunner:
    """Click CLI test runner."""
    return CliRunner()

@pytest.fixture
def sample_scenario() -> str:
    """Sample test scenario for generation."""
    return "Test user login with valid username and password"

@pytest.fixture
def sample_log() -> str:
    """Sample failure log for analysis."""
    pass
```

---

# Appendices

## Appendix A: Linter Mapping

| Framework | Language | Linters | Install |
|-----------|----------|---------|---------|
| pytest | Python | ruff, black, mypy | `pip install ruff black mypy` |
| playwright-py | Python | ruff, black, mypy | `pip install ruff black mypy` |
| locust | Python | ruff, black, mypy | `pip install ruff black mypy` |
| robot | Robot | robocop | `pip install robotframework-robocop` |
| jest | TypeScript | eslint, prettier | `npm install eslint prettier` |
| playwright-ts | TypeScript | eslint, prettier | `npm install eslint prettier` |
| cypress | JavaScript | eslint, prettier | `npm install eslint prettier` |
| junit | Java | checkstyle | Maven/Gradle plugin |
| cucumber-java | Java/Gherkin | checkstyle, gherkin-lint | Maven + npm |
| pytest-bdd | Python/Gherkin | ruff, gherkin-lint | `pip install ruff` + npm |
| k6 | JavaScript | eslint | `npm install eslint` |
| nuclei | YAML | yamllint | `pip install yamllint` |

## Appendix B: Model IDs

| Model | ID | Release |
|-------|-----|---------|
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | November 2025 |
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | September 2025 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | October 2025 |

## Appendix C: Conventional Commits

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(generator): add playwright support` |
| `fix` | Bug fix | `fix(cli): handle empty scenario` |
| `docs` | Documentation | `docs: update MASTER_SPEC.md` |
| `style` | Formatting | `style: fix line length issues` |
| `refactor` | Refactoring | `refactor(config): use Pydantic v2` |
| `test` | Tests | `test(generator): add unit tests` |
| `chore` | Maintenance | `chore: update dependencies` |

## Appendix D: Quick Start Guide

```bash
# 1. Install
pip install aitestkit

# 2. Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Generate a test
aitestkit generate "Test user registration with email validation" -f pytest

# 4. Review the generated file
cat generated/test_user_registration.py

# 5. Approve or reject
aitestkit feedback approve generated/test_user_registration.py
# OR
aitestkit feedback reject generated/test_user_registration.py --reason "Missing edge case for invalid email"

# 6. (Optional) Initialize project structure
aitestkit init

# 7. View available frameworks
aitestkit frameworks --list

# 8. Check configuration
aitestkit info
```

---

# Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-03 | QA Team | Initial specification |
| 2.0 | 2026-01-11 | QA Team | Consolidated all docs, added GitHub Actions, feedback loop |

---

**This document supersedes:**
- AITestKit_Project_Plan.md
- AITestKit_Visual_Roadmap.md
- AITestKit_MultiFramework_Update_Prompt.md
- AITestKit_Complete_Specification.md
- docs/IMPLEMENTATION_ROADMAP.md

**These files should be archived or deleted after MASTER_SPEC.md is committed.**

---

*AITestKit - AI-Powered Multi-Framework Test Generation Toolkit*
*Open Source | MIT License | github.com/sefaertunc/AITestKit*
