# Development Tests (dev_tests/)

Quick validation tests for development. **Not part of the official test suite.**

## Purpose

- **Quick Validation**: Test newly implemented features without full test suite
- **Manual Testing**: Test with real API keys and external services (when implemented)
- **Experimental**: Try out approaches before committing
- **Cost Estimation**: Validate Claude API usage and costs (Phase 3+)

## Current Structure (Phase 2)

- `unit/` - Unit tests for individual modules
  - `test_config.py` - Tests for configuration module ✅
  - (Future: test_claude_client.py, test_frameworks.py, etc.)
- `integration/` - End-to-end workflow tests (empty for now, will add when CLI is ready)
- `manual/` - Manual test scripts (empty for now, will add when claude_client.py exists)
- `helpers/` - Test utilities and fixtures

## Running Tests

```bash
# Run all dev tests
pytest dev_tests/ -v

# Run specific test file
pytest dev_tests/unit/test_config.py -v

# Or run as standalone script
python dev_tests/unit/test_config.py
```

## vs tests/ Directory

| Feature | tests/ | dev_tests/ |
|---------|--------|------------|
| Purpose | Official test suite | Development validation |
| CI/CD | ✅ Runs in CI | ❌ Manual only |
| API Key | ❌ Mocked | ✅ Real (optional) |
| Coverage | Full coverage | Key features only |
| Speed | Fast (mocked) | Slower (real API) |

## Adding New Tests

When implementing a new module:
1. Create unit test in `unit/test_<module>.py`
2. Add integration test in `integration/` if needed
3. Run tests: `pytest dev_tests/unit/test_<module>.py`
4. Once stable, add to official `tests/` suite

## Development Workflow

**Current Phase (Phase 2):**
- ✅ `config.py` → `unit/test_config.py` (implemented)
- ⏳ `claude_client.py` → Will add `unit/test_claude_client.py` after implementation
- ⏳ `cli.py` → Will add `integration/test_cli_commands.py` after implementation

Tests are added **parallel to development**, not ahead of time.
