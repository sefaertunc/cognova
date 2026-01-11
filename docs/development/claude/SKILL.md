# AITestKit Development Skill
## Claude Code Implementation Guide
### Version 1.0 | January 2025

---

# PROJECT IDENTITY

**Name:** AITestKit
**Type:** CLI Tool / Python Package
**Purpose:** AI-powered test development toolkit using Claude API
**Repository:** aitestkit
**License:** MIT

---

# RELATED DOCUMENTATION

This SKILL.md provides detailed implementation guidance for developers. For complete project context, see:

- **[docs/MASTER_SPEC.md](../../MASTER_SPEC.md)** - Complete project specification (vision, architecture, features, schemas)
- **[docs/BACKLOG.md](../../BACKLOG.md)** - Feature backlog with implementation status tracking
- **[CLAUDE.md](../../../CLAUDE.md)** - Claude Code instructions and quick reference

---

# QUICK REFERENCE

## Commands to Implement
```bash
aitestkit generate "scenario" -f pytest|robot|playwright  # Test generation
aitestkit analyze ./log.txt -f markdown|json|console      # Failure analysis
aitestkit regression --all                                 # Prompt validation
aitestkit info                                             # Show configuration
```

## Claude Models
| Task | Model ID | Cost (per 1M tokens) |
|------|----------|----------------------|
| Code Generation | `claude-opus-4-5-20250514` | $5 input / $25 output |
| Failure Analysis | `claude-sonnet-4-5-20250514` | $3 input / $15 output |
| Prompt Regression | `claude-haiku-4-5-20250514` | $1 input / $5 output |

## Key Paths
```
src/aitestkit/
├── cli.py                    # Entry point
├── config.py                 # Configuration
├── utils/claude_client.py    # API wrapper (IMPLEMENT FIRST)
├── generator/                # Test generation module
├── analyzer/                 # Failure analysis module
├── regression/               # Prompt regression module
└── prompts/                  # Prompt templates and benchmarks
```

---

# ARCHITECTURE OVERVIEW

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER INPUT                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  CLI Command: aitestkit [generate|analyze|regression] [args]            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                               CLI LAYER                                  │
│                              (cli.py)                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  • Parse arguments with Click                                           │
│  • Route to appropriate module                                          │
│  • Handle output formatting with Rich                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│     GENERATOR       │ │      ANALYZER       │ │     REGRESSION      │
│                     │ │                     │ │                     │
│ • context_builder   │ │ • log_parser        │ │ • scorer            │
│ • output_parser     │ │ • analyzer          │ │ • runner            │
│ • generator         │ │ • report_generator  │ │ • comparator        │
│                     │ │                     │ │                     │
│ Model: OPUS 4.5     │ │ Model: SONNET 4.5   │ │ Model: HAIKU 4.5    │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLAUDE CLIENT                                  │
│                      (utils/claude_client.py)                           │
├─────────────────────────────────────────────────────────────────────────┤
│  • Model selection (opus/sonnet/haiku)                                  │
│  • API call management                                                  │
│  • Usage tracking and cost estimation                                   │
│  • Error handling and retries                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          ANTHROPIC API                                   │
│                        (External Service)                               │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow: Test Generation

```
User: "Test user can create todo"
            │
            ▼
┌─────────────────────────────────────┐
│ 1. CONTEXT BUILDER                  │
│    • Load system.md prompt          │
│    • Load framework prompt (pytest) │
│    • Load shared context            │
│    • Merge into system_prompt       │
│    • Build user_prompt with scenario│
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│ 2. CLAUDE CLIENT (Opus 4.5)         │
│    • Send system_prompt + user_prompt│
│    • Receive generated code         │
│    • Track token usage              │
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│ 3. OUTPUT PARSER                    │
│    • Extract code from response     │
│    • Extract suggested filename     │
│    • Validate structure             │
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│ 4. FILE WRITER                      │
│    • Save to output directory       │
│    • Display success message        │
└─────────────────────────────────────┘
```

---

# IMPLEMENTATION SPECIFICATIONS

## 1. Claude Client (`utils/claude_client.py`)

### Purpose
Central API wrapper handling all Claude interactions with model selection, usage tracking, and error handling.

### Class Structure

```python
"""
Claude API client wrapper for AITestKit.

Responsibilities:
- Manage API authentication
- Select appropriate model for task type
- Track usage and costs
- Handle errors and retries
"""

from typing import Literal, Optional
from dataclasses import dataclass
from anthropic import Anthropic, APIError, RateLimitError, AuthenticationError
import os

ModelType = Literal["opus", "sonnet", "haiku"]


@dataclass
class UsageStats:
    """Track API usage for cost estimation."""
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


class ClaudeClient:
    """
    Claude API wrapper with model selection and usage tracking.
    
    Models:
        opus: Best quality, use for code generation ($5/$25 per 1M)
        sonnet: Balanced, use for analysis ($3/$15 per 1M)
        haiku: Fast/cheap, use for regression ($1/$5 per 1M)
    
    Example:
        client = ClaudeClient()
        code = client.generate_code(system_prompt, user_prompt)
    """
    
    MODELS = {
        "opus": "claude-opus-4-5-20250514",
        "sonnet": "claude-sonnet-4-5-20250514",
        "haiku": "claude-haiku-4-5-20250514",
    }
    
    PRICING = {
        "opus": {"input": 5.00, "output": 25.00},
        "sonnet": {"input": 3.00, "output": 15.00},
        "haiku": {"input": 1.00, "output": 5.00},
    }
```

### Required Methods

| Method | Model | Purpose | Temperature |
|--------|-------|---------|-------------|
| `generate(system, user, model)` | Any | Base method | 0.3 |
| `generate_code(system, user)` | Opus | Test generation | 0.2 |
| `analyze(system, user)` | Sonnet | Failure analysis | 0.4 |
| `quick_check(system, user)` | Haiku | Regression tests | 0.2 |
| `get_total_cost()` | - | Return session cost | - |
| `get_usage_summary()` | - | Return usage by model | - |

### Error Handling Pattern

```python
def generate(self, system_prompt: str, user_prompt: str, model: ModelType = "sonnet") -> str:
    try:
        response = self.client.messages.create(
            model=self.MODELS[model],
            max_tokens=4096,
            temperature=0.3,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        self._track_usage(model, response.usage)
        return response.content[0].text
    
    except AuthenticationError:
        raise ValueError("Invalid API key. Set ANTHROPIC_API_KEY environment variable.")
    except RateLimitError:
        # Implement exponential backoff retry
        raise
    except APIError as e:
        raise RuntimeError(f"Claude API error: {e}")
```

---

## 2. Configuration (`config.py`)

### Purpose
Centralized configuration management using environment variables and Pydantic validation.

### Structure

```python
"""
Configuration management for AITestKit.

Loads from:
1. Environment variables
2. .env file (via python-dotenv)
3. Default values
"""

from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Config(BaseModel):
    """Application configuration."""
    
    # API
    anthropic_api_key: str | None = None
    
    # Paths
    prompts_dir: Path = Path("src/aitestkit/prompts")
    output_dir: Path = Path("./output")
    
    # Defaults
    default_framework: str = "pytest"
    
    # Regression
    regression_threshold: int = 85   # Minimum passing score
    regression_tolerance: int = 5    # Max allowed score drop
    
    @classmethod
    def load(cls) -> "Config":
        """Load configuration from environment."""
        return cls(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            prompts_dir=Path(os.getenv("AITESTKIT_PROMPTS_DIR", "src/aitestkit/prompts")),
            output_dir=Path(os.getenv("AITESTKIT_OUTPUT_DIR", "./output")),
            default_framework=os.getenv("AITESTKIT_DEFAULT_FRAMEWORK", "pytest"),
        )
    
    def validate_api_key(self) -> bool:
        """Check if API key is configured."""
        return bool(self.anthropic_api_key)


# Global singleton
config = Config.load()
```

---

## 3. CLI (`cli.py`)

### Purpose
Entry point using Click framework with Rich for beautiful output.

### Command Structure

```python
"""
AITestKit Command Line Interface.

Usage:
    aitestkit generate "Test user login" -f pytest
    aitestkit analyze ./failed.log -f markdown
    aitestkit regression --all
"""

import click
from rich.console import Console
from rich.panel import Panel

from aitestkit import __version__
from aitestkit.config import config

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="aitestkit")
def main():
    """AITestKit - AI-Powered Test Development Toolkit"""
    pass


@main.command()
@click.argument("scenario", type=str)
@click.option("--framework", "-f", type=click.Choice(["robot", "pytest", "playwright"]), default="pytest")
@click.option("--output", "-o", type=click.Path(), default="./output")
@click.option("--context", "-c", type=click.Path(exists=True), default=None)
def generate(scenario: str, framework: str, output: str, context: str | None):
    """Generate test code from natural language scenario."""
    # Implementation
    pass


@main.command()
@click.argument("log_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), default=None)
@click.option("--format", "-f", type=click.Choice(["markdown", "json", "console"]), default="console")
def analyze(log_file: str, output: str | None, format: str):
    """Analyze test failure and suggest fixes."""
    # Implementation
    pass


@main.command()
@click.option("--prompt", "-p", type=click.Path(exists=True), default=None)
@click.option("--all", "-a", is_flag=True, default=False)
@click.option("--baseline", "-b", type=str, default="main")
@click.option("--verbose", "-v", is_flag=True, default=False)
def regression(prompt: str | None, all: bool, baseline: str, verbose: bool):
    """Run prompt regression tests."""
    # Implementation
    pass


@main.command()
def info():
    """Show configuration and status."""
    console.print(Panel("[bold]AITestKit Configuration[/bold]"))
    console.print(f"Version: {__version__}")
    console.print(f"API Key: {'✓ Configured' if config.validate_api_key() else '✗ Missing'}")
    console.print(f"Prompts: {config.prompts_dir}")
    console.print(f"Output: {config.output_dir}")


if __name__ == "__main__":
    main()
```

---

## 4. Generator Module

### 4.1 Context Builder (`generator/context_builder.py`)

```python
"""
Builds prompts by loading and merging template files with context.

Prompt Assembly Order:
1. Base system prompt (system.md)
2. Framework-specific prompt (pytest.md, robot_framework.md, playwright.md)
3. Shared context (testing_principles.md, coding_standards.md)
4. Few-shot examples (if available)
"""

from pathlib import Path
from aitestkit.config import config


class ContextBuilder:
    """Assembles system and user prompts from template files."""
    
    def __init__(self, prompts_dir: Path | None = None):
        self.prompts_dir = prompts_dir or config.prompts_dir
    
    def build_system_prompt(self, framework: str) -> str:
        """
        Build complete system prompt for code generation.
        
        Args:
            framework: Target framework (pytest, robot, playwright)
        
        Returns:
            Merged system prompt string
        """
        parts = []
        
        # 1. Base system prompt
        system_path = self.prompts_dir / "templates" / "code-generation" / "system.md"
        if system_path.exists():
            parts.append(system_path.read_text())
        
        # 2. Framework-specific prompt
        framework_map = {
            "pytest": "pytest.md",
            "robot": "robot_framework.md",
            "playwright": "playwright.md",
        }
        framework_path = self.prompts_dir / "templates" / "code-generation" / framework_map.get(framework, "pytest.md")
        if framework_path.exists():
            parts.append(f"\n\n# Framework: {framework.upper()}\n\n{framework_path.read_text()}")
        
        # 3. Shared context
        shared_dir = self.prompts_dir / "context" / "shared"
        if shared_dir.exists():
            for context_file in sorted(shared_dir.glob("*.md")):
                parts.append(f"\n\n# {context_file.stem.replace('_', ' ').title()}\n\n{context_file.read_text()}")
        
        return "\n".join(parts)
    
    def build_user_prompt(self, scenario: str, framework: str, context_file: Path | None = None) -> str:
        """
        Build user prompt with scenario and optional context.
        
        Args:
            scenario: Natural language test description
            framework: Target framework
            context_file: Optional additional context (API docs, etc.)
        
        Returns:
            Formatted user prompt
        """
        parts = [
            f"**Framework:** {framework}",
            f"\n**Scenario:**\n{scenario}",
        ]
        
        if context_file and context_file.exists():
            parts.append(f"\n**Additional Context:**\n{context_file.read_text()}")
        
        # Add examples if available
        examples = self._load_examples(framework)
        if examples:
            parts.append(f"\n**Reference Examples:**\n{examples}")
        
        return "\n".join(parts)
    
    def _load_examples(self, framework: str) -> str:
        """Load few-shot examples for the framework."""
        examples_dir = self.prompts_dir / "examples"
        if not examples_dir.exists():
            return ""
        
        ext_map = {"pytest": ".py", "robot": ".robot", "playwright": ".spec.ts"}
        ext = ext_map.get(framework, ".py")
        
        examples = []
        for example_file in sorted(examples_dir.glob(f"*{ext}"))[:2]:  # Max 2 examples
            examples.append(f"```\n{example_file.read_text()}\n```")
        
        return "\n\n".join(examples)
```

### 4.2 Output Parser (`generator/output_parser.py`)

```python
"""
Parses Claude API responses to extract code and metadata.

Handles:
- Code block extraction (```python ... ```)
- Filename extraction from comments
- Basic validation of generated code
"""

import re


class OutputParser:
    """Extracts and validates generated code from API responses."""
    
    EXTENSION_MAP = {
        "pytest": ".py",
        "robot": ".robot",
        "playwright": ".spec.ts",
    }
    
    def extract_code(self, response: str, framework: str) -> str:
        """
        Extract code from API response.
        
        Handles:
        - Fenced code blocks (```python ... ```)
        - Raw code without fencing
        - Multiple code blocks (returns largest)
        
        Args:
            response: Raw API response
            framework: Target framework for validation
        
        Returns:
            Extracted code string
        """
        # Try to extract from code blocks
        pattern = r"```(?:\w+)?\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        
        if matches:
            # Return the largest code block (likely the main code)
            return max(matches, key=len).strip()
        
        # No code blocks - clean up the response
        code = response
        
        # Remove common explanation prefixes
        code = re.sub(r"^Here(?:'s| is).*?:\n+", "", code, flags=re.IGNORECASE | re.MULTILINE)
        code = re.sub(r"^This (?:test|code).*?:\n+", "", code, flags=re.IGNORECASE | re.MULTILINE)
        
        return code.strip()
    
    def extract_filename(self, response: str, framework: str) -> str:
        """
        Extract suggested filename from response.
        
        Looks for patterns:
        - # Suggested filename: test_example.py
        - # Filename: test_example.py
        - File: test_example.py
        
        Falls back to default if not found.
        """
        patterns = [
            r"#\s*(?:Suggested\s+)?[Ff]ile(?:name)?:\s*(\S+)",
            r"[Ff]ile(?:name)?:\s*(\S+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response)
            if match:
                return match.group(1)
        
        # Generate default filename
        ext = self.EXTENSION_MAP.get(framework, ".py")
        return f"generated_test{ext}"
    
    def validate_code(self, code: str, framework: str) -> list[str]:
        """
        Validate generated code structure.
        
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        
        if framework == "pytest":
            if "def test_" not in code:
                issues.append("Missing test function (def test_*)")
            if "assert" not in code:
                issues.append("Missing assertions")
            if "import pytest" not in code and "@pytest" in code:
                issues.append("Using pytest decorators without import")
        
        elif framework == "robot":
            if "*** Test Cases ***" not in code:
                issues.append("Missing *** Test Cases *** section")
            if "*** Settings ***" not in code:
                issues.append("Missing *** Settings *** section")
        
        elif framework == "playwright":
            if "test(" not in code and "test.describe(" not in code:
                issues.append("Missing test() function")
            if "expect(" not in code:
                issues.append("Missing expect() assertions")
        
        return issues
```

### 4.3 Generator (`generator/generator.py`)

```python
"""
Main test code generator orchestrating context building and API calls.
"""

from dataclasses import dataclass
from pathlib import Path

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
    validation_issues: list[str]
    raw_response: str


class TestGenerator:
    """
    Generates test code from natural language scenarios.
    
    Uses Claude Opus 4.5 for highest code quality.
    
    Example:
        generator = TestGenerator()
        result = generator.generate(
            scenario="Test user can create a new todo",
            framework="pytest"
        )
        print(result.code)
    """
    
    def __init__(self, client: ClaudeClient | None = None):
        self.client = client or ClaudeClient()
        self.context_builder = ContextBuilder()
        self.output_parser = OutputParser()
    
    def generate(
        self,
        scenario: str,
        framework: str = "pytest",
        context_file: Path | None = None,
    ) -> GenerationResult:
        """
        Generate test code for a given scenario.
        
        Args:
            scenario: Natural language test description
            framework: Target framework (pytest, robot, playwright)
            context_file: Optional additional context file
        
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
        
        # Generate using Opus for best quality
        raw_response = self.client.generate_code(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
        
        # Parse output
        code = self.output_parser.extract_code(raw_response, framework)
        filename = self.output_parser.extract_filename(raw_response, framework)
        validation_issues = self.output_parser.validate_code(code, framework)
        
        # Get usage stats
        usage = self.client.usage_history[-1] if self.client.usage_history else None
        
        return GenerationResult(
            code=code,
            framework=framework,
            suggested_filename=filename,
            tokens_used=(usage.input_tokens + usage.output_tokens) if usage else 0,
            cost=usage.cost_usd if usage else 0.0,
            validation_issues=validation_issues,
            raw_response=raw_response,
        )
```

---

## 5. Analyzer Module

### 5.1 Log Parser (`analyzer/log_parser.py`)

```python
"""
Parses test log files to extract error information.

Supports:
- Python tracebacks
- Pytest output
- Robot Framework logs
- Generic error patterns
"""

import re
from dataclasses import dataclass


@dataclass
class ParsedLog:
    """Extracted log information."""
    test_name: str | None
    error_type: str | None
    error_message: str | None
    stack_trace: str | None
    timestamp: str | None
    framework: str | None


class LogParser:
    """Extracts structured information from test logs."""
    
    ERROR_PATTERNS = [
        (r"(\w+Error):\s*(.+)", "error_type", "error_message"),
        (r"(\w+Exception):\s*(.+)", "error_type", "error_message"),
        (r"FAILED\s+(.+?)\s*-", "test_name", None),
        (r"AssertionError:\s*(.+)", None, "error_message"),
    ]
    
    def parse(self, log_content: str) -> ParsedLog:
        """
        Parse log content into structured data.
        
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
            framework=self._detect_framework(log_content),
        )
    
    def _extract_test_name(self, content: str) -> str | None:
        patterns = [
            r"FAILED\s+(test_\w+)",
            r"(\w+::\w+::test_\w+)",
            r"Test Case:\s*(.+)",
        ]
        for pattern in patterns:
            if match := re.search(pattern, content):
                return match.group(1)
        return None
    
    def _extract_error_type(self, content: str) -> str | None:
        if match := re.search(r"(\w+(?:Error|Exception)):", content):
            return match.group(1)
        return None
    
    def _extract_error_message(self, content: str) -> str | None:
        if match := re.search(r"(?:Error|Exception):\s*(.+?)(?:\n|$)", content):
            return match.group(1).strip()
        return None
    
    def _extract_stack_trace(self, content: str) -> str | None:
        if match := re.search(r"(Traceback \(most recent call last\):.*?)(?:\n\n|\Z)", content, re.DOTALL):
            return match.group(1).strip()
        return None
    
    def _extract_timestamp(self, content: str) -> str | None:
        if match := re.search(r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})", content):
            return match.group(1)
        return None
    
    def _detect_framework(self, content: str) -> str | None:
        if "*** Test Cases ***" in content or "Robot Framework" in content:
            return "robot"
        if "pytest" in content.lower() or "def test_" in content:
            return "pytest"
        if "playwright" in content.lower():
            return "playwright"
        return None
```

### 5.2 Analyzer (`analyzer/analyzer.py`)

```python
"""
Failure analysis using Claude Sonnet for balanced quality and cost.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from rich.panel import Panel

from aitestkit.utils.claude_client import ClaudeClient
from aitestkit.analyzer.log_parser import LogParser, ParsedLog
from aitestkit.config import config


class FailureCategory(str, Enum):
    CODE_BUG = "Code Bug"
    ENVIRONMENT = "Environment Issue"
    TEST_FLAKY = "Test Flaky"
    DATA_ISSUE = "Data Issue"
    CONFIGURATION = "Configuration"
    UNKNOWN = "Unknown"


class Confidence(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass
class AnalysisResult:
    """Structured analysis result."""
    test_name: str
    error_summary: str
    root_cause: str
    confidence: Confidence
    confidence_percent: int
    category: FailureCategory
    evidence: list[str]
    suggested_actions: list[str]
    investigation_steps: list[str]
    
    def to_markdown(self) -> str:
        """Format as Markdown report."""
        return f"""# Failure Analysis Report

**Test:** {self.test_name}
**Category:** {self.category.value}
**Confidence:** {self.confidence.value} ({self.confidence_percent}%)

## Summary
{self.error_summary}

## Root Cause
{self.root_cause}

## Evidence
{chr(10).join(f'- {e}' for e in self.evidence)}

## Suggested Actions
{chr(10).join(f'{i+1}. {a}' for i, a in enumerate(self.suggested_actions))}

## Investigation Steps
{chr(10).join(f'{i+1}. {s}' for i, s in enumerate(self.investigation_steps))}
"""
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
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
        """Format as Rich panel for console output."""
        content = f"""[bold]Test:[/bold] {self.test_name}
[bold]Category:[/bold] {self.category.value}

[bold red]Root Cause:[/bold red]
{self.root_cause}

[bold]Confidence:[/bold] {self.confidence.value} ({self.confidence_percent}%)

[bold]Evidence:[/bold]
""" + "\n".join(f"  • {e}" for e in self.evidence) + """

[bold green]Suggested Actions:[/bold green]
""" + "\n".join(f"  {i+1}. {a}" for i, a in enumerate(self.suggested_actions))
        
        return Panel(content, title="[bold]Failure Analysis[/bold]", border_style="red")


class FailureAnalyzer:
    """
    Analyzes test failures using Claude Sonnet 4.5.
    
    Example:
        analyzer = FailureAnalyzer()
        result = analyzer.analyze(log_content)
        print(result.to_markdown())
    """
    
    def __init__(self, client: ClaudeClient | None = None):
        self.client = client or ClaudeClient()
        self.log_parser = LogParser()
    
    def analyze(self, log_content: str, test_name: str | None = None) -> AnalysisResult:
        """
        Analyze a test failure.
        
        Args:
            log_content: Raw log/error content
            test_name: Optional test name (extracted from log if not provided)
        
        Returns:
            AnalysisResult with root cause and suggestions
        """
        # Parse log
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
        
        # Parse response into structured result
        return self._parse_response(response, test_name)
    
    def _load_system_prompt(self) -> str:
        prompt_path = config.prompts_dir / "templates" / "failure_analysis" / "system.md"
        if prompt_path.exists():
            return prompt_path.read_text()
        return self._default_system_prompt()
    
    def _default_system_prompt(self) -> str:
        return """You are an expert QA engineer analyzing test failures.
Provide structured analysis with root cause, confidence level, and actionable suggestions."""
    
    def _build_user_prompt(self, log_content: str, parsed: ParsedLog) -> str:
        return f"""Analyze this test failure:

**Error Type:** {parsed.error_type or 'Unknown'}
**Error Message:** {parsed.error_message or 'See log'}
**Framework:** {parsed.framework or 'Unknown'}

**Full Log:**
```
{log_content}
```

Provide analysis with:
1. Root cause (be specific)
2. Confidence level (High/Medium/Low with percentage)
3. Category (Code Bug, Environment Issue, Test Flaky, Data Issue, Configuration)
4. Evidence supporting your conclusion
5. Suggested actions to fix
6. Investigation steps if needed"""
    
    def _parse_response(self, response: str, test_name: str) -> AnalysisResult:
        """Parse Claude's response into structured AnalysisResult."""
        import re
        
        # Extract root cause
        root_cause = "Unknown"
        if match := re.search(r"[Rr]oot [Cc]ause[:\s]+(.+?)(?:\n\n|\n[#*])", response, re.DOTALL):
            root_cause = match.group(1).strip()
        
        # Extract confidence
        confidence = Confidence.MEDIUM
        confidence_percent = 50
        if match := re.search(r"[Cc]onfidence[:\s]+(\w+)\s*\(?(\d+)?%?\)?", response):
            conf_str = match.group(1).upper()
            if conf_str in [c.name for c in Confidence]:
                confidence = Confidence[conf_str]
            if match.group(2):
                confidence_percent = int(match.group(2))
        
        # Extract category
        category = FailureCategory.UNKNOWN
        for cat in FailureCategory:
            if cat.value.lower() in response.lower():
                category = cat
                break
        
        # Extract summary (first meaningful sentence)
        lines = [l.strip() for l in response.split('\n') if l.strip() and not l.startswith('#')]
        error_summary = lines[0] if lines else "Analysis complete"
        
        # Extract lists (evidence, actions, investigation)
        evidence = self._extract_list(response, r"[Ee]vidence[:\s]*\n((?:[-•*]\s*.+\n?)+)")
        actions = self._extract_list(response, r"[Ss]uggested [Aa]ctions?[:\s]*\n((?:[-•*\d.]\s*.+\n?)+)")
        investigation = self._extract_list(response, r"[Ii]nvestigation[:\s]*\n((?:[-•*\d.]\s*.+\n?)+)")
        
        return AnalysisResult(
            test_name=test_name,
            error_summary=error_summary[:200],  # Truncate summary
            root_cause=root_cause,
            confidence=confidence,
            confidence_percent=confidence_percent,
            category=category,
            evidence=evidence or ["See full analysis"],
            suggested_actions=actions or ["Review the error details"],
            investigation_steps=investigation or ["Check logs for more context"],
        )
    
    def _extract_list(self, text: str, pattern: str) -> list[str]:
        """Extract bullet/numbered list items from text."""
        if match := re.search(pattern, text):
            items = re.findall(r"[-•*\d.]+\s*(.+)", match.group(1))
            return [item.strip() for item in items if item.strip()]
        return []
```

---

## 6. Regression Module

### 6.1 Benchmark Scenario Format

```yaml
# prompts/benchmarks/scenario_01_crud.yaml

scenario_id: "crud_001"
name: "CRUD - Create Todo Item"
description: "Test creating a new todo via POST endpoint"
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
  
  must_not_contain:
    - "time.sleep"
    - "TODO"
    - "pass  #"
  
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

baseline_score: 85
```

### 6.2 Scorer (`regression/scorer.py`)

```python
"""
Scores generated code against benchmark criteria.

Scoring:
- Structural: 40 points (sections, functions, setup/teardown)
- Content: 40 points (required elements, no forbidden elements)
- Quality: 20 points (style, patterns, best practices)
"""

import re
from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class ScoreBreakdown:
    structural: int      # /40
    content: int         # /40
    quality: int         # /20
    total: int           # /100
    details: list[str]   # Individual check results


@dataclass
class BenchmarkScenario:
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
        """Load benchmark scenario from YAML file."""
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
        """Score generated code against scenario criteria."""
        details = []
        
        structural = self._score_structural(code, scenario, details)
        content = self._score_content(code, scenario, details)
        quality = self._score_quality(code, scenario, details)
        
        return ScoreBreakdown(
            structural=structural,
            content=content,
            quality=quality,
            total=structural + content + quality,
            details=details,
        )
    
    def _score_structural(self, code: str, scenario: BenchmarkScenario, details: list) -> int:
        """Score structural elements (40 points)."""
        score = 0
        structure = scenario.expected_elements.get("structure", {})
        
        # Docstring check (10 points)
        if structure.get("has_docstring", False):
            if '"""' in code or "'''" in code:
                score += 10
                details.append("[✓] Has docstring (+10)")
            else:
                details.append("[✗] Missing docstring (+0)")
        else:
            score += 10
        
        # Assertions check (15 points)
        if structure.get("has_assertions", True):
            assertion_count = code.count("assert ") + code.count("expect(")
            min_assertions = structure.get("min_assertions", 1)
            if assertion_count >= min_assertions:
                score += 15
                details.append(f"[✓] Has {assertion_count} assertions (+15)")
            else:
                details.append(f"[✗] Only {assertion_count} assertions, need {min_assertions} (+0)")
        
        # Test function check (15 points)
        if scenario.framework == "pytest" and "def test_" in code:
            score += 15
            details.append("[✓] Has test function (+15)")
        elif scenario.framework == "robot" and "*** Test Cases ***" in code:
            score += 15
            details.append("[✓] Has Test Cases section (+15)")
        elif scenario.framework == "playwright" and "test(" in code:
            score += 15
            details.append("[✓] Has test() function (+15)")
        else:
            details.append("[✗] Missing test structure (+0)")
        
        return score
    
    def _score_content(self, code: str, scenario: BenchmarkScenario, details: list) -> int:
        """Score content elements (40 points)."""
        score = 0
        expected = scenario.expected_elements
        
        # must_contain (30 points)
        must_contain = expected.get("must_contain", [])
        if must_contain:
            found = sum(1 for item in must_contain if item.lower() in code.lower())
            points = int((found / len(must_contain)) * 30)
            score += points
            details.append(f"[{'✓' if found == len(must_contain) else '~'}] Contains {found}/{len(must_contain)} required (+{points})")
        else:
            score += 30
        
        # must_not_contain (10 points)
        must_not_contain = expected.get("must_not_contain", [])
        if must_not_contain:
            violations = [item for item in must_not_contain if item.lower() in code.lower()]
            if not violations:
                score += 10
                details.append("[✓] No forbidden elements (+10)")
            else:
                details.append(f"[✗] Contains forbidden: {violations[:2]} (+0)")
        else:
            score += 10
        
        return score
    
    def _score_quality(self, code: str, scenario: BenchmarkScenario, details: list) -> int:
        """Score quality checks (20 points)."""
        checks = scenario.quality_checks
        if not checks:
            return 20
        
        score = 0
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

### 6.3 Runner (`regression/runner.py`)

```python
"""
Runs prompt regression tests against benchmark scenarios.
"""

from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.table import Table

from aitestkit.utils.claude_client import ClaudeClient
from aitestkit.generator.context_builder import ContextBuilder
from aitestkit.regression.scorer import Scorer, ScoreBreakdown, BenchmarkScenario
from aitestkit.config import config


@dataclass
class ScenarioResult:
    scenario: BenchmarkScenario
    old_score: ScoreBreakdown
    new_score: ScoreBreakdown
    passed: bool
    regression: bool


@dataclass
class RegressionResult:
    passed: bool
    scenarios: list[ScenarioResult]
    total_scenarios: int
    passed_count: int
    failed_count: int
    regression_count: int


class RegressionRunner:
    """
    Runs prompt regression tests using Haiku for cost efficiency.
    
    Example:
        runner = RegressionRunner()
        result = runner.run_all()
        runner.display_results(result)
    """
    
    def __init__(self, client: ClaudeClient | None = None):
        self.client = client or ClaudeClient()
        self.scorer = Scorer()
        self.context_builder = ContextBuilder()
        self.console = Console()
    
    def run_all(self, baseline_ref: str = "main") -> RegressionResult:
        """Run regression on all benchmark scenarios."""
        benchmarks_dir = config.prompts_dir / "benchmarks"
        
        if not benchmarks_dir.exists():
            return RegressionResult(
                passed=True,
                scenarios=[],
                total_scenarios=0,
                passed_count=0,
                failed_count=0,
                regression_count=0,
            )
        
        scenarios = list(benchmarks_dir.glob("*.yaml"))
        results = [self._run_scenario(path, baseline_ref) for path in scenarios]
        
        return RegressionResult(
            passed=all(r.passed for r in results),
            scenarios=results,
            total_scenarios=len(results),
            passed_count=sum(1 for r in results if r.passed),
            failed_count=sum(1 for r in results if not r.passed),
            regression_count=sum(1 for r in results if r.regression),
        )
    
    def _run_scenario(self, scenario_path: Path, baseline_ref: str) -> ScenarioResult:
        """Run a single benchmark scenario."""
        scenario = self.scorer.load_scenario(scenario_path)
        
        # Build prompts
        system_prompt = self.context_builder.build_system_prompt(scenario.framework)
        user_prompt = f"**Framework:** {scenario.framework}\n\n**Scenario:**\n{scenario.input_scenario}"
        
        # Generate with Haiku (fast and cheap)
        response = self.client.quick_check(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
        
        # Extract and score
        code = self._extract_code(response)
        new_score = self.scorer.score(code, scenario)
        
        # For now, use current as baseline (real implementation would load from git)
        old_score = new_score
        
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
        if matches := re.findall(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL):
            return max(matches, key=len).strip()
        return response.strip()
    
    def display_results(self, results: RegressionResult, verbose: bool = False) -> None:
        """Display results in formatted table."""
        table = Table(title="Prompt Regression Results")
        table.add_column("Scenario", style="cyan")
        table.add_column("Score", justify="right")
        table.add_column("Baseline", justify="right")
        table.add_column("Status", justify="center")
        
        for result in results.scenarios:
            status = "[green]✓ PASS[/green]" if result.passed else "[red]✗ FAIL[/red]"
            if result.regression:
                status = "[red]⚠ REGRESSION[/red]"
            
            table.add_row(
                result.scenario.name,
                str(result.new_score.total),
                str(result.scenario.baseline_score),
                status,
            )
        
        self.console.print(table)
        self.console.print(f"\n[bold]Summary:[/bold] {results.passed_count}/{results.total_scenarios} passed")
        
        if verbose:
            for result in results.scenarios:
                self.console.print(f"\n[bold]{result.scenario.name}[/bold]")
                for detail in result.new_score.details:
                    self.console.print(f"  {detail}")
```

---

# PROMPT TEMPLATES

## Code Generation System Prompt

Location: `src/aitestkit/prompts/templates/code-generation/system.md`

```markdown
# Role

You are an expert Senior QA Engineer specializing in test automation. You write clean, maintainable, and comprehensive test code.

# Task

Generate a complete, executable test file based on the user's scenario description.

# Constraints

## DO:
- Include comprehensive assertions with descriptive messages
- Add proper error handling where appropriate
- Use descriptive variable and function names
- Include documentation/docstrings
- Follow the specific framework's best practices
- Make tests independent and repeatable
- Use explicit waits instead of hardcoded sleeps

## DO NOT:
- Use `time.sleep()` or hardcoded waits
- Leave placeholder comments like "# TODO" or "# FIXME"
- Generate incomplete code
- Include external dependencies not specified
- Add unnecessary complexity

# Output Format

Return ONLY the test code. Do not include explanations before or after.
Start directly with the code.
At the end, add a comment with the suggested filename.

Example ending:
```
# Suggested filename: test_user_login.py
```
```

## Pytest Specific Prompt

Location: `src/aitestkit/prompts/templates/code-generation/pytest.md`

```markdown
# Pytest Guidelines

## Structure

```python
"""Module docstring describing the test suite."""

import pytest
from typing import Generator

# Fixtures first
@pytest.fixture
def setup_data() -> Generator[dict, None, None]:
    """Setup fixture with cleanup."""
    data = {"key": "value"}
    yield data
    # Cleanup here

# Tests follow
class TestFeatureName:
    """Test class docstring."""
    
    def test_should_do_x_when_y(self, setup_data: dict) -> None:
        """Test docstring explaining what and why."""
        # Arrange
        expected = "expected_value"
        
        # Act
        result = function_under_test(setup_data)
        
        # Assert
        assert result == expected, f"Expected {expected}, got {result}"
```

## Best Practices

- Use type hints on all functions
- Follow AAA pattern (Arrange, Act, Assert)
- Use fixtures for setup/teardown
- Descriptive test names: `test_should_X_when_Y`
- Include assertion messages
- Use `pytest.mark.parametrize` for multiple inputs
```

---

# CODE STANDARDS

## Python Style

```python
# Imports: stdlib, third-party, local (separated by blank lines)
import os
from pathlib import Path

from anthropic import Anthropic
from pydantic import BaseModel

from aitestkit.config import config


# Classes: PascalCase with docstrings
class MyClass:
    """Single-line docstring for simple classes."""
    
    def method(self, param: str) -> str:
        """
        Multi-line docstring for complex methods.
        
        Args:
            param: Description of parameter
        
        Returns:
            Description of return value
        
        Raises:
            ValueError: When param is empty
        """
        if not param:
            raise ValueError("param cannot be empty")
        return param.upper()


# Functions: snake_case with type hints
def process_data(items: list[str]) -> list[str]:
    """Process items and return results."""
    return [item.strip() for item in items if item]


# Constants: UPPER_CASE
DEFAULT_TIMEOUT = 30
API_VERSION = "v1"
```

## Error Handling Pattern

```python
from aitestkit.exceptions import AITestKitError, ConfigurationError, APIError


def safe_api_call():
    """Example of proper error handling."""
    try:
        result = client.generate(...)
        return result
    except AuthenticationError:
        raise ConfigurationError("Invalid API key. Check ANTHROPIC_API_KEY.")
    except RateLimitError as e:
        # Log and retry with backoff
        logger.warning(f"Rate limited: {e}")
        time.sleep(60)
        return safe_api_call()  # Retry
    except APIError as e:
        raise AITestKitError(f"API error: {e}")
```

## Logging Pattern

```python
import logging

logger = logging.getLogger(__name__)

def process():
    logger.debug("Starting process")
    logger.info("Processing item: %s", item_name)
    logger.warning("Unusual condition: %s", condition)
    logger.error("Failed to process: %s", error)
```

---

# TESTING GUIDELINES

## Test File Structure

```python
# tests/test_generator.py

"""Tests for the generator module."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from aitestkit.generator import TestGenerator, GenerationResult


class TestTestGenerator:
    """Tests for TestGenerator class."""
    
    @pytest.fixture
    def mock_client(self):
        """Mock Claude client."""
        client = MagicMock()
        client.generate_code.return_value = "def test_example():\n    assert True"
        client.usage_history = []
        return client
    
    @pytest.fixture
    def generator(self, mock_client):
        """Generator instance with mocked client."""
        return TestGenerator(client=mock_client)
    
    def test_generate_returns_result(self, generator):
        """Test that generate returns GenerationResult."""
        result = generator.generate("Test user login", framework="pytest")
        
        assert isinstance(result, GenerationResult)
        assert result.framework == "pytest"
        assert "def test_" in result.code
    
    def test_generate_uses_correct_framework(self, generator, mock_client):
        """Test that correct framework prompt is used."""
        generator.generate("Test something", framework="robot")
        
        call_args = mock_client.generate_code.call_args
        assert "Robot" in call_args.kwargs["system_prompt"] or "robot" in call_args.kwargs["system_prompt"].lower()
```

## Mocking Claude API

```python
@pytest.fixture
def mock_anthropic():
    """Mock the Anthropic client."""
    with patch("aitestkit.utils.claude_client.Anthropic") as mock:
        instance = MagicMock()
        instance.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Generated code here")],
            usage=MagicMock(input_tokens=100, output_tokens=200),
        )
        mock.return_value = instance
        yield mock
```

---

# COMMON TASKS

## Adding a New Framework

1. Create prompt template: `prompts/templates/code-generation/{framework}.md`
2. Update `EXTENSION_MAP` in `output_parser.py`
3. Add validation rules in `output_parser.validate_code()`
4. Add to CLI choices in `cli.py`
5. Create benchmark scenarios in `prompts/benchmarks/`
6. Add tests

## Adding a New Benchmark Scenario

1. Create YAML file in `prompts/benchmarks/scenario_XX_name.yaml`
2. Define scenario_id, name, framework, input scenario
3. Define expected_elements (must_contain, must_not_contain, structure)
4. Define quality_checks with regex patterns
5. Set baseline_score (typically 85)
6. Run `aitestkit regression --all` to verify

## Updating Prompts

1. Edit the prompt file in `prompts/templates/`
2. Run `aitestkit regression --all` to check for regressions
3. If scores drop, adjust the prompt or update baseline
4. Commit with descriptive message about changes

---

# IMPLEMENTATION CHECKLIST

## Phase 1: Core (Days 2-3)
- [ ] `utils/claude_client.py` - Full implementation
- [ ] `config.py` - Full implementation
- [ ] `cli.py` - All 4 commands (generate, analyze, regression, info)
- [ ] `__init__.py` - Version and exports

## Phase 2: Generator (Days 4-7)
- [ ] `generator/context_builder.py`
- [ ] `generator/output_parser.py`
- [ ] `generator/generator.py`
- [ ] Prompt templates (system.md, pytest.md, robot_framework.md, playwright.md)
- [ ] Tests for generator module

## Phase 3: Analyzer (Days 8-10)
- [ ] `analyzer/log_parser.py`
- [ ] `analyzer/analyzer.py`
- [ ] `analyzer/report_generator.py`
- [ ] Prompt template (failure_analysis/system.md)
- [ ] Tests for analyzer module

## Phase 4: Regression (Days 11-13)
- [ ] `regression/scorer.py`
- [ ] `regression/runner.py`
- [ ] `regression/comparator.py`
- [ ] Benchmark scenarios (5+ scenarios)
- [ ] Tests for regression module

## Phase 5: Polish (Days 14-20)
- [ ] Sample app completion
- [ ] GitHub Actions workflows
- [ ] README with examples
- [ ] Documentation
- [ ] Demo script

---

# DEBUGGING TIPS

## API Issues

```python
# Check API key
import os
print(f"API Key set: {bool(os.getenv('ANTHROPIC_API_KEY'))}")

# Test connection
from anthropic import Anthropic
client = Anthropic()
response = client.messages.create(
    model="claude-haiku-4-5-20250514",
    max_tokens=100,
    messages=[{"role": "user", "content": "Say hello"}]
)
print(response.content[0].text)
```

## Path Issues

```python
# Check prompt paths
from aitestkit.config import config
print(f"Prompts dir: {config.prompts_dir}")
print(f"Exists: {config.prompts_dir.exists()}")
print(f"Contents: {list(config.prompts_dir.glob('**/*.md'))}")
```

## Generation Issues

```python
# Debug generation
generator = TestGenerator()
result = generator.generate("Test login", framework="pytest")
print(f"Raw response:\n{result.raw_response}")
print(f"Extracted code:\n{result.code}")
print(f"Validation issues: {result.validation_issues}")
```

---

*AITestKit Development Skill v1.0 - January 2025*