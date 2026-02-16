import pytest

def test_project_root(project_root):
    """Test project_root fixture."""
    assert project_root.is_dir()
    assert (project_root / "src").is_dir()

def test_temp_env_file(temp_env_file):
    content = temp_env_file.read_text()
    assert "ANTHROPIC_API_KEY=test-key-12345" in content

def test_mock_api_key(mock_api_key):
    import os
    assert os.getenv("ANTHROPIC_API_KEY") == "test-key-12345"

def test_has_real_api_key(has_real_api_key):
    import os
    real_key = os.getenv("ANTHROPIC_API_KEY")
    if real_key and real_key != "test-key-12345":
        assert has_real_api_key is True
    else:
        assert has_real_api_key is False
