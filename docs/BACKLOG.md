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
  - Commands: `generate`, `feedback`, `analyze`, `regression`, `frameworks`, `info`, `init`
  - `cli.py`

- [ ] **F04: Claude Client** 🔲 Placeholder
  - Wrapper for Anthropic API with model selection and cost tracking
  - `utils/claude_client.py`

### Test Generation

- [ ] **F05: Test Generation** 🔲 Placeholder
  - Core test generation logic using Claude API
  - Components: ContextBuilder, OutputParser, Generator
  - `generator/`

- [ ] **F06: Prompt Templates** 🔲 Placeholder
  - CTCO-framework prompt templates for each supported framework
  - `prompts/templates/`

- [ ] **F09: Few-Shot Examples** ⬜ Not Started
  - Approved test examples used as few-shot prompts
  - `prompts/examples/`

### Feedback Loop

- [ ] **F07: Human Review Flow** ⬜ Not Started
  - Generate to file, user reviews externally, submits feedback via CLI
  - Workflow: generate → review → approve/reject

- [ ] **F08: Feedback Storage** ⬜ Not Started
  - Project-local storage for feedback, history, and patterns
  - `.aitestkit/feedback/` (pending.json, approved.json, rejected.json, patterns.json)

---

## P1 - Important Features (Target: v1.1)

Significant value, not blocking MVP.

### Analysis & Patterns

- [ ] **F10: Failure Analysis** 🔲 Placeholder
  - AI-powered analysis of test failure logs
  - Components: LogParser, Analyzer
  - `analyzer/`

- [ ] **F11: Pattern Identification** ⬜ Not Started
  - Automatically identify patterns in rejection reasons
  - Algorithm: 3+ similar rejections → Pattern identified

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
  - Command: `aitestkit init [--force]`

---

## P1.5 - GitHub Actions (Target: v1.0)

CI/CD automation features.

- [ ] **F23: CI Test Workflow** 🔲 Placeholder
  - Standard CI workflow for AITestKit development
  - Lint + test on push/PR
  - `.github/workflows/test.yml`

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
| **P0**   | 9     | 2           | 4              | 3              |
| **P1**   | 6     | 0           | 1              | 5              |
| **P1.5** | 5     | 0           | 2              | 3              |
| **P2**   | 3     | 0           | 0              | 3              |
| **P3**   | 4     | 0           | 0              | 4              |
| **Total**| 27    | 2           | 7              | 18             |

---

## Next Up

Based on the [Implementation Plan](MASTER_SPEC.md#5-implementation-plan), the next phase is:

**Phase 2: Core CLI** (Target: Week of January 13-17, 2026)

- [ ] 2.1 Implement `claude_client.py` (F04)
- [ ] 2.2 Implement basic CLI structure (F01)
- [ ] 2.3 Implement `frameworks` command
- [ ] 2.4 Implement `info` command
- [ ] 2.5 Implement `init` command
- [ ] 2.6 Write unit tests

---

*For detailed specifications, schemas, and implementation guidance, see [docs/MASTER_SPEC.md](MASTER_SPEC.md)*
