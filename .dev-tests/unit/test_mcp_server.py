from mcp.server.fastmcp import FastMCP
from cognova.mcp_server import mcp, main, init_project
import pytest


def test_mcp_instance_exists():
    assert isinstance(mcp, FastMCP)


def test_mcp_server_name():
    assert mcp.name == "Cognova"


def test_main_function_exists():
    assert callable(main)


def test_tool_count():
    assert len(mcp._tool_manager._tools) == 12


@pytest.mark.parametrize(
    "tool",
    [
        "init_project",
        "generate_test",
        "generate_edge_cases",
        "generate_fault_tests",
        "repair_test",
        "heal_test",
        "feedback",
        "validate_scenario",
        "analyze_failure",
        "manage_memory",
        "get_cost_summary",
        "validate_prompt_change",
    ],
)
def test_all_tool_names_registered(tool):
    assert tool in mcp._tool_manager._tools.keys()
    assert mcp._tool_manager.get_tool(tool).is_async == True


@pytest.mark.parametrize(
    "tool_name, required, optional",
    [
        ("init_project", [], ["project_path"]),
        ("generate_test", ["scenario_path"], ["framework", "quality"]),
        ("generate_edge_cases", ["scenario_path"], ["framework", "quality"]),
        ("generate_fault_tests", ["scenario_path"], ["framework", "quality"]),
        ("repair_test", ["scenario_path", "test_code", "failure_output"], ["quality"]),
        ("heal_test", ["test_path", "failure_output"], []),
        ("feedback", ["file_path", "action"], ["reason"]),
        ("validate_scenario", ["scenario_path"], []),
        ("analyze_failure", ["log_content"], []),
        ("manage_memory", ["action"], ["query"]),
        ("get_cost_summary", [], ["period"]),
        ("validate_prompt_change", ["template_path"], []),
    ],
)
def test_tool_signature(tool_name, required, optional):
    tool = mcp._tool_manager.get_tool(tool_name)
    all_params = set(tool.parameters["properties"].keys())
    required_params = set(tool.parameters.get("required", []))
    assert required_params == set(required)
    assert all_params == set(required) | set(optional)


async def test_stub_tool_returns_dict():
    result = await init_project()
    assert isinstance(result, dict)


async def test_stub_tool_has_error_key():
    result = await init_project()
    assert isinstance(result["error"], str)


async def test_stub_tool_has_tool_key():
    result = await init_project()
    assert result["tool"] == "init_project"


def test_mcp_server_importable():
    import cognova.mcp_server as mod

    assert mod.mcp is not None
    assert mod.main is not None


def test_main_is_entry_point():
    import cognova.mcp_server as mod

    assert getattr(mod, "main") is main
