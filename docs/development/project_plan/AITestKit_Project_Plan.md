# AITestKit - AI-Powered Test Development Toolkit
## Portfolio Project Plan
### Version 1.0 | January 8, 2025

---

# Project Overview

## Vision

An open-source toolkit that demonstrates AI-assisted test automation, featuring intelligent test generation, automated failure analysis, and prompt engineering best practices.

## Why This Project Stands Out

| Differentiator | Impact on CV |
|----------------|--------------|
| AI/LLM Integration | Hot skill, high demand |
| Prompt Engineering | Emerging discipline, few have portfolio examples |
| Working Code + Architecture | Shows both design AND implementation |
| Open Source | Demonstrates collaboration mindset |
| Documentation Quality | Shows technical communication skills |

## Project Name Options

| Name | Pros | Cons |
|------|------|------|
| **AITestKit** | Clear, professional | Generic |
| **TestForge AI** | Memorable, action-oriented | Slightly long |
| **PromptQA** | Highlights prompt engineering | Narrow focus |
| **ClaudeTest** | Direct, recognizable | Tied to one provider |

**Recommendation:** `AITestKit` - clean, professional, extensible

---

# Scope Definition

## In Scope (Must Build)

```
+------------------------------------------------------------------+
|                         CORE DELIVERABLES                         |
+------------------------------------------------------------------+

1. TEST CODE GENERATOR
   - Input: Natural language test scenario
   - Output: Working test file (.robot, .py, or .spec.ts)
   - Model: Claude API (configurable)
   - Human review workflow documented

2. FAILURE ANALYZER
   - Input: Test logs, error messages
   - Output: Root cause analysis report
   - Confidence scoring
   - Suggested fixes

3. PROMPT LIBRARY
   - Version-controlled prompts
   - CTCO framework implementation
   - Product/framework context system
   - Few-shot examples

4. PROMPT REGRESSION TESTER
   - Benchmark scenarios
   - Automated quality scoring
   - Old vs New comparison
   - CI integration ready

5. DOCUMENTATION & DEMOS
   - Professional README
   - Architecture diagrams (you have these!)
   - Usage examples
   - Demo recordings/GIFs
```

## Out of Scope (Not Needed for Portfolio)

```
- Full Azure infrastructure
- Windows VM provisioning
- SharePoint integration
- Teams notifications
- Production Docker images
- Multi-product support (Verikor/Veriket/Verifim)
```

## Target Application for Testing

Instead of Siberson products, we need a **sample application** to test against:

| Option | Pros | Cons |
|--------|------|------|
| **Todo API (build simple one)** | Full control, simple | Extra work |
| **JSONPlaceholder API** | Free, public, no setup | Limited scenarios |
| **PetStore API (Swagger)** | Industry standard demo | Complex |
| **Local Flask/FastAPI app** | Realistic, controllable | Need to build |

**Recommendation:** Build minimal FastAPI app (50 lines) + use JSONPlaceholder for variety

---

# Technology Stack

## Required

| Component | Technology | Cost |
|-----------|------------|------|
| AI Provider | Anthropic Claude API | ~$5-20 for development |
| Language | Python 3.11+ | Free |
| Version Control | GitHub | Free |
| Test Frameworks | Robot Framework, Pytest | Free |
| CI/CD | GitHub Actions | Free tier |

## Optional (Enhances Portfolio)

| Component | Technology | Purpose |
|-----------|------------|---------|
| Sample App | FastAPI | Target for generated tests |
| Containerization | Docker | Shows DevOps skills |
| Documentation | MkDocs / Docusaurus | Professional docs site |
| Demo | Streamlit | Interactive web demo |

---

# Project Structure

```
aitestkit/
│
├── README.md                          # Professional project overview
├── LICENSE                            # MIT License
├── pyproject.toml                     # Project configuration
├── .gitignore
├── .env.example                       # Environment template
│
├── docs/
│   ├── architecture/
│   │   ├── system-overview.md
│   │   ├── ai-integration.md
│   │   └── diagrams/
│   │       ├── ai-integration.png
│   │       └── workflow.png
│   ├── guides/
│   │   ├── getting-started.md
│   │   ├── prompt-engineering.md
│   │   └── extending.md
│   └── examples/
│       ├── generated-tests/
│       └── analysis-reports/
│
├── src/
│   └── aitestkit/
│       ├── __init__.py
│       ├── cli.py                     # Command-line interface
│       ├── config.py                  # Configuration management
│       │
│       ├── generator/                 # Test Code Generation
│       │   ├── __init__.py
│       │   ├── generator.py           # Main generator class
│       │   ├── context_builder.py     # Builds prompts with context
│       │   └── output_parser.py       # Parses AI output
│       │
│       ├── analyzer/                  # Failure Analysis
│       │   ├── __init__.py
│       │   ├── analyzer.py            # Main analyzer class
│       │   ├── log_parser.py          # Extracts relevant info
│       │   └── report_generator.py    # Creates analysis reports
│       │
│       ├── regression/                # Prompt Regression Testing
│       │   ├── __init__.py
│       │   ├── runner.py              # Runs regression tests
│       │   ├── scorer.py              # Scores outputs
│       │   └── comparator.py          # Compares old vs new
│       │
│       ├── prompts/                   # Prompt Library
│       │   ├── templates/
│       │   │   ├── code_generation/
│       │   │   │   ├── system.md
│       │   │   │   ├── robot_framework.md
│       │   │   │   ├── pytest.md
│       │   │   │   └── playwright.md
│       │   │   └── failure_analysis/
│       │   │       └── system.md
│       │   │
│       │   ├── context/
│       │   │   ├── shared/
│       │   │   │   ├── testing_principles.md
│       │   │   │   └── coding_standards.md
│       │   │   └── sample_app/
│       │   │       └── api_reference.md
│       │   │
│       │   ├── examples/
│       │   │   ├── input_scenario_01.txt
│       │   │   ├── output_robot_01.robot
│       │   │   └── output_pytest_01.py
│       │   │
│       │   └── benchmarks/
│       │       ├── scenario_01_crud.yaml
│       │       ├── scenario_02_auth.yaml
│       │       └── scenario_03_error.yaml
│       │
│       └── utils/
│           ├── __init__.py
│           └── claude_client.py       # Claude API wrapper
│
├── tests/                             # Tests for the toolkit itself
│   ├── test_generator.py
│   ├── test_analyzer.py
│   ├── test_regression.py
│   └── fixtures/
│       ├── sample_logs/
│       └── sample_scenarios/
│
├── sample_app/                        # Target application for demos
│   ├── main.py                        # Simple FastAPI app
│   ├── requirements.txt
│   └── README.md
│
├── examples/                          # Usage examples
│   ├── 01_generate_robot_test.py
│   ├── 02_generate_pytest.py
│   ├── 03_analyze_failure.py
│   ├── 04_run_regression.py
│   └── outputs/                       # Generated outputs for showcase
│       ├── generated_test.robot
│       ├── generated_test.py
│       └── analysis_report.md
│
├── scripts/
│   ├── setup.sh
│   └── demo.sh
│
└── .github/
    └── workflows/
        ├── test.yml                   # Run toolkit tests
        ├── prompt-regression.yml      # Validate prompt changes
        └── demo.yml                   # Generate demo outputs
```

---

# Implementation Phases

## Phase 1: Foundation (Days 1-3)
### Goal: Repository setup and core infrastructure

```
DAY 1: Project Setup
--------------------
[ ] Create GitHub repository "aitestkit"
[ ] Initialize Python project (pyproject.toml)
[ ] Set up folder structure
[ ] Create .gitignore, LICENSE (MIT)
[ ] Write initial README.md (placeholder)
[ ] Set up virtual environment
[ ] Install dependencies (anthropic, pyyaml, click)

DAY 2: Claude Client & Config
-----------------------------
[ ] Create claude_client.py wrapper
    - Model selection (opus/sonnet/haiku)
    - Error handling
    - Usage tracking
[ ] Create config.py
    - Load from environment
    - Model configuration
    - Default settings
[ ] Create .env.example
[ ] Test API connection

DAY 3: Basic CLI Structure
--------------------------
[ ] Create cli.py with Click framework
[ ] Implement subcommands structure:
    - aitestkit generate
    - aitestkit analyze
    - aitestkit regression
[ ] Add --help documentation
[ ] Test CLI works
```

**Deliverable:** Working repository with Claude API connection

---

## Phase 2: Test Generator (Days 4-7)
### Goal: Working test code generation

```
DAY 4: Prompt Templates
-----------------------
[ ] Create system.md (main code gen prompt)
    - CTCO framework
    - Role definition
    - Output format
[ ] Create robot_framework.md
[ ] Create pytest.md
[ ] Create testing_principles.md (shared context)

DAY 5: Context Builder
----------------------
[ ] Implement context_builder.py
    - Load templates
    - Merge context files
    - Build complete prompt
[ ] Implement output_parser.py
    - Extract code from response
    - Validate structure
    - Suggest filename

DAY 6: Generator Core
---------------------
[ ] Implement generator.py
    - Accept scenario input
    - Select framework
    - Call Claude API
    - Return structured output
[ ] Add CLI integration
    - aitestkit generate --framework robot "scenario"
    - aitestkit generate --framework pytest "scenario"

DAY 7: Testing & Examples
-------------------------
[ ] Write tests for generator
[ ] Create example scenarios
[ ] Generate sample outputs (for portfolio)
[ ] Document in README
```

**Deliverable:** `aitestkit generate` command working

**Demo Command:**
```bash
aitestkit generate \
  --framework robot \
  --output ./output/ \
  "Test that user can create a new todo item with title and description"
```

---

## Phase 3: Failure Analyzer (Days 8-10)
### Goal: Working failure analysis

```
DAY 8: Analysis Prompt & Log Parser
-----------------------------------
[ ] Create failure_analysis/system.md prompt
    - Role: Senior QA debugging expert
    - Output format: structured report
    - Confidence scoring criteria
[ ] Implement log_parser.py
    - Extract error messages
    - Find stack traces
    - Identify test name

DAY 9: Analyzer Core
--------------------
[ ] Implement analyzer.py
    - Accept log file or text
    - Build analysis prompt
    - Call Claude API (Sonnet)
    - Return structured analysis
[ ] Implement report_generator.py
    - Markdown report format
    - Confidence indicators
    - Suggested actions

DAY 10: CLI & Examples
----------------------
[ ] Add CLI integration
    - aitestkit analyze ./failed_test.log
    - aitestkit analyze --stdin (pipe input)
[ ] Create sample failure logs
[ ] Generate sample analysis reports
[ ] Write tests
```

**Deliverable:** `aitestkit analyze` command working

**Demo Command:**
```bash
aitestkit analyze ./tests/fixtures/sample_logs/timeout_failure.log
```

**Sample Output:**
```markdown
# Failure Analysis Report

**Test:** test_user_login
**Status:** FAILED

## Root Cause Analysis
**Probable Cause:** Database connection timeout
**Confidence:** 87% (High)

## Evidence
- Error: "Connection refused on port 5432"
- Timeout occurred at line 45
- Previous 3 runs: 2 passed, 1 flaky

## Suggested Actions
1. Check database service is running
2. Verify connection string in config
3. Consider increasing timeout to 30s

## Category
Environment Issue (not code bug)
```

---

## Phase 4: Prompt Regression (Days 11-13)
### Goal: Working prompt validation system

```
DAY 11: Benchmark Scenarios
---------------------------
[ ] Create scenario YAML format
[ ] Write 5 benchmark scenarios:
    - scenario_01_crud.yaml
    - scenario_02_auth.yaml
    - scenario_03_validation.yaml
    - scenario_04_error_handling.yaml
    - scenario_05_integration.yaml
[ ] Define expected_elements for each

DAY 12: Scorer & Comparator
---------------------------
[ ] Implement scorer.py
    - Structural score (40 pts)
    - Content score (40 pts)
    - Quality score (20 pts)
[ ] Implement comparator.py
    - Load old prompt (from git)
    - Load new prompt (current)
    - Run both against scenarios
    - Compare scores

DAY 13: Runner & CLI
--------------------
[ ] Implement runner.py
    - Orchestrate full regression
    - Generate report
[ ] Add CLI integration
    - aitestkit regression --prompt ./prompts/system.md
    - aitestkit regression --all
[ ] Create GitHub Actions workflow
[ ] Write tests
```

**Deliverable:** `aitestkit regression` command working

**Demo Output:**
```
Prompt Regression Test Results
==============================

| Scenario          | Old Score | New Score | Status |
|-------------------|-----------|-----------|--------|
| CRUD Operations   | 85        | 92        | ✅ PASS |
| Authentication    | 88        | 90        | ✅ PASS |
| Input Validation  | 82        | 85        | ✅ PASS |
| Error Handling    | 79        | 88        | ✅ PASS |
| Integration       | 84        | 86        | ✅ PASS |

Overall: PASSED (+5.6 average improvement)
```

---

## Phase 5: Sample App & Integration (Days 14-16)
### Goal: Complete demo environment

```
DAY 14: Sample FastAPI App
--------------------------
[ ] Create minimal Todo API
    - GET /todos
    - POST /todos
    - GET /todos/{id}
    - PUT /todos/{id}
    - DELETE /todos/{id}
    - POST /auth/login (mock)
[ ] Add deliberate bugs (for failure analysis demo)
[ ] Document API endpoints

DAY 15: End-to-End Demo
-----------------------
[ ] Generate tests for sample app
[ ] Run tests (some should fail)
[ ] Analyze failures
[ ] Document the workflow
[ ] Create demo script (demo.sh)

DAY 16: GitHub Actions
----------------------
[ ] Create test.yml (toolkit tests)
[ ] Create prompt-regression.yml
[ ] Create demo.yml (showcase generation)
[ ] Verify all workflows pass
```

**Deliverable:** Complete working demo

---

## Phase 6: Documentation & Polish (Days 17-20)
### Goal: Portfolio-ready presentation

```
DAY 17: README Excellence
-------------------------
[ ] Professional README with:
    - Clear value proposition
    - Beautiful badges
    - Architecture diagram
    - Quick start guide
    - Feature showcase with GIFs/screenshots
    - Installation instructions
    - Usage examples
    - Contributing guide

DAY 18: Documentation Site (Optional but Impressive)
---------------------------------------------------
[ ] Set up MkDocs or similar
[ ] Architecture documentation
[ ] API reference
[ ] Tutorial: "Generate Your First Test"
[ ] Deploy to GitHub Pages

DAY 19: Demo Assets
-------------------
[ ] Record terminal GIFs (asciinema)
[ ] Create screenshots
[ ] Write blog post / dev.to article
[ ] Prepare LinkedIn post

DAY 20: Final Polish
--------------------
[ ] Code cleanup
[ ] Add docstrings
[ ] Final testing
[ ] Tag v1.0.0 release
[ ] Share publicly
```

**Deliverable:** Portfolio-ready project

---

# Timeline Summary

```
+------------------------------------------------------------------+
|                        20-DAY TIMELINE                            |
+------------------------------------------------------------------+

Week 1 (Days 1-7): Foundation + Generator
-----------------------------------------
[====] Foundation (Days 1-3)
[======] Test Generator (Days 4-7)

Week 2 (Days 8-13): Analyzer + Regression
-----------------------------------------
[====] Failure Analyzer (Days 8-10)
[====] Prompt Regression (Days 11-13)

Week 3 (Days 14-20): Integration + Polish
-----------------------------------------
[====] Sample App & Demo (Days 14-16)
[=====] Documentation & Polish (Days 17-20)


MILESTONES:
-----------
Day 3:  ✓ Repository live, API working
Day 7:  ✓ Can generate tests
Day 10: ✓ Can analyze failures
Day 13: ✓ Can validate prompts
Day 16: ✓ Complete working demo
Day 20: ✓ Portfolio ready
```

---

# Key Files to Showcase

## Most Important for Portfolio

| File | Why It Matters |
|------|----------------|
| `README.md` | First impression, shows communication skills |
| `src/aitestkit/generator/generator.py` | Core AI integration code |
| `src/aitestkit/prompts/templates/code_generation/system.md` | Prompt engineering skills |
| `examples/outputs/` | Proof it works |
| `docs/architecture/` | System design thinking |
| `.github/workflows/` | CI/CD knowledge |

## Demo Commands for Interviews

```bash
# Generate a test
aitestkit generate --framework pytest \
  "Test user registration with valid email and password"

# Analyze a failure
aitestkit analyze ./failed_test.log

# Run prompt regression
aitestkit regression --all

# Full demo
./scripts/demo.sh
```

---

# Resume/CV Entry

```
AITestKit - AI-Powered Test Development Toolkit
-----------------------------------------------
Open-source toolkit for AI-assisted test automation

• Developed intelligent test generator using Claude API 
  (Opus 4.5) that converts natural language scenarios 
  into Robot Framework, Pytest, and Playwright tests

• Built automated failure analysis system with 
  confidence scoring and root cause detection

• Implemented prompt regression testing framework to 
  validate prompt quality changes with automated CI/CD

• Technologies: Python, Claude API, GitHub Actions, 
  Robot Framework, Pytest, FastAPI

GitHub: github.com/[username]/aitestkit
```

---

# LinkedIn Post Template

```
🚀 Excited to share my latest project: AITestKit

An open-source toolkit that brings AI assistance to 
test automation:

✅ Generate test code from plain English descriptions
✅ Automatically analyze test failures with AI
✅ Validate prompt quality with regression testing

Built with:
• Claude API (Anthropic)
• Python
• Robot Framework / Pytest
• GitHub Actions

Key insight: AI doesn't replace QA engineers - it 
accelerates them. Human review remains essential.

Check it out: [GitHub Link]

#QA #TestAutomation #AI #Python #OpenSource
```

---

# Risk Mitigation

| Risk | Mitigation |
|------|------------|
| API costs | Set budget limit ($20), use Haiku for testing |
| Scope creep | Strict phase boundaries, MVP focus |
| Time constraints | Core features first, polish later |
| Complexity | Start simple, iterate |
| Burnout | 20-day plan, not 7-day sprint |

---

# Success Criteria

## Minimum Viable Portfolio (Must Have)

- [ ] Working `aitestkit generate` command
- [ ] Working `aitestkit analyze` command
- [ ] Professional README with examples
- [ ] At least 3 generated test examples
- [ ] At least 2 analysis report examples
- [ ] GitHub repository public

## Strong Portfolio (Should Have)

- [ ] All above plus:
- [ ] Working `aitestkit regression` command
- [ ] GitHub Actions CI/CD
- [ ] Sample application
- [ ] Demo GIFs/screenshots
- [ ] Architecture documentation

## Impressive Portfolio (Nice to Have)

- [ ] All above plus:
- [ ] Documentation website
- [ ] Blog post / article
- [ ] 10+ GitHub stars
- [ ] Mentioned in resume with metrics

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 8, 2025 | Sefa | Initial project plan |

---

*Let's build something impressive! 🚀*
