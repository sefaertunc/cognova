# AITestKit - Complete Project Specification
## AI-Powered Test Development Toolkit
### For Claude Code Implementation

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Technology Stack](#3-technology-stack)
4. [Project Structure](#4-project-structure)
5. [Core Components](#5-core-components)
6. [Claude API Integration](#6-claude-api-integration)
7. [Prompt Templates](#7-prompt-templates)
8. [CLI Specification](#8-cli-specification)
9. [Test Generator](#9-test-generator)
10. [Failure Analyzer](#10-failure-analyzer)
11. [Prompt Regression](#11-prompt-regression)
12. [Sample Application](#12-sample-application)
13. [Configuration](#13-configuration)
14. [GitHub Actions](#14-github-actions)
15. [File Specifications](#15-file-specifications)
16. [Implementation Order](#16-implementation-order)
17. [Testing Strategy](#17-testing-strategy)
18. [Documentation Requirements](#18-documentation-requirements)

---

# 1. Project Overview

## 1.1 Vision

AITestKit is an open-source command-line toolkit that demonstrates AI-assisted test automation. It uses Claude API to generate test code from natural language descriptions, analyze test failures, and validate prompt quality through regression testing.

## 1.2 Purpose

This is a **portfolio project** designed to showcase:
- AI/LLM integration skills
- Prompt engineering expertise
- Python development proficiency
- Test automation knowledge
- DevOps capabilities (CI/CD)
- Technical documentation skills

## 1.3 Core Features

| Feature | Command | Model | Description |
|---------|---------|-------|-------------|
| **Test Generator** | `aitestkit generate` | Claude Opus 4.5 | Generate test code from natural language |
| **Failure Analyzer** | `aitestkit analyze` | Claude Sonnet 4.5 | Analyze test failures, suggest fixes |
| **Prompt Regression** | `aitestkit regression` | Claude Haiku 4.5 | Validate prompt changes don't degrade quality |

## 1.4 Core Principle

```
+------------------------------------------------------------------+
|                                                                    |
|   AI generates → Human reviews → Human approves/rejects            |
|                                                                    |
|   AI does NOT self-learn. Humans improve prompts based on output.  |
|                                                                    |
+------------------------------------------------------------------+
```

## 1.5 Target Users

- QA Engineers exploring AI assistance
- Developers learning prompt engineering
- Teams evaluating AI for test automation
- Portfolio reviewers / potential employers

---

# 2. Architecture

## 2.1 High-Level Architecture

```
+=========================================================================+
|                         AITESTKIT ARCHITECTURE                           |
+=========================================================================+

                              TRIGGERS
    +------------------+  +------------------+  +------------------+
    |    MANUAL        |  |  TEST FAILURE    |  |   PROMPT PR      |
    | (CLI command)    |  | (Log file input) |  | (Git detects)    |
    +--------+---------+  +--------+---------+  +--------+---------+
             |                     |                     |
             v                     v                     v
    +------------------+  +------------------+  +------------------+
    |  TEST GENERATOR  |  | FAILURE ANALYZER |  | PROMPT REGRESSION|
    |                  |  |                  |  |                  |
    |  Claude Opus 4.5 |  | Claude Sonnet 4.5|  | Claude Haiku 4.5 |
    |  $5/$25 per 1M   |  | $3/$15 per 1M    |  | $1/$5 per 1M     |
    +--------+---------+  +--------+---------+  +--------+---------+
             |                     |                     |
             v                     v                     v
    +------------------+  +------------------+  +------------------+
    |  GENERATED TEST  |  | ANALYSIS REPORT  |  |  PASS/FAIL       |
    |  .robot/.py/.ts  |  |  Markdown file   |  |  Score comparison|
    +--------+---------+  +--------+---------+  +--------+---------+
             |                     |                     |
             v                     v                     v
    +------------------+  +------------------+  +------------------+
    |  HUMAN REVIEW    |  |  HUMAN ACTION    |  |  MERGE/BLOCK     |
    |  Approve/Reject  |  |  Fix the issue   |  |  PR decision     |
    +------------------+  +------------------+  +------------------+
             |
             v
    +------------------------------------------------------------------+
    |                       FEEDBACK LOOP                               |
    |   Rejections → Identify Patterns → Update Prompts → Regression   |
    +------------------------------------------------------------------+
             |
             v
    +------------------------------------------------------------------+
    |                      PROMPT LIBRARY                               |
    |   templates/ | context/ | examples/ | benchmarks/                 |
    +------------------------------------------------------------------+
```

## 2.2 Data Flow

```
TEST GENERATION FLOW:
---------------------
User Input (scenario) 
    → Context Builder (loads prompts + context)
    → Claude API (Opus 4.5)
    → Output Parser (extracts code)
    → File Writer (saves test file)
    → Human Review

FAILURE ANALYSIS FLOW:
----------------------
Log File Input
    → Log Parser (extracts errors, traces)
    → Context Builder (loads analysis prompt)
    → Claude API (Sonnet 4.5)
    → Report Generator (formats output)
    → Markdown Report

PROMPT REGRESSION FLOW:
-----------------------
Prompt Change Detected
    → Load Benchmark Scenarios
    → Run Old Prompt (baseline)
    → Run New Prompt (candidate)
    → Score Both Outputs
    → Compare Scores
    → Pass/Fail Decision
```

## 2.3 Component Interaction

```
+------------------------------------------------------------------+
|                     COMPONENT RELATIONSHIPS                       |
+------------------------------------------------------------------+

                    +-------------------+
                    |    CLI (cli.py)   |
                    |    Entry Point    |
                    +---------+---------+
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
+----------------+  +----------------+  +----------------+
|   Generator    |  |   Analyzer     |  |   Regression   |
|   Module       |  |   Module       |  |   Module       |
+-------+--------+  +-------+--------+  +-------+--------+
        |                   |                   |
        +-------------------+-------------------+
                            |
                            v
                  +-------------------+
                  | Claude Client     |
                  | (API Wrapper)     |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  |  Anthropic API    |
                  |  (Claude Models)  |
                  +-------------------+


SHARED RESOURCES:
-----------------
All modules access:
├── prompts/templates/    (prompt files)
├── prompts/context/      (context files)
├── prompts/examples/     (few-shot examples)
├── prompts/benchmarks/   (regression scenarios)
└── config.py             (configuration)
```

---

# 3. Technology Stack

## 3.1 Required Dependencies

```toml
# pyproject.toml dependencies

[project]
name = "aitestkit"
version = "1.0.0"
description = "AI-Powered Test Development Toolkit"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.11"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["testing", "ai", "automation", "claude", "qa"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Testing",
]

dependencies = [
    "anthropic>=0.40.0",      # Claude API client
    "click>=8.1.0",           # CLI framework
    "pyyaml>=6.0",            # YAML parsing
    "rich>=13.0.0",           # Beautiful terminal output
    "pydantic>=2.0.0",        # Data validation
    "python-dotenv>=1.0.0",   # Environment variables
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "black>=24.0.0",
    "mypy>=1.0.0",
]

[project.scripts]
aitestkit = "aitestkit.cli:main"

[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.mypy]
python_version = "3.11"
strict = true
```

## 3.2 Python Version

- **Minimum:** Python 3.11
- **Recommended:** Python 3.12

## 3.3 External Services

| Service | Purpose | Cost |
|---------|---------|------|
| Anthropic API | Claude models | ~$5-20 for development |
| GitHub | Repository hosting | Free |
| GitHub Actions | CI/CD | Free tier |

---

# 4. Project Structure

## 4.1 Complete Directory Tree

```
aitestkit/
│
├── README.md                              # Project overview, badges, quick start
├── LICENSE                                # MIT License
├── pyproject.toml                         # Project configuration
├── .gitignore                             # Git ignore patterns
├── .env.example                           # Environment template
│
├── docs/                                  # Documentation
│   ├── architecture.md                    # System architecture
│   ├── getting-started.md                 # Setup guide
│   ├── prompt-engineering.md              # Prompt design guide
│   └── api-reference.md                   # CLI reference
│
├── src/
│   └── aitestkit/
│       ├── __init__.py                    # Package init, version
│       ├── cli.py                         # CLI entry point (Click)
│       ├── config.py                      # Configuration management
│       │
│       ├── generator/                     # Test Code Generation
│       │   ├── __init__.py
│       │   ├── generator.py               # Main generator class
│       │   ├── context_builder.py         # Builds prompts with context
│       │   └── output_parser.py           # Parses AI response
│       │
│       ├── analyzer/                      # Failure Analysis
│       │   ├── __init__.py
│       │   ├── analyzer.py                # Main analyzer class
│       │   ├── log_parser.py              # Extracts from logs
│       │   └── report_generator.py        # Creates reports
│       │
│       ├── regression/                    # Prompt Regression Testing
│       │   ├── __init__.py
│       │   ├── runner.py                  # Orchestrates regression
│       │   ├── scorer.py                  # Scores outputs
│       │   └── comparator.py              # Compares old vs new
│       │
│       ├── prompts/                       # Prompt Library
│       │   ├── templates/
│       │   │   ├── code_generation/
│       │   │   │   ├── system.md          # Main system prompt
│       │   │   │   ├── robot_framework.md # Robot-specific
│       │   │   │   ├── pytest.md          # Pytest-specific
│       │   │   │   └── playwright.md      # Playwright-specific
│       │   │   └── failure_analysis/
│       │   │       └── system.md          # Analysis prompt
│       │   │
│       │   ├── context/
│       │   │   ├── shared/
│       │   │   │   ├── testing_principles.md
│       │   │   │   └── coding_standards.md
│       │   │   └── sample_app/
│       │   │       └── api_reference.md
│       │   │
│       │   ├── examples/
│       │   │   ├── scenario_01_input.txt
│       │   │   ├── scenario_01_robot.robot
│       │   │   └── scenario_01_pytest.py
│       │   │
│       │   └── benchmarks/
│       │       ├── scenario_01_crud.yaml
│       │       ├── scenario_02_auth.yaml
│       │       ├── scenario_03_validation.yaml
│       │       ├── scenario_04_error.yaml
│       │       └── scenario_05_integration.yaml
│       │
│       └── utils/
│           ├── __init__.py
│           ├── claude_client.py           # Claude API wrapper
│           └── file_utils.py              # File operations
│
├── tests/                                 # Tests for the toolkit
│   ├── __init__.py
│   ├── conftest.py                        # Pytest fixtures
│   ├── test_generator.py
│   ├── test_analyzer.py
│   ├── test_regression.py
│   ├── test_claude_client.py
│   └── fixtures/
│       ├── sample_logs/
│       │   ├── timeout_failure.log
│       │   ├── assertion_failure.log
│       │   └── connection_failure.log
│       └── sample_scenarios/
│           └── test_scenario.yaml
│
├── sample_app/                            # Demo target application
│   ├── README.md
│   ├── requirements.txt
│   ├── main.py                            # FastAPI application
│   └── test_sample_app.py                 # Example tests
│
├── examples/                              # Usage examples
│   ├── 01_generate_robot_test.py
│   ├── 02_generate_pytest.py
│   ├── 03_analyze_failure.py
│   └── outputs/                           # Generated samples
│       ├── generated_test.robot
│       ├── generated_test.py
│       └── analysis_report.md
│
├── scripts/
│   ├── setup.sh                           # Initial setup
│   └── demo.sh                            # Run full demo
│
└── .github/
    └── workflows/
        ├── test.yml                       # Run tests on PR
        ├── prompt-regression.yml          # Validate prompts
        └── release.yml                    # Publish releases
```

## 4.2 Key Files Description

| File | Purpose | Priority |
|------|---------|----------|
| `cli.py` | Entry point, all commands | High |
| `claude_client.py` | API wrapper, model selection | High |
| `generator.py` | Test code generation | High |
| `analyzer.py` | Failure analysis | High |
| `runner.py` | Prompt regression | Medium |
| `system.md` (code_gen) | Main generation prompt | High |
| `system.md` (analysis) | Main analysis prompt | High |
| `config.py` | Settings management | High |

---

# 5. Core Components

## 5.1 Claude Client (`utils/claude_client.py`)

```python
"""
Claude API client wrapper for AITestKit.
Handles model selection, API calls, error handling, and usage tracking.
"""

import os
from typing import Literal, Optional
from anthropic import Anthropic
from pydantic import BaseModel

ModelType = Literal["opus", "sonnet", "haiku"]


class UsageStats(BaseModel):
    """Track API usage for cost estimation."""
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


class ClaudeClient:
    """
    Wrapper for Anthropic Claude API.
    
    Supports three models:
    - opus: Best quality, use for code generation
    - sonnet: Balanced, use for analysis
    - haiku: Fast/cheap, use for regression testing
    """
    
    MODELS = {
        "opus": "claude-opus-4-5-20250514",
        "sonnet": "claude-sonnet-4-5-20250514",
        "haiku": "claude-haiku-4-5-20250514",
    }
    
    # Pricing per 1M tokens (as of Jan 2025)
    PRICING = {
        "opus": {"input": 5.00, "output": 25.00},
        "sonnet": {"input": 3.00, "output": 15.00},
        "haiku": {"input": 1.00, "output": 5.00},
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize client.
        
        Args:
            api_key: Anthropic API key. If None, reads from ANTHROPIC_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.client = Anthropic(api_key=self.api_key)
        self.usage_history: list[UsageStats] = []
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: ModelType = "sonnet",
        max_tokens: int = 4096,
        temperature: float = 0.3,
    ) -> str:
        """
        Generate response from Claude.
        
        Args:
            system_prompt: System instructions
            user_prompt: User message
            model: "opus", "sonnet", or "haiku"
            max_tokens: Maximum response length
            temperature: Randomness (0.0-1.0)
        
        Returns:
            Generated text response
        """
        model_id = self.MODELS.get(model, self.MODELS["sonnet"])
        
        response = self.client.messages.create(
            model=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        
        # Track usage
        self._track_usage(model, response.usage)
        
        return response.content[0].text
    
    def generate_code(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 8192,
    ) -> str:
        """Generate code using Opus (best quality)."""
        return self.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="opus",
            max_tokens=max_tokens,
            temperature=0.2,  # Lower for more consistent code
        )
    
    def analyze(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> str:
        """Analyze using Sonnet (balanced)."""
        return self.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="sonnet",
            max_tokens=max_tokens,
            temperature=0.4,
        )
    
    def quick_check(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2048,
    ) -> str:
        """Quick check using Haiku (fast/cheap)."""
        return self.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="haiku",
            max_tokens=max_tokens,
            temperature=0.2,
        )
    
    def _track_usage(self, model: str, usage) -> None:
        """Track API usage for cost estimation."""
        pricing = self.PRICING[model]
        cost = (
            (usage.input_tokens / 1_000_000) * pricing["input"] +
            (usage.output_tokens / 1_000_000) * pricing["output"]
        )
        
        stats = UsageStats(
            model=model,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            cost_usd=cost,
        )
        self.usage_history.append(stats)
    
    def get_total_cost(self) -> float:
        """Get total cost of all API calls in this session."""
        return sum(stats.cost_usd for stats in self.usage_history)
    
    def get_usage_summary(self) -> dict:
        """Get usage summary by model."""
        summary = {}
        for stats in self.usage_history:
            if stats.model not in summary:
                summary[stats.model] = {
                    "calls": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost_usd": 0.0,
                }
            summary[stats.model]["calls"] += 1
            summary[stats.model]["input_tokens"] += stats.input_tokens
            summary[stats.model]["output_tokens"] += stats.output_tokens
            summary[stats.model]["cost_usd"] += stats.cost_usd
        return summary
```

## 5.2 Configuration (`config.py`)

```python
"""
Configuration management for AITestKit.
Loads settings from environment variables and config files.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()


class ModelConfig(BaseModel):
    """Configuration for a specific model."""
    name: str
    temperature: float = 0.3
    max_tokens: int = 4096


class Config(BaseModel):
    """Main configuration for AITestKit."""
    
    # API Configuration
    anthropic_api_key: Optional[str] = None
    
    # Model Configuration
    code_generation_model: str = "opus"
    analysis_model: str = "sonnet"
    regression_model: str = "haiku"
    
    # Paths
    prompts_dir: Path = Path("src/aitestkit/prompts")
    output_dir: Path = Path("./output")
    
    # Generation Settings
    default_framework: str = "pytest"
    
    # Regression Settings
    regression_threshold: int = 85  # Minimum passing score
    regression_tolerance: int = 5   # Max allowed score drop
    
    @classmethod
    def load(cls) -> "Config":
        """Load configuration from environment."""
        return cls(
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
            prompts_dir=Path(os.environ.get("AITESTKIT_PROMPTS_DIR", "src/aitestkit/prompts")),
            output_dir=Path(os.environ.get("AITESTKIT_OUTPUT_DIR", "./output")),
            default_framework=os.environ.get("AITESTKIT_DEFAULT_FRAMEWORK", "pytest"),
        )


# Global config instance
config = Config.load()
```

---

# 6. Claude API Integration

## 6.1 Model Selection Strategy

| Task | Model | Why |
|------|-------|-----|
| **Code Generation** | Claude Opus 4.5 | Best coding quality (80.9% SWE-bench) |
| **Failure Analysis** | Claude Sonnet 4.5 | Good analysis, reasonable cost |
| **Prompt Regression** | Claude Haiku 4.5 | Fast, cheap, high volume |

## 6.2 API Call Patterns

```python
# Pattern 1: Code Generation (Opus)
response = client.generate_code(
    system_prompt=code_gen_system_prompt,
    user_prompt=f"Generate a {framework} test for: {scenario}",
    max_tokens=8192,
)

# Pattern 2: Analysis (Sonnet)
response = client.analyze(
    system_prompt=analysis_system_prompt,
    user_prompt=f"Analyze this failure:\n\n{log_content}",
    max_tokens=4096,
)

# Pattern 3: Regression (Haiku)
response = client.quick_check(
    system_prompt=code_gen_system_prompt,
    user_prompt=f"Generate a {framework} test for: {scenario}",
    max_tokens=4096,
)
```

## 6.3 Error Handling

```python
from anthropic import APIError, RateLimitError, AuthenticationError

try:
    response = client.generate(...)
except AuthenticationError:
    print("Invalid API key. Check ANTHROPIC_API_KEY.")
    sys.exit(1)
except RateLimitError:
    print("Rate limited. Waiting 60 seconds...")
    time.sleep(60)
    response = client.generate(...)  # Retry
except APIError as e:
    print(f"API error: {e}")
    raise
```

---

# 7. Prompt Templates

## 7.1 Code Generation System Prompt

**File:** `src/aitestkit/prompts/templates/code_generation/system.md`

```markdown
# Role

You are an expert Senior QA Engineer specializing in test automation. You write clean, maintainable, and comprehensive test code.

# Task

Generate a complete, executable test file based on the user's scenario description.

# Framework Instructions

You will receive a framework specification. Follow these framework-specific guidelines:

## For Robot Framework (.robot):
- Use proper Robot Framework syntax
- Include *** Settings ***, *** Variables ***, *** Test Cases ***, *** Keywords *** sections
- Use BDD style (Given/When/Then) for test cases
- Include proper documentation and tags

## For Pytest (.py):
- Use pytest conventions and fixtures
- Include proper docstrings
- Use descriptive test function names (test_*)
- Include appropriate assertions with messages

## For Playwright (.spec.ts):
- Use TypeScript with Playwright test runner
- Include proper page object patterns where appropriate
- Use async/await properly
- Include meaningful test descriptions

# Constraints

DO:
- Include comprehensive assertions
- Add error handling where appropriate
- Use descriptive names
- Include documentation/comments
- Follow the specific framework's best practices
- Make tests independent and repeatable

DO NOT:
- Use hardcoded waits (time.sleep, etc.) - use explicit waits
- Leave placeholder comments like "# TODO"
- Generate incomplete code
- Include external dependencies not specified

# Output Format

Return ONLY the test code. Do not include explanations before or after.
Start directly with the code.
At the end, add a comment with the suggested filename.

Example ending:
```
# Suggested filename: test_user_login.py
```
```

## 7.2 Robot Framework Specific Prompt

**File:** `src/aitestkit/prompts/templates/code_generation/robot_framework.md`

```markdown
# Robot Framework Specific Guidelines

## Structure

```robotframework
*** Settings ***
Documentation    Brief description of test suite
Library          RequestsLibrary    # For API tests
Library          Browser            # For UI tests
Library          Collections
Resource         common.resource
Suite Setup      Setup Suite
Suite Teardown   Teardown Suite
Test Tags        smoke    api

*** Variables ***
${BASE_URL}      http://localhost:8000
${TIMEOUT}       30s

*** Test Cases ***
Test Case Name Should Describe Expected Behavior
    [Documentation]    Detailed description
    [Tags]    critical    positive
    Given Precondition Is Met
    When Action Is Performed
    Then Expected Result Should Occur

*** Keywords ***
Custom Keyword Name
    [Documentation]    What this keyword does
    [Arguments]    ${arg1}    ${arg2}=default
    # Implementation
    RETURN    ${result}
```

## Best Practices

- Use 4 spaces for indentation
- Separate sections with blank lines
- Use meaningful variable names in ${UPPER_CASE}
- Keywords should be action-oriented verbs
- Tags should categorize: smoke, regression, critical, api, ui
```

## 7.3 Pytest Specific Prompt

**File:** `src/aitestkit/prompts/templates/code_generation/pytest.md`

```markdown
# Pytest Specific Guidelines

## Structure

```python
"""
Test module description.
"""

import pytest
from typing import Generator
# Other imports


class TestFeatureName:
    """Tests for specific feature."""
    
    @pytest.fixture
    def setup_data(self) -> Generator[dict, None, None]:
        """Set up test data."""
        data = {"key": "value"}
        yield data
        # Cleanup if needed
    
    def test_should_do_something_when_condition(self, setup_data: dict) -> None:
        """Test description explaining what and why."""
        # Arrange
        expected = "expected_value"
        
        # Act
        result = function_under_test(setup_data)
        
        # Assert
        assert result == expected, f"Expected {expected}, got {result}"
    
    @pytest.mark.parametrize("input_val,expected", [
        ("input1", "output1"),
        ("input2", "output2"),
    ])
    def test_with_multiple_inputs(self, input_val: str, expected: str) -> None:
        """Test with parameterized inputs."""
        result = function_under_test(input_val)
        assert result == expected
```

## Best Practices

- Use type hints
- Follow AAA pattern (Arrange, Act, Assert)
- Use fixtures for setup/teardown
- Descriptive test names: test_should_X_when_Y
- Include assertion messages
```

## 7.4 Failure Analysis System Prompt

**File:** `src/aitestkit/prompts/templates/failure_analysis/system.md`

```markdown
# Role

You are an expert QA Engineer and debugging specialist. You excel at analyzing test failures and identifying root causes quickly and accurately.

# Task

Analyze the provided test failure information and generate a comprehensive analysis report.

# Input

You will receive:
- Error message and stack trace
- Test log output
- Any additional context (test name, recent changes, etc.)

# Analysis Process

1. **Identify the Error Type**
   - Assertion failure
   - Timeout
   - Connection error
   - Element not found
   - Exception/crash

2. **Determine Root Cause**
   - Code bug (test or application)
   - Environment issue
   - Data issue
   - Timing/race condition
   - Configuration problem

3. **Assess Confidence**
   - High (>80%): Clear evidence points to cause
   - Medium (50-80%): Likely cause but some uncertainty
   - Low (<50%): Multiple possible causes

4. **Suggest Fixes**
   - Immediate actions
   - Investigation steps
   - Prevention measures

# Output Format

Generate a Markdown report with this structure:

```markdown
# Failure Analysis Report

**Test:** [Test name]
**Status:** FAILED
**Analyzed:** [Timestamp]

## Summary
[One-line summary of the failure]

## Root Cause Analysis

**Probable Cause:** [Description]
**Confidence:** [High/Medium/Low] ([percentage]%)

### Evidence
- [Evidence point 1]
- [Evidence point 2]
- [Evidence point 3]

## Category

[Code Bug | Environment Issue | Test Flaky | Data Issue | Configuration]

## Suggested Actions

### Immediate
1. [Action 1]
2. [Action 2]

### Investigation
1. [Investigation step 1]
2. [Investigation step 2]

### Prevention
1. [Prevention measure 1]
```

# Constraints

- Be specific and actionable
- Don't guess without evidence
- Acknowledge uncertainty when present
- Prioritize the most likely cause
```

---

# 8. CLI Specification

## 8.1 CLI Structure (`cli.py`)

```python
"""
AITestKit Command Line Interface.

Usage:
    aitestkit generate --framework pytest "Test user can login"
    aitestkit analyze ./failed_test.log
    aitestkit regression --all
"""

import click
from rich.console import Console
from rich.panel import Panel
from pathlib import Path

from aitestkit import __version__
from aitestkit.generator import TestGenerator
from aitestkit.analyzer import FailureAnalyzer
from aitestkit.regression import RegressionRunner
from aitestkit.config import config

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="aitestkit")
def main():
    """AITestKit - AI-Powered Test Development Toolkit"""
    pass


@main.command()
@click.argument("scenario", type=str)
@click.option(
    "--framework", "-f",
    type=click.Choice(["robot", "pytest", "playwright"]),
    default="pytest",
    help="Test framework to generate for"
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default="./output",
    help="Output directory for generated test"
)
@click.option(
    "--context", "-c",
    type=click.Path(exists=True),
    default=None,
    help="Additional context file (API docs, etc.)"
)
def generate(scenario: str, framework: str, output: str, context: str | None):
    """
    Generate test code from a natural language scenario.
    
    Example:
        aitestkit generate "Test user can create a new todo item" -f pytest
    """
    console.print(Panel(f"[bold blue]Generating {framework} test...[/bold blue]"))
    
    generator = TestGenerator()
    result = generator.generate(
        scenario=scenario,
        framework=framework,
        context_file=Path(context) if context else None,
    )
    
    # Save output
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    file_path = output_path / result.suggested_filename
    file_path.write_text(result.code)
    
    console.print(f"[green]✓[/green] Generated: {file_path}")
    console.print(f"[dim]Tokens used: {result.tokens_used}[/dim]")
    console.print(f"[dim]Cost: ${result.cost:.4f}[/dim]")


@main.command()
@click.argument("log_file", type=click.Path(exists=True))
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Output file for analysis report"
)
@click.option(
    "--format", "-f",
    type=click.Choice(["markdown", "json", "console"]),
    default="console",
    help="Output format"
)
def analyze(log_file: str, output: str | None, format: str):
    """
    Analyze a test failure and generate insights.
    
    Example:
        aitestkit analyze ./logs/failed_test.log
        aitestkit analyze ./logs/failed_test.log -o report.md -f markdown
    """
    console.print(Panel("[bold red]Analyzing failure...[/bold red]"))
    
    analyzer = FailureAnalyzer()
    log_content = Path(log_file).read_text()
    
    result = analyzer.analyze(log_content)
    
    if format == "console":
        # Rich formatted output
        console.print(result.to_rich_panel())
    elif format == "markdown":
        report = result.to_markdown()
        if output:
            Path(output).write_text(report)
            console.print(f"[green]✓[/green] Report saved: {output}")
        else:
            console.print(report)
    elif format == "json":
        import json
        json_output = json.dumps(result.to_dict(), indent=2)
        if output:
            Path(output).write_text(json_output)
            console.print(f"[green]✓[/green] Report saved: {output}")
        else:
            console.print(json_output)


@main.command()
@click.option(
    "--prompt", "-p",
    type=click.Path(exists=True),
    default=None,
    help="Specific prompt file to test"
)
@click.option(
    "--all", "-a",
    is_flag=True,
    default=False,
    help="Run regression on all prompts"
)
@click.option(
    "--baseline", "-b",
    type=str,
    default="main",
    help="Git branch/commit for baseline comparison"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    default=False,
    help="Show detailed output"
)
def regression(prompt: str | None, all: bool, baseline: str, verbose: bool):
    """
    Run prompt regression tests.
    
    Example:
        aitestkit regression --all
        aitestkit regression --prompt ./prompts/system.md
    """
    console.print(Panel("[bold yellow]Running prompt regression...[/bold yellow]"))
    
    runner = RegressionRunner()
    
    if all:
        results = runner.run_all(baseline_ref=baseline)
    elif prompt:
        results = runner.run_single(Path(prompt), baseline_ref=baseline)
    else:
        console.print("[red]Error: Specify --prompt or --all[/red]")
        return
    
    # Display results
    runner.display_results(results, verbose=verbose)
    
    # Exit with appropriate code
    if not results.passed:
        raise SystemExit(1)


@main.command()
def info():
    """Show configuration and status information."""
    console.print(Panel("[bold]AITestKit Configuration[/bold]"))
    console.print(f"Version: {__version__}")
    console.print(f"Prompts directory: {config.prompts_dir}")
    console.print(f"Output directory: {config.output_dir}")
    console.print(f"Default framework: {config.default_framework}")
    console.print(f"API key configured: {'✓' if config.anthropic_api_key else '✗'}")


if __name__ == "__main__":
    main()
```

## 8.2 Command Summary

| Command | Description | Example |
|---------|-------------|---------|
| `generate` | Generate test code | `aitestkit generate "scenario" -f pytest` |
| `analyze` | Analyze failure | `aitestkit analyze ./log.txt` |
| `regression` | Validate prompts | `aitestkit regression --all` |
| `info` | Show config | `aitestkit info` |

---

# 9. Test Generator

## 9.1 Generator Class (`generator/generator.py`)

```python
"""
Test code generator using Claude API.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from aitestkit.utils.claude_client import ClaudeClient
from aitestkit.generator.context_builder import ContextBuilder
from aitestkit.generator.output_parser import OutputParser


@dataclass
class GenerationResult:
    """Result of test generation."""
    code: str
    framework: str
    suggested_filename: str
    tokens_used: int
    cost: float
    raw_response: str


class TestGenerator:
    """
    Generates test code from natural language scenarios.
    
    Uses Claude Opus 4.5 for best code quality.
    """
    
    def __init__(self, client: Optional[ClaudeClient] = None):
        self.client = client or ClaudeClient()
        self.context_builder = ContextBuilder()
        self.output_parser = OutputParser()
    
    def generate(
        self,
        scenario: str,
        framework: str = "pytest",
        context_file: Optional[Path] = None,
    ) -> GenerationResult:
        """
        Generate test code for a scenario.
        
        Args:
            scenario: Natural language test description
            framework: Target framework (robot, pytest, playwright)
            context_file: Optional additional context (API docs, etc.)
        
        Returns:
            GenerationResult with code and metadata
        """
        # Build prompts
        system_prompt = self.context_builder.build_system_prompt(framework)
        user_prompt = self.context_builder.build_user_prompt(
            scenario=scenario,
            framework=framework,
            context_file=context_file,
        )
        
        # Generate with Opus (best quality)
        response = self.client.generate_code(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
        
        # Parse output
        code = self.output_parser.extract_code(response, framework)
        filename = self.output_parser.extract_filename(response, framework)
        
        # Get usage stats
        usage = self.client.usage_history[-1] if self.client.usage_history else None
        
        return GenerationResult(
            code=code,
            framework=framework,
            suggested_filename=filename,
            tokens_used=usage.input_tokens + usage.output_tokens if usage else 0,
            cost=usage.cost_usd if usage else 0.0,
            raw_response=response,
        )
```

## 9.2 Context Builder (`generator/context_builder.py`)

```python
"""
Builds prompts with appropriate context for test generation.
"""

from pathlib import Path
from typing import Optional

from aitestkit.config import config


class ContextBuilder:
    """Builds system and user prompts with context."""
    
    def __init__(self, prompts_dir: Optional[Path] = None):
        self.prompts_dir = prompts_dir or config.prompts_dir
    
    def build_system_prompt(self, framework: str) -> str:
        """
        Build system prompt for code generation.
        
        Combines:
        - Base system prompt
        - Framework-specific prompt
        - Shared context (principles, standards)
        """
        # Load base system prompt
        system_path = self.prompts_dir / "templates" / "code_generation" / "system.md"
        system_prompt = system_path.read_text()
        
        # Load framework-specific prompt
        framework_path = self.prompts_dir / "templates" / "code_generation" / f"{framework}.md"
        if framework_path.exists():
            framework_prompt = framework_path.read_text()
            system_prompt += f"\n\n# Framework Specific\n\n{framework_prompt}"
        
        # Load shared context
        context_dir = self.prompts_dir / "context" / "shared"
        if context_dir.exists():
            for context_file in context_dir.glob("*.md"):
                context = context_file.read_text()
                system_prompt += f"\n\n# {context_file.stem}\n\n{context}"
        
        return system_prompt
    
    def build_user_prompt(
        self,
        scenario: str,
        framework: str,
        context_file: Optional[Path] = None,
    ) -> str:
        """
        Build user prompt with scenario and optional context.
        """
        prompt_parts = [
            f"Framework: {framework}",
            f"\nScenario:\n{scenario}",
        ]
        
        # Add optional context
        if context_file and context_file.exists():
            context = context_file.read_text()
            prompt_parts.append(f"\nAdditional Context:\n{context}")
        
        # Add few-shot examples if available
        examples = self._load_examples(framework)
        if examples:
            prompt_parts.append(f"\nExamples of good output:\n{examples}")
        
        return "\n".join(prompt_parts)
    
    def _load_examples(self, framework: str) -> str:
        """Load few-shot examples for the framework."""
        examples_dir = self.prompts_dir / "examples"
        examples = []
        
        extension_map = {
            "robot": ".robot",
            "pytest": ".py",
            "playwright": ".spec.ts",
        }
        ext = extension_map.get(framework, ".py")
        
        for example_file in examples_dir.glob(f"*{ext}"):
            examples.append(f"```\n{example_file.read_text()}\n```")
        
        return "\n\n".join(examples[:2])  # Limit to 2 examples
```

## 9.3 Output Parser (`generator/output_parser.py`)

```python
"""
Parses AI output to extract code and metadata.
"""

import re
from typing import Optional


class OutputParser:
    """Parses and validates generated test code."""
    
    EXTENSION_MAP = {
        "robot": ".robot",
        "pytest": ".py",
        "playwright": ".spec.ts",
    }
    
    def extract_code(self, response: str, framework: str) -> str:
        """
        Extract code from AI response.
        
        Handles:
        - Code blocks (```python ... ```)
        - Raw code
        - Removes explanations
        """
        # Try to extract from code block
        pattern = r"```(?:\w+)?\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        
        if matches:
            # Return the largest code block (likely the main code)
            return max(matches, key=len).strip()
        
        # If no code block, assume entire response is code
        # Remove common explanation patterns
        code = response
        code = re.sub(r"^Here's.*?:\n+", "", code, flags=re.IGNORECASE)
        code = re.sub(r"^This test.*?:\n+", "", code, flags=re.IGNORECASE)
        
        return code.strip()
    
    def extract_filename(self, response: str, framework: str) -> str:
        """
        Extract suggested filename from response.
        
        Looks for pattern: # Suggested filename: xyz.py
        """
        pattern = r"#\s*Suggested filename:\s*(\S+)"
        match = re.search(pattern, response, re.IGNORECASE)
        
        if match:
            return match.group(1)
        
        # Generate default filename
        ext = self.EXTENSION_MAP.get(framework, ".py")
        return f"generated_test{ext}"
    
    def validate_code(self, code: str, framework: str) -> list[str]:
        """
        Validate generated code structure.
        
        Returns list of validation issues (empty if valid).
        """
        issues = []
        
        if framework == "robot":
            if "*** Test Cases ***" not in code:
                issues.append("Missing *** Test Cases *** section")
            if "*** Settings ***" not in code:
                issues.append("Missing *** Settings *** section")
        
        elif framework == "pytest":
            if "def test_" not in code:
                issues.append("Missing test function (def test_*)")
            if "assert" not in code:
                issues.append("Missing assertions")
        
        elif framework == "playwright":
            if "test(" not in code and "test.describe(" not in code:
                issues.append("Missing test() or test.describe()")
            if "expect(" not in code:
                issues.append("Missing expect() assertions")
        
        return issues
```

---

# 10. Failure Analyzer

## 10.1 Analyzer Class (`analyzer/analyzer.py`)

```python
"""
Test failure analyzer using Claude API.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum
from pathlib import Path

from rich.panel import Panel
from rich.table import Table

from aitestkit.utils.claude_client import ClaudeClient
from aitestkit.analyzer.log_parser import LogParser
from aitestkit.config import config


class FailureCategory(Enum):
    """Categories of test failures."""
    CODE_BUG = "Code Bug"
    ENVIRONMENT = "Environment Issue"
    TEST_FLAKY = "Test Flaky"
    DATA_ISSUE = "Data Issue"
    CONFIGURATION = "Configuration"
    UNKNOWN = "Unknown"


class Confidence(Enum):
    """Confidence levels for analysis."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass
class AnalysisResult:
    """Result of failure analysis."""
    test_name: str
    error_summary: str
    root_cause: str
    confidence: Confidence
    confidence_percent: int
    category: FailureCategory
    evidence: list[str]
    suggested_actions: list[str]
    investigation_steps: list[str]
    raw_response: str
    
    def to_markdown(self) -> str:
        """Convert to Markdown report."""
        evidence_list = "\n".join(f"- {e}" for e in self.evidence)
        actions_list = "\n".join(f"{i+1}. {a}" for i, a in enumerate(self.suggested_actions))
        investigation_list = "\n".join(f"{i+1}. {s}" for i, s in enumerate(self.investigation_steps))
        
        return f"""# Failure Analysis Report

**Test:** {self.test_name}
**Status:** FAILED
**Category:** {self.category.value}

## Summary
{self.error_summary}

## Root Cause Analysis

**Probable Cause:** {self.root_cause}
**Confidence:** {self.confidence.value} ({self.confidence_percent}%)

### Evidence
{evidence_list}

## Suggested Actions

### Immediate
{actions_list}

### Investigation
{investigation_list}
"""
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "test_name": self.test_name,
            "error_summary": self.error_summary,
            "root_cause": self.root_cause,
            "confidence": self.confidence.value,
            "confidence_percent": self.confidence_percent,
            "category": self.category.value,
            "evidence": self.evidence,
            "suggested_actions": self.suggested_actions,
            "investigation_steps": self.investigation_steps,
        }
    
    def to_rich_panel(self) -> Panel:
        """Convert to Rich panel for console output."""
        content = f"""[bold]Test:[/bold] {self.test_name}
[bold]Category:[/bold] {self.category.value}

[bold red]Root Cause:[/bold red] {self.root_cause}
[bold]Confidence:[/bold] {self.confidence.value} ({self.confidence_percent}%)

[bold]Evidence:[/bold]
""" + "\n".join(f"  • {e}" for e in self.evidence) + """

[bold green]Suggested Actions:[/bold green]
""" + "\n".join(f"  {i+1}. {a}" for i, a in enumerate(self.suggested_actions))
        
        return Panel(content, title="[bold]Failure Analysis[/bold]", border_style="red")


class FailureAnalyzer:
    """
    Analyzes test failures using Claude API.
    
    Uses Claude Sonnet 4.5 for balanced analysis.
    """
    
    def __init__(self, client: Optional[ClaudeClient] = None):
        self.client = client or ClaudeClient()
        self.log_parser = LogParser()
    
    def analyze(self, log_content: str, test_name: Optional[str] = None) -> AnalysisResult:
        """
        Analyze a test failure.
        
        Args:
            log_content: Raw log content or error message
            test_name: Optional test name (extracted from log if not provided)
        
        Returns:
            AnalysisResult with root cause and suggestions
        """
        # Parse log to extract key information
        parsed = self.log_parser.parse(log_content)
        test_name = test_name or parsed.test_name or "Unknown Test"
        
        # Load analysis prompt
        system_prompt = self._load_system_prompt()
        
        # Build user prompt
        user_prompt = self._build_user_prompt(log_content, parsed)
        
        # Analyze with Sonnet
        response = self.client.analyze(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
        
        # Parse response
        return self._parse_response(response, test_name)
    
    def _load_system_prompt(self) -> str:
        """Load the failure analysis system prompt."""
        prompt_path = config.prompts_dir / "templates" / "failure_analysis" / "system.md"
        return prompt_path.read_text()
    
    def _build_user_prompt(self, log_content: str, parsed) -> str:
        """Build user prompt with log content and extracted info."""
        return f"""Analyze this test failure:

Error Type: {parsed.error_type or 'Unknown'}
Error Message: {parsed.error_message or 'See full log'}

Full Log:
```
{log_content}
```

Provide a detailed analysis following the specified format."""
    
    def _parse_response(self, response: str, test_name: str) -> AnalysisResult:
        """Parse Claude's response into AnalysisResult."""
        # Extract sections from markdown response
        import re
        
        # Extract root cause
        root_cause_match = re.search(
            r"\*\*Probable Cause:\*\*\s*(.+?)(?:\n|$)", response
        )
        root_cause = root_cause_match.group(1) if root_cause_match else "Unknown"
        
        # Extract confidence
        confidence_match = re.search(
            r"\*\*Confidence:\*\*\s*(\w+)\s*\((\d+)%\)", response
        )
        if confidence_match:
            conf_str = confidence_match.group(1).upper()
            conf_percent = int(confidence_match.group(2))
            confidence = Confidence[conf_str] if conf_str in Confidence.__members__ else Confidence.MEDIUM
        else:
            confidence = Confidence.MEDIUM
            conf_percent = 50
        
        # Extract category
        category = FailureCategory.UNKNOWN
        for cat in FailureCategory:
            if cat.value.lower() in response.lower():
                category = cat
                break
        
        # Extract evidence (bullet points after "Evidence")
        evidence = []
        evidence_match = re.search(r"### Evidence\n((?:- .+\n?)+)", response)
        if evidence_match:
            evidence = [
                line.strip("- ").strip()
                for line in evidence_match.group(1).split("\n")
                if line.strip().startswith("-")
            ]
        
        # Extract suggested actions
        actions = []
        actions_match = re.search(r"### Immediate\n((?:\d+\. .+\n?)+)", response)
        if actions_match:
            actions = [
                re.sub(r"^\d+\.\s*", "", line).strip()
                for line in actions_match.group(1).split("\n")
                if re.match(r"^\d+\.", line.strip())
            ]
        
        # Extract investigation steps
        investigation = []
        inv_match = re.search(r"### Investigation\n((?:\d+\. .+\n?)+)", response)
        if inv_match:
            investigation = [
                re.sub(r"^\d+\.\s*", "", line).strip()
                for line in inv_match.group(1).split("\n")
                if re.match(r"^\d+\.", line.strip())
            ]
        
        # Extract summary
        summary_match = re.search(r"## Summary\n(.+?)(?:\n\n|$)", response, re.DOTALL)
        summary = summary_match.group(1).strip() if summary_match else "Analysis complete"
        
        return AnalysisResult(
            test_name=test_name,
            error_summary=summary,
            root_cause=root_cause,
            confidence=confidence,
            confidence_percent=conf_percent,
            category=category,
            evidence=evidence or ["See full analysis"],
            suggested_actions=actions or ["Review the error details"],
            investigation_steps=investigation or ["Check logs for more context"],
            raw_response=response,
        )
```

## 10.2 Log Parser (`analyzer/log_parser.py`)

```python
"""
Parses test log files to extract relevant information.
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedLog:
    """Parsed log information."""
    test_name: Optional[str]
    error_type: Optional[str]
    error_message: Optional[str]
    stack_trace: Optional[str]
    timestamp: Optional[str]


class LogParser:
    """Parses various test log formats."""
    
    # Common error patterns
    ERROR_PATTERNS = [
        r"(?:Error|Exception|Failure):\s*(.+)",
        r"AssertionError:\s*(.+)",
        r"TimeoutError:\s*(.+)",
        r"ConnectionError:\s*(.+)",
        r"FAILED\s+(.+)",
    ]
    
    # Test name patterns
    TEST_NAME_PATTERNS = [
        r"test_(\w+)",
        r"Test Case:\s*(.+)",
        r"FAILED\s+(test_\w+)",
        r"(\w+::\w+::\w+)",  # pytest format
    ]
    
    def parse(self, log_content: str) -> ParsedLog:
        """
        Parse log content to extract key information.
        
        Args:
            log_content: Raw log text
        
        Returns:
            ParsedLog with extracted information
        """
        return ParsedLog(
            test_name=self._extract_test_name(log_content),
            error_type=self._extract_error_type(log_content),
            error_message=self._extract_error_message(log_content),
            stack_trace=self._extract_stack_trace(log_content),
            timestamp=self._extract_timestamp(log_content),
        )
    
    def _extract_test_name(self, content: str) -> Optional[str]:
        """Extract test name from log."""
        for pattern in self.TEST_NAME_PATTERNS:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
        return None
    
    def _extract_error_type(self, content: str) -> Optional[str]:
        """Extract error type (Exception class name)."""
        # Look for Python exception types
        match = re.search(r"(\w+Error|\w+Exception):", content)
        if match:
            return match.group(1)
        
        # Look for generic failure indicators
        if "TIMEOUT" in content.upper():
            return "TimeoutError"
        if "CONNECTION" in content.upper():
            return "ConnectionError"
        if "ASSERT" in content.upper():
            return "AssertionError"
        
        return None
    
    def _extract_error_message(self, content: str) -> Optional[str]:
        """Extract error message."""
        for pattern in self.ERROR_PATTERNS:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_stack_trace(self, content: str) -> Optional[str]:
        """Extract stack trace if present."""
        # Look for Python traceback
        match = re.search(
            r"Traceback \(most recent call last\):(.+?)(?:\n\n|\Z)",
            content,
            re.DOTALL
        )
        if match:
            return match.group(0).strip()
        return None
    
    def _extract_timestamp(self, content: str) -> Optional[str]:
        """Extract timestamp from log."""
        # Common timestamp patterns
        patterns = [
            r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}",
            r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}",
        ]
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(0)
        return None
```

---

# 11. Prompt Regression

## 11.1 Benchmark Scenario Format

**File:** `src/aitestkit/prompts/benchmarks/scenario_01_crud.yaml`

```yaml
# Benchmark scenario for CRUD operations testing

scenario_id: "crud_001"
name: "CRUD Operations - Create Item"
description: "Test creating a new item via API"
framework: pytest

input:
  scenario: |
    Test that a user can create a new todo item.
    1. Send POST request to /todos with title and description
    2. Verify response status is 201
    3. Verify response contains the created item with an ID
    4. Verify the item can be retrieved with GET /todos/{id}

expected_elements:
  must_contain:
    - "def test_"
    - "assert"
    - "POST"
    - "/todos"
    - "201"
    - "id"
  
  must_not_contain:
    - "time.sleep"
    - "TODO"
    - "pass  # "
  
  structure:
    has_docstring: true
    has_assertions: true
    min_assertions: 2

quality_checks:
  - name: "No hardcoded waits"
    pattern: "time\\.sleep|sleep\\("
    should_match: false
  
  - name: "Has type hints"
    pattern: "def test_\\w+\\([^)]*:\\s*\\w+"
    should_match: true
  
  - name: "Has assertion messages"
    pattern: 'assert .+, ["\']'
    should_match: true

baseline_score: 85
```

## 11.2 Scorer (`regression/scorer.py`)

```python
"""
Scores generated test code against expected criteria.
"""

import re
from dataclasses import dataclass
from typing import Optional
import yaml
from pathlib import Path


@dataclass
class ScoreBreakdown:
    """Detailed score breakdown."""
    structural: int      # /40 points
    content: int         # /40 points
    quality: int         # /20 points
    total: int           # /100 points
    details: list[str]   # Individual check results


@dataclass
class BenchmarkScenario:
    """Loaded benchmark scenario."""
    scenario_id: str
    name: str
    description: str
    framework: str
    input_scenario: str
    expected_elements: dict
    quality_checks: list[dict]
    baseline_score: int


class Scorer:
    """Scores generated code against benchmark criteria."""
    
    def load_scenario(self, path: Path) -> BenchmarkScenario:
        """Load a benchmark scenario from YAML."""
        data = yaml.safe_load(path.read_text())
        
        return BenchmarkScenario(
            scenario_id=data["scenario_id"],
            name=data["name"],
            description=data.get("description", ""),
            framework=data["framework"],
            input_scenario=data["input"]["scenario"],
            expected_elements=data.get("expected_elements", {}),
            quality_checks=data.get("quality_checks", []),
            baseline_score=data.get("baseline_score", 85),
        )
    
    def score(self, code: str, scenario: BenchmarkScenario) -> ScoreBreakdown:
        """
        Score generated code against scenario criteria.
        
        Args:
            code: Generated test code
            scenario: Benchmark scenario with expectations
        
        Returns:
            ScoreBreakdown with points and details
        """
        details = []
        
        # Structural score (40 points)
        structural = self._score_structural(code, scenario, details)
        
        # Content score (40 points)
        content = self._score_content(code, scenario, details)
        
        # Quality score (20 points)
        quality = self._score_quality(code, scenario, details)
        
        total = structural + content + quality
        
        return ScoreBreakdown(
            structural=structural,
            content=content,
            quality=quality,
            total=total,
            details=details,
        )
    
    def _score_structural(
        self,
        code: str,
        scenario: BenchmarkScenario,
        details: list[str],
    ) -> int:
        """Score structural elements (40 points)."""
        score = 0
        structure = scenario.expected_elements.get("structure", {})
        
        # Check for docstring (10 points)
        if structure.get("has_docstring", False):
            if '"""' in code or "'''" in code:
                score += 10
                details.append("[✓] Has docstring (+10)")
            else:
                details.append("[✗] Missing docstring (+0)")
        else:
            score += 10  # Not required
        
        # Check for assertions (10 points)
        if structure.get("has_assertions", True):
            if "assert" in code or "expect(" in code:
                score += 10
                details.append("[✓] Has assertions (+10)")
            else:
                details.append("[✗] Missing assertions (+0)")
        
        # Check minimum assertions (10 points)
        min_assertions = structure.get("min_assertions", 1)
        assertion_count = code.count("assert ") + code.count("expect(")
        if assertion_count >= min_assertions:
            score += 10
            details.append(f"[✓] Has {assertion_count} assertions (min: {min_assertions}) (+10)")
        else:
            details.append(f"[✗] Only {assertion_count} assertions (min: {min_assertions}) (+0)")
        
        # Check proper structure (10 points)
        if scenario.framework == "pytest":
            if "def test_" in code:
                score += 10
                details.append("[✓] Has test function (+10)")
            else:
                details.append("[✗] Missing test function (+0)")
        elif scenario.framework == "robot":
            if "*** Test Cases ***" in code:
                score += 10
                details.append("[✓] Has Test Cases section (+10)")
            else:
                details.append("[✗] Missing Test Cases section (+0)")
        
        return score
    
    def _score_content(
        self,
        code: str,
        scenario: BenchmarkScenario,
        details: list[str],
    ) -> int:
        """Score content elements (40 points)."""
        score = 0
        expected = scenario.expected_elements
        
        # Check must_contain (30 points)
        must_contain = expected.get("must_contain", [])
        if must_contain:
            found = sum(1 for item in must_contain if item.lower() in code.lower())
            points = int((found / len(must_contain)) * 30)
            score += points
            details.append(f"[{'✓' if found == len(must_contain) else '~'}] Contains {found}/{len(must_contain)} required elements (+{points})")
        else:
            score += 30
        
        # Check must_not_contain (10 points)
        must_not_contain = expected.get("must_not_contain", [])
        if must_not_contain:
            violations = [item for item in must_not_contain if item.lower() in code.lower()]
            if not violations:
                score += 10
                details.append("[✓] No forbidden elements (+10)")
            else:
                details.append(f"[✗] Contains forbidden: {violations} (+0)")
        else:
            score += 10
        
        return score
    
    def _score_quality(
        self,
        code: str,
        scenario: BenchmarkScenario,
        details: list[str],
    ) -> int:
        """Score quality checks (20 points)."""
        score = 0
        checks = scenario.quality_checks
        
        if not checks:
            return 20  # Full points if no quality checks defined
        
        points_per_check = 20 // len(checks)
        
        for check in checks:
            name = check["name"]
            pattern = check["pattern"]
            should_match = check.get("should_match", True)
            
            matches = bool(re.search(pattern, code))
            passed = matches == should_match
            
            if passed:
                score += points_per_check
                details.append(f"[✓] {name} (+{points_per_check})")
            else:
                details.append(f"[✗] {name} (+0)")
        
        return score
```

## 11.3 Runner (`regression/runner.py`)

```python
"""
Runs prompt regression tests.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table

from aitestkit.utils.claude_client import ClaudeClient
from aitestkit.generator.context_builder import ContextBuilder
from aitestkit.regression.scorer import Scorer, ScoreBreakdown, BenchmarkScenario
from aitestkit.config import config


@dataclass
class ScenarioResult:
    """Result for a single scenario."""
    scenario: BenchmarkScenario
    old_score: ScoreBreakdown
    new_score: ScoreBreakdown
    passed: bool
    regression: bool


@dataclass
class RegressionResult:
    """Overall regression test result."""
    passed: bool
    scenarios: list[ScenarioResult]
    total_scenarios: int
    passed_count: int
    failed_count: int
    regression_count: int


class RegressionRunner:
    """
    Runs prompt regression tests.
    
    Compares old and new prompts against benchmark scenarios.
    Uses Claude Haiku 4.5 for fast, cost-effective testing.
    """
    
    def __init__(self, client: Optional[ClaudeClient] = None):
        self.client = client or ClaudeClient()
        self.scorer = Scorer()
        self.context_builder = ContextBuilder()
        self.console = Console()
    
    def run_all(self, baseline_ref: str = "main") -> RegressionResult:
        """
        Run regression on all benchmark scenarios.
        
        Args:
            baseline_ref: Git ref for baseline prompts
        
        Returns:
            RegressionResult with all scenario results
        """
        benchmarks_dir = config.prompts_dir / "benchmarks"
        scenarios = list(benchmarks_dir.glob("*.yaml"))
        
        results = []
        for scenario_path in scenarios:
            result = self._run_scenario(scenario_path, baseline_ref)
            results.append(result)
        
        passed_count = sum(1 for r in results if r.passed)
        failed_count = sum(1 for r in results if not r.passed)
        regression_count = sum(1 for r in results if r.regression)
        
        return RegressionResult(
            passed=all(r.passed for r in results),
            scenarios=results,
            total_scenarios=len(results),
            passed_count=passed_count,
            failed_count=failed_count,
            regression_count=regression_count,
        )
    
    def run_single(self, prompt_path: Path, baseline_ref: str = "main") -> RegressionResult:
        """Run regression for scenarios affected by a specific prompt."""
        # For now, run all scenarios
        # Could be optimized to only run relevant scenarios
        return self.run_all(baseline_ref)
    
    def _run_scenario(
        self,
        scenario_path: Path,
        baseline_ref: str,
    ) -> ScenarioResult:
        """Run a single benchmark scenario."""
        scenario = self.scorer.load_scenario(scenario_path)
        
        # Build prompts
        system_prompt = self.context_builder.build_system_prompt(scenario.framework)
        user_prompt = f"Framework: {scenario.framework}\n\nScenario:\n{scenario.input_scenario}"
        
        # Generate with current prompt (using Haiku for speed)
        new_response = self.client.quick_check(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
        new_code = self._extract_code(new_response)
        new_score = self.scorer.score(new_code, scenario)
        
        # For baseline, we'd normally load old prompt from git
        # For simplicity, we use current prompt as baseline too
        # In real implementation, use: git show {baseline_ref}:path/to/prompt
        old_score = new_score  # Simplified - would be different in real impl
        
        # Determine pass/fail
        passed = (
            new_score.total >= scenario.baseline_score and
            new_score.total >= old_score.total - config.regression_tolerance
        )
        regression = new_score.total < old_score.total - config.regression_tolerance
        
        return ScenarioResult(
            scenario=scenario,
            old_score=old_score,
            new_score=new_score,
            passed=passed,
            regression=regression,
        )
    
    def _extract_code(self, response: str) -> str:
        """Extract code from response."""
        import re
        pattern = r"```(?:\w+)?\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        if matches:
            return max(matches, key=len).strip()
        return response.strip()
    
    def display_results(self, results: RegressionResult, verbose: bool = False) -> None:
        """Display regression results in a table."""
        table = Table(title="Prompt Regression Results")
        
        table.add_column("Scenario", style="cyan")
        table.add_column("Old Score", justify="right")
        table.add_column("New Score", justify="right")
        table.add_column("Status", justify="center")
        
        for result in results.scenarios:
            status = "[green]✓ PASS[/green]" if result.passed else "[red]✗ FAIL[/red]"
            if result.regression:
                status = "[red]⚠ REGRESSION[/red]"
            
            table.add_row(
                result.scenario.name,
                str(result.old_score.total),
                str(result.new_score.total),
                status,
            )
        
        self.console.print(table)
        
        # Summary
        summary = f"\n[bold]Summary:[/bold] {results.passed_count}/{results.total_scenarios} passed"
        if results.regression_count > 0:
            summary += f", [red]{results.regression_count} regressions[/red]"
        
        overall = "[green]PASSED[/green]" if results.passed else "[red]FAILED[/red]"
        summary += f"\n[bold]Overall: {overall}[/bold]"
        
        self.console.print(summary)
        
        if verbose:
            for result in results.scenarios:
                self.console.print(f"\n[bold]{result.scenario.name}[/bold]")
                for detail in result.new_score.details:
                    self.console.print(f"  {detail}")
```

---

# 12. Sample Application

## 12.1 FastAPI Todo App (`sample_app/main.py`)

```python
"""
Sample Todo API for testing AITestKit.
A minimal FastAPI application with intentional issues for failure analysis demos.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(
    title="Todo API",
    description="Sample API for AITestKit demos",
    version="1.0.0",
)

# In-memory storage
todos: dict[int, dict] = {}
next_id = 1


class TodoCreate(BaseModel):
    """Schema for creating a todo."""
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoUpdate(BaseModel):
    """Schema for updating a todo."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    """Schema for todo response."""
    id: int
    title: str
    description: Optional[str]
    completed: bool


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Todo API", "version": "1.0.0"}


@app.get("/todos", response_model=list[Todo])
def list_todos():
    """List all todos."""
    return [Todo(id=id, **data) for id, data in todos.items()]


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    """Create a new todo."""
    global next_id
    
    todo_id = next_id
    next_id += 1
    
    todos[todo_id] = {
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
    }
    
    return Todo(id=todo_id, **todos[todo_id])


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    """Get a specific todo."""
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo {todo_id} not found",
        )
    return Todo(id=todo_id, **todos[todo_id])


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate):
    """Update a todo."""
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo {todo_id} not found",
        )
    
    if todo.title is not None:
        todos[todo_id]["title"] = todo.title
    if todo.description is not None:
        todos[todo_id]["description"] = todo.description
    if todo.completed is not None:
        todos[todo_id]["completed"] = todo.completed
    
    return Todo(id=todo_id, **todos[todo_id])


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    """Delete a todo."""
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo {todo_id} not found",
        )
    del todos[todo_id]


# Intentional bug for failure analysis demo
@app.get("/todos/search")
def search_todos(q: str):
    """
    Search todos by title.
    
    BUG: This endpoint has an intentional bug - it will fail
    if the query is empty, demonstrating failure analysis.
    """
    if not q:
        # Intentional bug: should return empty list, not error
        raise ValueError("Search query cannot be empty")
    
    results = [
        Todo(id=id, **data)
        for id, data in todos.items()
        if q.lower() in data["title"].lower()
    ]
    return results


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

# 13. Configuration

## 13.1 Environment Variables (`.env.example`)

```bash
# AITestKit Configuration

# Required: Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Optional: Override default paths
AITESTKIT_PROMPTS_DIR=./src/aitestkit/prompts
AITESTKIT_OUTPUT_DIR=./output

# Optional: Default framework
AITESTKIT_DEFAULT_FRAMEWORK=pytest

# Optional: Regression settings
AITESTKIT_REGRESSION_THRESHOLD=85
AITESTKIT_REGRESSION_TOLERANCE=5
```

## 13.2 Git Ignore (`.gitignore`)

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.eggs/
*.egg
.mypy_cache/
.pytest_cache/
.ruff_cache/

# Virtual environments
.venv/
venv/
ENV/

# Environment variables
.env
.env.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# Output
output/
*.log

# Test artifacts
htmlcov/
.coverage
coverage.xml

# OS
.DS_Store
Thumbs.db
```

---

# 14. GitHub Actions

## 14.1 Test Workflow (`.github/workflows/test.yml`)

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"
      
      - name: Lint with ruff
        run: ruff check src/ tests/
      
      - name: Type check with mypy
        run: mypy src/
      
      - name: Run tests
        run: pytest tests/ -v --cov=src/aitestkit --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: coverage.xml
```

## 14.2 Prompt Regression (`.github/workflows/prompt-regression.yml`)

```yaml
name: Prompt Regression

on:
  pull_request:
    paths:
      - 'src/aitestkit/prompts/**'

jobs:
  regression:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for baseline comparison
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .
      
      - name: Run prompt regression
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          aitestkit regression --all --baseline origin/main
      
      - name: Comment on PR
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            // Read results and post comment
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '## Prompt Regression Results\n\nSee workflow run for details.'
            });
```

---

# 15. File Specifications

## 15.1 README.md Structure

```markdown
# AITestKit

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Claude API](https://img.shields.io/badge/Claude-API-orange.svg)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/github/actions/workflow/status/USER/aitestkit/test.yml)](https://github.com/USER/aitestkit/actions)

> AI-Powered Test Development Toolkit - Generate tests, analyze failures, validate prompts

[Screenshot or GIF here]

## ✨ Features

- **Test Generator** - Convert natural language to test code
- **Failure Analyzer** - AI-powered root cause analysis  
- **Prompt Regression** - Validate prompt quality changes

## 🚀 Quick Start

### Installation

```bash
pip install aitestkit
```

### Generate a Test

```bash
export ANTHROPIC_API_KEY=your-key
aitestkit generate "Test user can create a todo item" -f pytest
```

### Analyze a Failure

```bash
aitestkit analyze ./failed_test.log
```

## 📖 Documentation

- [Getting Started](docs/getting-started.md)
- [Architecture](docs/architecture.md)
- [Prompt Engineering Guide](docs/prompt-engineering.md)

## 🏗️ Architecture

[Architecture diagram]

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE)
```

---

# 16. Implementation Order

## Priority Order

```
PHASE 1: Foundation (Days 1-3)
==============================
1. pyproject.toml
2. src/aitestkit/__init__.py
3. src/aitestkit/config.py
4. src/aitestkit/utils/claude_client.py
5. src/aitestkit/cli.py (basic structure)
6. .env.example
7. .gitignore

PHASE 2: Test Generator (Days 4-7)
==================================
8. prompts/templates/code_generation/system.md
9. prompts/templates/code_generation/pytest.md
10. prompts/templates/code_generation/robot_framework.md
11. src/aitestkit/generator/context_builder.py
12. src/aitestkit/generator/output_parser.py
13. src/aitestkit/generator/generator.py
14. Update cli.py with generate command

PHASE 3: Failure Analyzer (Days 8-10)
=====================================
15. prompts/templates/failure_analysis/system.md
16. src/aitestkit/analyzer/log_parser.py
17. src/aitestkit/analyzer/report_generator.py
18. src/aitestkit/analyzer/analyzer.py
19. Update cli.py with analyze command

PHASE 4: Prompt Regression (Days 11-13)
=======================================
20. prompts/benchmarks/scenario_01_crud.yaml
21. prompts/benchmarks/scenario_02_auth.yaml (etc.)
22. src/aitestkit/regression/scorer.py
23. src/aitestkit/regression/comparator.py
24. src/aitestkit/regression/runner.py
25. Update cli.py with regression command

PHASE 5: Sample App & Polish (Days 14-20)
=========================================
26. sample_app/main.py
27. tests/ (all test files)
28. .github/workflows/test.yml
29. .github/workflows/prompt-regression.yml
30. README.md (full version)
31. docs/ (all documentation)
```

---

# 17. Testing Strategy

## 17.1 Test Categories

| Category | Purpose | Location |
|----------|---------|----------|
| Unit tests | Test individual functions | tests/test_*.py |
| Integration tests | Test component interaction | tests/integration/ |
| Mock tests | Test without API calls | tests/ (with mocks) |

## 17.2 Mocking Claude API

```python
# tests/conftest.py

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_claude_response():
    """Mock Claude API response."""
    return """```python
def test_example():
    assert True
```

# Suggested filename: test_example.py
"""


@pytest.fixture
def mock_client(mock_claude_response):
    """Mock ClaudeClient."""
    with patch("aitestkit.utils.claude_client.Anthropic") as mock:
        client = MagicMock()
        client.messages.create.return_value = MagicMock(
            content=[MagicMock(text=mock_claude_response)],
            usage=MagicMock(input_tokens=100, output_tokens=200),
        )
        mock.return_value = client
        yield mock
```

---

# 18. Documentation Requirements

## 18.1 Required Documentation

| Document | Purpose | Priority |
|----------|---------|----------|
| README.md | Project overview | High |
| docs/getting-started.md | Setup guide | High |
| docs/architecture.md | System design | Medium |
| docs/prompt-engineering.md | Prompt guide | Medium |
| CONTRIBUTING.md | Contribution guide | Low |
| CHANGELOG.md | Version history | Low |

## 18.2 Code Documentation

- All public functions must have docstrings
- Complex logic should have inline comments
- Type hints required for all function signatures

---

# Summary

## Key Commands

```bash
# Install
pip install -e ".[dev]"

# Generate test
aitestkit generate "scenario" -f pytest

# Analyze failure
aitestkit analyze ./log.txt

# Run regression
aitestkit regression --all

# Run tests
pytest tests/ -v
```

## Key Files

| File | Description |
|------|-------------|
| `cli.py` | Entry point |
| `claude_client.py` | API wrapper |
| `generator.py` | Test generation |
| `analyzer.py` | Failure analysis |
| `runner.py` | Prompt regression |
| `system.md` | Main prompts |

## Models Used

| Task | Model | Cost |
|------|-------|------|
| Code generation | Opus 4.5 | $5/$25 |
| Failure analysis | Sonnet 4.5 | $3/$15 |
| Regression tests | Haiku 4.5 | $1/$5 |

---

**This document provides everything needed to implement AITestKit with Claude Code.**

*Last updated: January 8, 2025*
