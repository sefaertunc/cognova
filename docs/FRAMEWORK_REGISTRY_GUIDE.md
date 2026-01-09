# Framework Registry User Guide

## Overview

The Framework Registry is the core component of AITestKit's multi-framework architecture. It provides a centralized, data-driven system for managing 25+ testing frameworks across 6 categories.

**Version:** 1.0.0
**Status:** ✅ Implemented and Ready to Use

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Framework Categories](#framework-categories)
3. [Using the Registry](#using-the-registry)
4. [Framework Information](#framework-information)
5. [Implementation Status](#implementation-status)
6. [Examples](#examples)
7. [Extending the Registry](#extending-the-registry)

---

## Quick Start

### Import the Registry

```python
from aitestkit.frameworks.registry import (
    get_framework,
    list_frameworks,
    get_framework_choices,
    FrameworkCategory,
    FRAMEWORKS,
)
```

### Get a Specific Framework

```python
# Get pytest framework info
fw = get_framework("pytest")
print(fw.name)          # "pytest"
print(fw.language)      # "Python"
print(fw.extension)     # ".py"
print(fw.category)      # FrameworkCategory.UNIT
print(fw.priority)      # 0 (Core)
```

### List All Frameworks

```python
# Get all frameworks
all_frameworks = list_frameworks()
print(f"Total: {len(all_frameworks)} frameworks")

# Get frameworks by category
perf_frameworks = list_frameworks(category=FrameworkCategory.PERFORMANCE)
for fw in perf_frameworks:
    print(f"{fw.name}: {fw.description}")
```

---

## Framework Categories

The registry organizes frameworks into 6 main categories:

### 1. Unit Testing (`FrameworkCategory.UNIT`)
Frameworks for unit and integration testing:
- **pytest** - Python unit/integration testing
- **jest** - JavaScript/TypeScript testing
- **junit** - Java unit testing (JUnit 5)
- **nunit** - .NET unit testing

### 2. E2E Testing (`FrameworkCategory.E2E`)
End-to-end and browser testing frameworks:
- **playwright-py** - Cross-browser E2E (Python)
- **playwright-ts** - Cross-browser E2E (TypeScript)
- **cypress** - JavaScript E2E testing
- **selenium-py** - Browser automation (Python)

### 3. BDD Testing (`FrameworkCategory.BDD`)
Behavior-driven development frameworks:
- **pytest-bdd** - Gherkin BDD (Python)
- **cucumber-java** - Gherkin BDD (Java)
- **cucumber-js** - Gherkin BDD (JavaScript)
- **behave** - BDD framework (Python)
- **robot** - Keyword-driven automation (Python) ⭐ *Original framework*

### 4. Performance Testing (`FrameworkCategory.PERFORMANCE`)
Load and performance testing tools:
- **locust** - Python load testing
- **k6** - Modern load testing (JavaScript)
- **jmeter** - Enterprise performance testing (XML)
- **gatling** - High-performance load testing (Scala)
- **artillery** - Cloud-scale load testing (YAML)

### 5. Security Testing (`FrameworkCategory.SECURITY`)
Security and vulnerability testing:
- **nuclei** - Template-based vulnerability scanner (YAML)
- **zap** - OWASP ZAP security scanner (Python)
- **bandit** - Python security linter

### 6. API Testing (`FrameworkCategory.API`)
REST API testing frameworks:
- **httpx** - pytest + httpx (Python)
- **postman** - Postman/Newman collections (JSON)
- **rest-assured** - REST API testing (Java)
- **supertest** - Node.js API testing (JavaScript)

---

## Using the Registry

### Core Functions

#### `get_framework(name: str) -> FrameworkInfo`

Get detailed information about a specific framework.

```python
from aitestkit.frameworks.registry import get_framework

# Get framework info
playwright = get_framework("playwright-py")
print(playwright.name)              # "Playwright"
print(playwright.language)          # "Python"
print(playwright.extension)         # ".py"
print(playwright.prompt_template)   # "e2e/playwright_python.md"
print(playwright.description)       # "Cross-browser E2E testing (Python)"
```

**Raises:** `ValueError` if framework name is not found.

---

#### `list_frameworks(...) -> list[FrameworkInfo]`

List frameworks with optional filtering.

**Parameters:**
- `category: FrameworkCategory | None` - Filter by category
- `language: str | None` - Filter by programming language
- `priority: int | None` - Filter by priority (0, 1, or 2)

**Returns:** List of `FrameworkInfo` objects, sorted by priority then name.

```python
from aitestkit.frameworks.registry import list_frameworks, FrameworkCategory

# Get all Python frameworks
python_frameworks = list_frameworks(language="Python")

# Get all performance testing frameworks
perf_frameworks = list_frameworks(category=FrameworkCategory.PERFORMANCE)

# Get core (priority 0) frameworks only
core_frameworks = list_frameworks(priority=0)

# Combine filters: Python BDD frameworks
python_bdd = list_frameworks(
    category=FrameworkCategory.BDD,
    language="Python"
)
```

---

#### `get_framework_choices() -> list[str]`

Get a sorted list of all framework identifiers (useful for CLI choices).

```python
from aitestkit.frameworks.registry import get_framework_choices

choices = get_framework_choices()
# ['artillery', 'bandit', 'behave', 'cucumber-java', 'cucumber-js', ...]

# Use in Click CLI
import click

@click.option(
    "--framework",
    "-f",
    type=click.Choice(get_framework_choices(), case_sensitive=False),
    default="pytest"
)
def generate(framework: str):
    pass
```

---

#### `get_frameworks_by_category() -> dict[FrameworkCategory, list[FrameworkInfo]]`

Get all frameworks organized by category.

```python
from aitestkit.frameworks.registry import get_frameworks_by_category

frameworks_by_cat = get_frameworks_by_category()

# Iterate by category
for category, frameworks in frameworks_by_cat.items():
    print(f"\n{category.value.upper()}:")
    for fw in frameworks:
        print(f"  - {fw.name} ({fw.language})")
```

---

#### `validate_framework(name: str) -> bool`

Check if a framework name is valid.

```python
from aitestkit.frameworks.registry import validate_framework

if validate_framework("pytest"):
    print("Valid framework!")

if not validate_framework("unknown"):
    print("Invalid framework name")
```

---

#### `get_core_frameworks() -> list[FrameworkInfo]`

Get priority 0 (core) frameworks that should be implemented first.

```python
from aitestkit.frameworks.registry import get_core_frameworks

core = get_core_frameworks()
print(f"{len(core)} core frameworks")
# Includes: pytest, jest, playwright-py, playwright-ts, pytest-bdd,
#           cucumber-java, locust, k6, nuclei, httpx, robot
```

---

## Framework Information

Each framework is represented by a `FrameworkInfo` dataclass with the following attributes:

```python
@dataclass(frozen=True)
class FrameworkInfo:
    name: str                           # Display name
    category: FrameworkCategory         # Testing category
    language: str                       # Programming language
    extension: str                      # File extension
    prompt_template: str                # Prompt template path
    description: str                    # Human-readable description
    priority: int = 0                   # 0=core, 1=standard, 2=extended
    multi_file: bool = False            # Generates multiple files?
    secondary_extension: str | None = None  # For multi-file frameworks
```

### Priority Levels

- **Priority 0 (Core)**: 11 frameworks - implement first
- **Priority 1 (Standard)**: 8 frameworks - implement second
- **Priority 2 (Extended)**: 6 frameworks - implement later

### Multi-File Frameworks

Some frameworks generate multiple files (e.g., BDD frameworks):

```python
from aitestkit.frameworks.registry import get_framework

# pytest-bdd generates .feature + _steps.py
pytest_bdd = get_framework("pytest-bdd")
print(pytest_bdd.multi_file)           # True
print(pytest_bdd.extension)            # ".feature"
print(pytest_bdd.secondary_extension)  # "_steps.py"

# cucumber-java generates .feature + Steps.java
cucumber = get_framework("cucumber-java")
print(cucumber.secondary_extension)    # "Steps.java"
```

---

## Implementation Status

### ✅ Completed (Phase 1)

- [x] Framework registry module structure
- [x] `FrameworkInfo` dataclass definition
- [x] `FrameworkCategory` enum
- [x] 25 frameworks defined in `FRAMEWORKS` dict
- [x] All registry helper functions implemented
- [x] Robot Framework added to BDD category
- [x] Test directory structure created
- [x] `pyproject.toml` configuration updated

### 🔨 In Progress (Phase 2-4)

**Phase 2: CLI Implementation** (To be implemented with guidance)
- [ ] Import registry functions into CLI
- [ ] Update `generate` command with dynamic framework selection
- [ ] Add `frameworks` command to list available frameworks
- [ ] Update `info` command to show framework statistics
- [ ] Add framework validation in commands

**Phase 3: Test Infrastructure** (To be implemented with guidance)
- [ ] Create test fixtures in `tests/conftest.py`
- [ ] Mock Claude API responses
- [ ] Create framework registry unit tests
- [ ] Add integration tests for CLI commands

**Phase 4: GitHub Actions** (To be implemented with guidance)
- [ ] Create `.github/workflows/test.yml`
- [ ] Create `.github/workflows/prompt-regression.yml`
- [ ] Configure CI/CD pipeline

---

## Examples

### Example 1: Building a Framework Selector UI

```python
from aitestkit.frameworks.registry import get_frameworks_by_category
from rich.console import Console
from rich.table import Table

console = Console()

def show_frameworks():
    """Display all frameworks organized by category."""
    frameworks_by_cat = get_frameworks_by_category()

    table = Table(title="Available Testing Frameworks")
    table.add_column("Category", style="cyan")
    table.add_column("Framework", style="green")
    table.add_column("Language")
    table.add_column("Extension")

    for category, frameworks in frameworks_by_cat.items():
        for fw in frameworks:
            table.add_row(
                category.value,
                fw.name,
                fw.language,
                fw.extension
            )

    console.print(table)
```

### Example 2: Validating User Input

```python
from aitestkit.frameworks.registry import get_framework, validate_framework

def select_framework(user_input: str):
    """Validate and return framework info from user input."""
    if not validate_framework(user_input):
        available = ", ".join(get_framework_choices())
        raise ValueError(
            f"Unknown framework: '{user_input}'\n"
            f"Available: {available}"
        )

    return get_framework(user_input)

# Usage
try:
    fw = select_framework("pytest")
    print(f"Selected: {fw.name} ({fw.language})")
except ValueError as e:
    print(f"Error: {e}")
```

### Example 3: Filter and Generate

```python
from aitestkit.frameworks.registry import list_frameworks, FrameworkCategory

def get_python_frameworks():
    """Get all Python testing frameworks."""
    return list_frameworks(language="Python")

def get_web_testing_frameworks():
    """Get frameworks for web testing (E2E + BDD)."""
    e2e = list_frameworks(category=FrameworkCategory.E2E)
    bdd = list_frameworks(category=FrameworkCategory.BDD)
    return e2e + bdd

# Print Python frameworks
for fw in get_python_frameworks():
    print(f"{fw.name:20} {fw.category.value:15} {fw.extension}")
```

### Example 4: Generate File Names

```python
from aitestkit.frameworks.registry import get_framework

def generate_test_filename(framework_name: str, test_name: str) -> str:
    """Generate appropriate test filename for framework."""
    fw = get_framework(framework_name)

    # Clean test name
    clean_name = test_name.lower().replace(" ", "_")

    # Add appropriate prefix/suffix based on framework
    if fw.category.value == "unit":
        clean_name = f"test_{clean_name}"

    # Add extension
    return f"{clean_name}{fw.extension}"

# Examples
print(generate_test_filename("pytest", "user login"))      # test_user_login.py
print(generate_test_filename("jest", "user login"))        # test_user_login.test.ts
print(generate_test_filename("robot", "user login"))       # test_user_login.robot
print(generate_test_filename("locust", "api load"))        # test_api_load.py
```

---

## Extending the Registry

### Adding a New Framework

To add a new framework to the registry:

1. **Edit** `src/aitestkit/frameworks/registry.py`
2. **Add entry** to the `FRAMEWORKS` dict:

```python
FRAMEWORKS: dict[str, FrameworkInfo] = {
    # ... existing frameworks ...

    "your-framework": FrameworkInfo(
        name="Your Framework Name",
        category=FrameworkCategory.UNIT,  # Choose appropriate category
        language="Python",
        extension=".py",
        prompt_template="unit/your_framework.md",
        description="Brief description of the framework",
        priority=1,  # 0=core, 1=standard, 2=extended
        multi_file=False,  # Set to True if generates multiple files
        secondary_extension=None,  # Only if multi_file=True
    ),
}
```

3. **Create prompt template** in `src/aitestkit/prompts/templates/code-generation/`
4. **Add benchmark scenario** in `src/aitestkit/prompts/benchmarks/`
5. **Test** the new framework with the CLI

### Example: Adding Mocha Framework

```python
"mocha": FrameworkInfo(
    name="Mocha",
    category=FrameworkCategory.UNIT,
    language="JavaScript",
    extension=".test.js",
    prompt_template="unit/mocha.md",
    description="JavaScript testing framework",
    priority=2,
),
```

---

## Best Practices

### 1. Always Validate Framework Names

```python
from aitestkit.frameworks.registry import validate_framework, get_framework

framework_name = user_input.lower()

if validate_framework(framework_name):
    fw = get_framework(framework_name)
else:
    print(f"Invalid framework: {framework_name}")
```

### 2. Use Category Filtering

```python
# Instead of iterating all frameworks
from aitestkit.frameworks.registry import list_frameworks, FrameworkCategory

# Filter by category first
api_frameworks = list_frameworks(category=FrameworkCategory.API)
```

### 3. Handle Multi-File Frameworks

```python
from aitestkit.frameworks.registry import get_framework

fw = get_framework("pytest-bdd")

if fw.multi_file:
    primary_file = f"test_scenario{fw.extension}"
    secondary_file = f"test_scenario{fw.secondary_extension}"
    print(f"Will generate: {primary_file} and {secondary_file}")
```

### 4. Respect Priority Levels

```python
from aitestkit.frameworks.registry import get_core_frameworks

# Implement core frameworks first
core_frameworks = get_core_frameworks()
print("Implement these frameworks first:")
for fw in core_frameworks:
    print(f"  - {fw.name}")
```

---

## Troubleshooting

### Framework Not Found

```python
from aitestkit.frameworks.registry import get_framework

try:
    fw = get_framework("unknown-framework")
except ValueError as e:
    print(e)  # Shows available frameworks
```

### Finding Framework by Language

```python
from aitestkit.frameworks.registry import list_frameworks

# Case-insensitive language filtering
java_frameworks = list_frameworks(language="java")
python_frameworks = list_frameworks(language="Python")
```

---

## Reference

- **Registry Module**: `src/aitestkit/frameworks/registry.py`
- **Base Interface**: `src/aitestkit/frameworks/base.py`
- **Implementation Plan**: `docs/development/project_plan/AITestKit_MultiFramework_Update_Prompt.md`
- **Plan File**: `~/.claude/plans/mighty-noodling-forest.md`

---

## Next Steps

Ready to implement? Ask for guidance:
- "Guide me through implementing the CLI"
- "Guide me through creating test fixtures"
- "Guide me through creating GitHub Actions workflows"

Each phase can be broken down into smaller, manageable steps with detailed examples and explanations.

---

**Last Updated:** 2026-01-09
**Framework Count:** 25
**Status:** Foundation Complete, Ready for Implementation
