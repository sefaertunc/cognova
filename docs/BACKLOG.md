# AITestKit Feature Backlog

> This backlog is extracted from [MASTER_SPEC.md](MASTER_SPEC.md) Section 4. For detailed specifications, refer to the master document.

## Legend

- ✅ **Complete** - Implemented and tested
- 🔲 **Placeholder** - File exists but not implemented
- ⬜ **Not Started** - Not yet begun
- 🔨 **In Progress** - Currently being worked on

---

## P0 - Core MVP (Target: v1.0)

Essential features for basic functionality.

### Core Infrastructure

- [x] **F02: Framework Registry** ✅ Complete
  - Central registry of 25 testing frameworks across 6 categories
  - `frameworks/registry.py`

- [x] **F03: Config Management** ✅ Complete
  - Pydantic-based configuration with environment variable support
  - `config.py`

- [ ] **F01: CLI Framework** 🔲 Placeholder
  - Click-based command-line interface with Rich console output
  - Commands: `scenario`, `generate`, `feedback`, `analyze`, `regression`, `frameworks`, `memory`, `info`, `init`
  - `cli.py`

- [ ] **F04: Claude Client** 🔲 Placeholder
  - Wrapper for Anthropic API with model selection and cost tracking
  - `utils/claude_client.py`

- [ ] **F30: Error Handling Module** 🔲 Placeholder (NEW)
  - Structured exception hierarchy with exit codes
  - `errors.py`
  - See MASTER_SPEC.md Section 6

### Scenario System (NEW - REQUIRED)

- [ ] **F31: Scenario Loader** 🔲 Placeholder (NEW)
  - Load and parse scenario YAML files into Pydantic models
  - `scenario/loader.py`

- [ ] **F32: Scenario Validator** 🔲 Placeholder (NEW)
  - Three-tier validation (Required/Recommended/Optional)
  - `scenario/validator.py`
  - See MASTER_SPEC.md Section 9.4

- [ ] **F33: Scenario Migrator** 🔲 Placeholder (NEW)
  - Schema version migration with backup
  - `scenario/migrator.py`
  - See MASTER_SPEC.md Section 7

- [ ] **F34: Scenario CLI Commands** ⬜ Not Started (NEW)
  - `scenario init` - Create scenario from template
  - `scenario validate` - Validate scenario file(s)
  - `scenario migrate` - Migrate to latest schema

### Test Generation

- [ ] **F05: Test Generation** 🔲 Placeholder
  - Core test generation logic using Claude API
  - Components: ContextBuilder, OutputParser, Generator, SCoT
  - `generator/`

- [ ] **F06: Prompt Templates** 🔲 Placeholder
  - CTCO-framework prompt templates for each supported framework
  - SCoT reasoning templates
  - `prompts/templates/`

- [ ] **F09: Few-Shot Examples** ⬜ Not Started
  - Approved test examples used as few-shot prompts
  - `prompts/examples/`

### Feedback Loop

- [ ] **F07: Human Review Flow** ⬜ Not Started
  - Generate to file, user reviews externally, submits feedback via CLI
  - Workflow: generate → review → approve/reject

- [ ] **F08: Feedback Storage** 🔲 Placeholder
  - Project-local storage for feedback, history, and patterns
  - Memvid + JSON fallback
  - `feedback/storage.py`, `feedback/patterns.py`

### Semantic Memory (ELEVATED to P0)

- [ ] **F29: Smart Memory Layer** 🔲 Placeholder (Elevated from P1.5)
  - Memvid-based vector storage for feedback patterns
  - Semantic search across past generations
  - Dynamic few-shot example selection (CEDAR-style)
  - Commands: `memory init`, `memory stats`, `memory search`, `memory export`, `memory rebuild`
  - `memory/memvid_store.py`, `memory/embeddings.py`, `memory/retrieval.py`
  - Location: `.aitestkit/memory/`

### Docker Distribution (NEW - REQUIRED)

- [ ] **F35: Docker Infrastructure** 🔲 Placeholder
  - Dockerfile for containerized distribution
  - Wrapper scripts (sh, bat, ps1)
  - Install script
  - `docker/Dockerfile`, `scripts/`
  - See MASTER_SPEC.md Section 12.3

---

## P1 - Important Features (Target: v1.1)

Significant value, not blocking MVP.

### Analysis & Patterns

- [ ] **F10: Failure Analysis** 🔲 Placeholder
  - AI-powered analysis of test failure logs
  - Components: LogParser, Analyzer
  - `analyzer/`

- [ ] **F11: Pattern Identification** 🔲 Placeholder
  - Automatically identify patterns in rejection reasons
  - Algorithm: 3+ similar rejections → Pattern identified
  - `feedback/patterns.py`

- [ ] **F12: Prompt Regression** 🔲 Placeholder
  - Automated validation that prompt changes don't degrade quality
  - Components: Scorer, Runner, Benchmarks
  - `regression/`

### Tracking & History

- [ ] **F13: Cost Tracking** ⬜ Not Started
  - Track API usage and costs for budgeting
  - Per-call cost calculation, session total, export to JSON/CSV

- [ ] **F14: Generation History** ⬜ Not Started
  - Track all generation attempts for analytics and debugging
  - `.aitestkit/history/generations.json`

### Project Management

- [ ] **F17: Project Init** ⬜ Not Started (Elevated from P2)
  - Initialize project with `.aitestkit/` directory
  - Creates `project.yaml`, feedback files, memory directory
  - Command: `aitestkit init [--force]`

---

## P1.5 - GitHub Actions (Target: v1.0)

CI/CD automation features.

- [ ] **F23: CI Test Workflow** 🔲 Placeholder
  - Standard CI workflow for AITestKit development
  - Lint + test on push/PR
  - `.github/workflows/test.yml`

- [ ] **F36: Docker Build Workflow** 🔲 Placeholder
  - Build and push Docker image to GHCR
  - Trigger: Push to main, tags
  - `.github/workflows/docker.yml`

- [ ] **F24: Auto CHANGELOG** ⬜ Not Started
  - Generate CHANGELOG.md from conventional commits
  - Trigger: Push to main
  - `.github/workflows/release.yml`

- [ ] **F25: AI Version Log** ⬜ Not Started
  - Generate human-readable release notes using Claude AI
  - Output: `RELEASE_NOTES.md`
  - `.github/workflows/release.yml`

- [ ] **F26: Prompt Regression Action** 🔲 Placeholder
  - Validate prompt quality on PRs modifying templates
  - Behavior: Block PR if regression detected
  - `.github/workflows/prompt-regression.yml`

- [ ] **F27: Auto-Lint on Approve** ⬜ Not Started
  - Run framework-specific linting on approved tests
  - Trigger: Push modifying `approved.json`
  - `.github/workflows/lint-approved.yml`

### Multi-Model Pipeline

- [ ] **F28: Multi-Agent Pipeline** ⬜ Not Started (Phase 3)
  - Subagent orchestration for complex test generation
  - Flags: `--thorough`, `--validate`, `--full`
  - Default: Opus (baseline)
  - Optional: Multi-model pipelines for higher quality

### LLM-as-Judge

- [ ] **F37: LLM-as-Judge Validation** ⬜ Not Started (NEW - Phase 7)
  - Use Haiku to validate generated code quality
  - Catches: time.sleep, TODO/FIXME, empty bodies
  - `judge/validator.py`

---

## P2 - Nice-to-Have (Target: v1.2+)

Quality of life improvements.

- [ ] **F15: Demo Workflow** ⬜ Not Started
  - Interactive demo mode showing AITestKit capabilities
  - `.github/workflows/demo.yml`

- [ ] **F16: Auto-Prompt Update** ⬜ Not Started
  - Suggest prompt improvements based on rejection patterns

- [ ] **F18: Config Profiles** ⬜ Not Started
  - Named configuration profiles for different use cases

### Advanced Memory

- [ ] **F38: Dual Embedding** ⬜ Not Started (Phase 8)
  - code-search-ada + text-embedding-3-small
  - `memory/embeddings.py`

- [ ] **F39: CEDAR Retrieval** ⬜ Not Started (Phase 8)
  - Context-aware dynamic example retrieval
  - `memory/retrieval.py`

---

## P3 - Future (Target: v2.0+)

Long-term roadmap.

- [ ] **F19: Web Dashboard** ⬜ Not Started
  - Browser-based UI for generation and review

- [ ] **F20: Team Collaboration** ⬜ Not Started
  - Shared feedback and pattern learning across teams

- [ ] **F21: Custom Framework Support** ⬜ Not Started
  - User-defined frameworks beyond the 25 built-in

- [ ] **F22: IDE Plugins** ⬜ Not Started
  - VS Code and IntelliJ integrations

---

## Status Summary

| Priority | Total | ✅ Complete | 🔲 Placeholder | ⬜ Not Started |
|----------|-------|-------------|----------------|----------------|
| **P0**   | 16    | 2           | 11             | 3              |
| **P1**   | 6     | 0           | 3              | 3              |
| **P1.5** | 9     | 0           | 3              | 6              |
| **P2**   | 5     | 0           | 0              | 5              |
| **P3**   | 4     | 0           | 0              | 4              |
| **Total**| 40    | 2           | 17             | 21             |

---

## Next Up

Based on the [Implementation Plan](MASTER_SPEC.md#5-implementation-plan), the next phase is:

**Phase 2: Docker + CLI** (Current)

- [x] 2.1 Create Dockerfile (placeholder)
- [x] 2.2 Create wrapper scripts (sh, bat, ps1) (placeholder)
- [x] 2.3 Create install script (placeholder)
- [x] 2.4 Create error handling module structure (`errors.py`) (placeholder)
- [x] 2.5 Create scenario module structure (loader, validator, migrator) (placeholder)
- [x] 2.11 Set up GitHub Actions for Docker build (placeholder)
- [ ] 2.6 Implement `scenario init` command
- [ ] 2.7 Implement `scenario validate` command
- [ ] 2.8 Implement `frameworks` command
- [ ] 2.9 Implement `info` command
- [ ] 2.10 Implement `init` command
- [ ] 2.12 Write unit tests

---

*For detailed specifications, schemas, and implementation guidance, see [docs/MASTER_SPEC.md](MASTER_SPEC.md)*
