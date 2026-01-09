# AITestKit Multi-Framework Implementation Roadmap

## Project Vision

Transform AITestKit from a basic 3-framework tool (pytest, Robot Framework, Playwright) into a comprehensive **multi-framework test generation platform** supporting 25+ frameworks across 6 testing categories, powered by Claude AI.

---

## Progress Overview

```
Phase 1: Foundation    ████████████████████ 100% ✅ COMPLETE
Phase 2: CLI           ░░░░░░░░░░░░░░░░░░░░   0% 🔨 NEXT
Phase 3: Testing       ░░░░░░░░░░░░░░░░░░░░   0% 📋 PLANNED
Phase 4: CI/CD         ░░░░░░░░░░░░░░░░░░░░   0% 📋 PLANNED
Phase 5: Verification  ░░░░░░░░░░░░░░░░░░░░   0% 📋 PLANNED
```

---

## Phase 1: Framework Registry Foundation ✅ COMPLETE

**Status:** ✅ Implemented and Committed (Commit: 8cd16b8)

### What We Built

#### 1. Framework Registry System
**File:** `src/aitestkit/frameworks/registry.py` (467 lines)

**Components:**
- `FrameworkCategory` enum (6 categories)
- `FrameworkInfo` dataclass (framework metadata)
- `FRAMEWORKS` dict (25 frameworks defined)
- 9 helper functions for querying and filtering

**Frameworks Added (25 Total):**

| Category | Count | Frameworks |
|----------|-------|------------|
| Unit | 4 | pytest, jest, junit, nunit |
| E2E | 4 | playwright-py, playwright-ts, cypress, selenium-py |
| BDD | 5 | pytest-bdd, cucumber-java, cucumber-js, behave, **robot** ⭐ |
| Performance | 5 | locust, k6, jmeter, gatling, artillery |
| Security | 3 | nuclei, zap, bandit |
| API | 4 | httpx, postman, rest-assured, supertest |

**Priority Distribution:**
- Priority 0 (Core): 11 frameworks
- Priority 1 (Standard): 8 frameworks
- Priority 2 (Extended): 6 frameworks

#### 2. Base Framework Interface
**File:** `src/aitestkit/frameworks/base.py`

- `FrameworkAdapter` abstract base class
- Reserved for future framework-specific extensions
- Methods: `validate_output()`, `get_suggested_filename()`, `post_process()`

#### 3. Module Structure
**File:** `src/aitestkit/frameworks/__init__.py`

- Exports all public functions and classes
- Clean API surface for consumers

#### 4. Project Configuration
**File:** `pyproject.toml` (Updated)

**New Dependencies:**
- `jinja2>=3.1.0` - Template rendering
- `pytest-mock>=3.12.0` - Test mocking
- `pytest-asyncio>=0.23.0` - Async test support
- `hypothesis>=6.0.0` - Property-based testing
- `pre-commit>=3.6.0` - Git hooks

**New Dependency Groups:**
- `dev` - Testing and code quality tools
- `validators` - Framework validators (Robot, Gherkin)
- `sample-app` - FastAPI demo application
- `all` - All optional dependencies

**Tool Configurations:**
- Ruff linting (line-length: 100)
- Black formatting (Python 3.11+)
- MyPy strict type checking
- Pytest with coverage tracking (80% threshold)

#### 5. Test Infrastructure
**Directories Created:**
```
tests/
├── __init__.py
├── conftest.py (placeholder)
├── unit/
│   ├── generator/
│   ├── analyzer/
│   └── regression/
├── integration/
└── fixtures/
    ├── sample_logs/
    ├── mock_responses/
    └── expected_outputs/
```

#### 6. Documentation
- `docs/development/project_plan/AITestKit_MultiFramework_Update_Prompt.md` - Complete spec
- `docs/FRAMEWORK_REGISTRY_GUIDE.md` - User guide (this was just created!)

---

## Phase 2: CLI Implementation 🔨 NEXT UP

**Status:** 🔨 Ready to Implement with Guidance
**File:** `src/aitestkit/cli.py` (Currently a placeholder)

### What We'll Build

#### Commands to Implement

1. **`aitestkit generate`** - Generate test code
   - Dynamic framework selection from registry
   - Context file support
   - Dry-run mode
   - Rich console output

2. **`aitestkit frameworks`** - List frameworks
   - `--list` - Show all frameworks in table
   - `--category` - Filter by category
   - `--language` - Filter by language
   - Rich table formatting

3. **`aitestkit analyze`** - Analyze failures
   - Support multiple output formats (markdown, json, console)
   - Optional output file

4. **`aitestkit regression`** - Run regression tests
   - `--all` - Run all benchmarks
   - `--category` - Run specific category
   - `--prompt` - Test specific prompt

5. **`aitestkit info`** - Show configuration
   - Display framework counts by priority
   - Show API key status
   - Show paths and defaults

#### Key Features to Implement

```python
# Dynamic framework choices from registry
@click.option(
    "--framework", "-f",
    type=click.Choice(get_framework_choices(), case_sensitive=False),
    default="pytest"
)

# Framework validation
fw_info = get_framework(framework)
console.print(f"Generating {fw_info.name} test...")

# Category filtering
@click.option(
    "--category", "-c",
    type=click.Choice([c.value for c in FrameworkCategory])
)
```

### Implementation Guide Available

Ask: **"Guide me through implementing the CLI"**

You'll receive step-by-step guidance on:
1. Importing registry functions
2. Setting up Click command structure
3. Adding dynamic framework selection
4. Implementing each command with examples
5. Adding rich console output
6. Error handling and validation

---

## Phase 3: Test Infrastructure 📋 PLANNED

**Status:** 📋 Planned for Implementation
**File:** `tests/conftest.py` (Currently a placeholder)

### What We'll Build

#### Test Fixtures

1. **Mock Claude API Responses**
   ```python
   @pytest.fixture
   def mock_claude_response() -> str:
       # Return sample pytest test code
   ```

2. **Mock Anthropic Client**
   ```python
   @pytest.fixture
   def mock_anthropic() -> Generator[MagicMock, None, None]:
       # Mock API client to prevent real calls
   ```

3. **Test Configuration**
   ```python
   @pytest.fixture
   def test_config(tmp_path: Path) -> Config:
       # Create test config with temp paths
   ```

4. **CLI Test Runner**
   ```python
   @pytest.fixture
   def cli_runner() -> CliRunner:
       # Click CLI test runner
   ```

5. **Sample Data**
   - Sample log files
   - Mock API responses
   - Expected outputs
   - Benchmark YAML files

#### Unit Tests to Create

- `tests/unit/test_framework_registry.py` - Registry functions
- `tests/unit/test_config.py` - Configuration
- `tests/unit/test_claude_client.py` - API client
- `tests/unit/generator/test_*.py` - Generator modules
- `tests/unit/analyzer/test_*.py` - Analyzer modules
- `tests/unit/regression/test_*.py` - Regression modules

#### Integration Tests to Create

- `tests/integration/test_cli_generate.py` - Generate command
- `tests/integration/test_cli_analyze.py` - Analyze command
- `tests/integration/test_cli_regression.py` - Regression command

### Implementation Guide Available

Ask: **"Guide me through creating test fixtures"**

You'll receive step-by-step guidance on:
1. Creating mock API responses
2. Setting up pytest fixtures
3. Mocking the Anthropic client
4. Writing unit tests for registry
5. Writing integration tests for CLI
6. Using pytest best practices

---

## Phase 4: GitHub Actions CI/CD 📋 PLANNED

**Status:** 📋 Planned for Implementation
**Files:** `.github/workflows/test.yml`, `.github/workflows/prompt-regression.yml`

### What We'll Build

#### 1. Test Workflow (`test.yml`)

**Triggers:**
- Push to main/develop
- Pull requests

**Jobs:**
```yaml
jobs:
  test:
    - Python 3.11, 3.12 matrix
    - Install dependencies
    - Run linting (ruff, black)
    - Run type checking (mypy)
    - Run tests with coverage
    - Upload coverage to codecov

  lint:
    - Standalone lint job
    - Fast feedback on code quality
```

#### 2. Prompt Regression Workflow (`prompt-regression.yml`)

**Triggers:**
- Changes to `src/aitestkit/prompts/**`

**Jobs:**
```yaml
jobs:
  regression:
    - Run regression tests
    - Compare against baseline scores
    - Comment PR with results
    - Fail if scores drop below threshold
```

### Implementation Guide Available

Ask: **"Guide me through creating GitHub Actions workflows"**

You'll receive step-by-step guidance on:
1. Creating workflow files
2. Setting up matrices
3. Configuring secrets (ANTHROPIC_API_KEY)
4. Adding status badges
5. Configuring PR comments
6. Best practices for CI/CD

---

## Phase 5: Verification & Testing 📋 PLANNED

**Status:** 📋 Planned

### Verification Checklist

#### Installation Verification
```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Verify CLI is available
aitestkit --version        # Should show "1.0.0"
which aitestkit            # Should show installed location
```

#### Framework Registry Verification
```bash
# List all frameworks (should show 25)
aitestkit frameworks --list

# Filter by category
aitestkit frameworks --category bdd

# Filter by language
aitestkit frameworks --language Python

# Show info
aitestkit info
```

#### Test Execution
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=aitestkit --cov-report=term-missing

# Should have 80%+ coverage
# All tests should pass (mocked, no real API calls)
```

#### Code Quality Checks
```bash
# Linting
ruff check src/ tests/

# Formatting
black --check src/ tests/

# Type checking
mypy src/

# All should pass with no errors
```

#### Manual Testing
```bash
# Test generate command (dry run)
aitestkit generate "Test user login" -f pytest --dry-run

# Test with each priority 0 framework
for fw in pytest jest playwright-py playwright-ts pytest-bdd cucumber-java locust k6 nuclei httpx robot; do
    echo "Testing $fw..."
    aitestkit generate "Test scenario" -f $fw --dry-run
done
```

---

## Implementation Timeline

### Recommended Order

1. ✅ **Phase 1: Foundation** - COMPLETE (Jan 9, 2026)
2. 🔨 **Phase 2: CLI** - Implement first (1-2 sessions)
   - Start with basic commands
   - Add framework integration
   - Implement rich output

3. 📋 **Phase 3: Testing** - Implement second (1-2 sessions)
   - Create test fixtures
   - Write unit tests
   - Write integration tests

4. 📋 **Phase 4: CI/CD** - Implement third (1 session)
   - Create workflows
   - Test in GitHub
   - Configure secrets

5. 📋 **Phase 5: Verification** - Final validation (1 session)
   - Run all checks
   - Document issues
   - Create examples

---

## How to Get Started

### For Each Phase

1. **Ask for guidance**: e.g., "Guide me through implementing the CLI"
2. **Receive step-by-step instructions** with code examples
3. **Implement incrementally** - small, testable changes
4. **Test as you go** - verify each step works
5. **Commit with conventional commits** - track progress

### Example Workflow

```bash
# 1. Pull latest changes
git pull origin main

# 2. Ask for guidance (in Claude Code)
"Guide me through implementing the CLI"

# 3. Implement the changes with guidance
# (Claude provides step-by-step code examples)

# 4. Test your implementation
aitestkit frameworks --list

# 5. Commit your work
git add -A
git commit -m "feat(cli): implement frameworks list command"
git push origin main

# 6. Move to next feature
"Guide me through implementing the generate command"
```

---

## Resources

### Documentation Files
- `docs/FRAMEWORK_REGISTRY_GUIDE.md` - How to use the registry
- `docs/development/project_plan/AITestKit_MultiFramework_Update_Prompt.md` - Complete spec
- `docs/development/claude/SKILL.md` - Claude Code skill reference
- `CLAUDE.md` - Project overview and conventions

### Code References
- `src/aitestkit/frameworks/registry.py` - Framework definitions
- `src/aitestkit/frameworks/base.py` - Base interface
- `pyproject.toml` - Dependencies and configuration

### External References
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Anthropic API](https://docs.anthropic.com/)

---

## Current State Summary

### What Works Now ✅
- Framework registry with 25 frameworks
- All registry query functions
- Directory structure
- Configuration files
- Documentation

### What's Ready to Build 🔨
- CLI with dynamic framework selection
- Test fixtures and mocking
- Unit and integration tests
- GitHub Actions workflows

### What You Need
- Python 3.11+
- Git
- Anthropic API key (for testing)
- Text editor / IDE

---

## Questions?

**Ready to start?** Ask:
- "Guide me through implementing the CLI"
- "Show me examples of using the framework registry"
- "Help me set up the test fixtures"
- "Walk me through the verification steps"

Each phase has detailed guidance available - just ask!

---

**Last Updated:** 2026-01-09
**Current Phase:** Phase 2 (CLI Implementation)
**Next Milestone:** Complete CLI with all commands
**Total Progress:** 20% (1 of 5 phases complete)
