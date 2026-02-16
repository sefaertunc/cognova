# Development Tests (.dev-tests/)

Quick validation tests for development. **Not part of the official test suite.**

> **Note:** This directory is gitignored and local-only. It will not be pushed to the repository.

## Purpose

- **Quick Validation**: Test newly implemented features without full test suite
- **Manual Testing**: Test with real API keys and external services (when implemented)
- **Experimental**: Try out approaches before committing
- **Cost Estimation**: Validate Claude API usage and costs

## Current Structure (v4.0: MCP Server)

- `unit/` - Unit tests for individual modules
  - `test_config.py` - Tests for configuration module (Settings, ProjectConfig, quality tiers)
  - `test_fw_registry.py` - Tests for framework registry
  - `test_dev_conftest.py` - Tests for conftest fixtures
  - (Future: test_mcp_server.py, test_provider.py, test_rules_engine.py)
- `integration/` - End-to-end workflow tests (empty for now)
- `manual/` - Manual test scripts (empty for now)
- `helpers/` - Test utilities and fixtures

## Running Tests

```bash
# Run all dev tests
pytest .dev-tests/ -v

# Run specific test file
pytest .dev-tests/unit/test_config.py -v
```

## vs tests/ Directory

| Feature | tests/ | .dev-tests/ |
|---------|--------|------------|
| Purpose | Official test suite | Development validation |
| CI/CD | Runs in CI | Manual only |
| API Key | Mocked | Real (optional) |
| Coverage | Full coverage | Key features only |
| Speed | Fast (mocked) | Slower (real API) |

## Adding New Tests

When implementing a new module:
1. Create unit test in `unit/test_<module>.py`
2. Add integration test in `integration/` if needed
3. Run tests: `pytest .dev-tests/unit/test_<module>.py`
4. Once stable, add to official `tests/` suite

## Module Test Priority

| Module | Test File | Priority | Notes |
|--------|-----------|----------|-------|
| `mcp_server.py` | `test_mcp_server.py` | P0 | MCP tool registration |
| `providers/claude.py` | `test_provider.py` | P0 | Quality tier resolution |
| `rules/engine.py` | `test_rules_engine.py` | P0 | 3-layer validation |
| `context/analyzer.py` | `test_context.py` | P1 | tree-sitter analysis |
| `repair/repairer.py` | `test_repair.py` | P1 | Repair loop + cost cap |
| `healing/healer.py` | `test_healing.py` | P1 | Suggest mode |

Tests are added **parallel to development**, not ahead of time.
