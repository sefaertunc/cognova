"""Cognova MCP Server — IDE integration entry point.

Registers all MCP tools and starts the stdio transport.
Handles project initialization, version checking, and tool routing.

MCP Tools Registered:
    - init_project: Initialize .cognova/ in project root
    - generate_test: Main test generation pipeline
    - generate_edge_cases: Edge-case test generation (v1.1)
    - generate_fault_tests: Fault-guided test generation (v1.2, ACH)
    - repair_test: Context-aware test repair loop
    - heal_test: Self-healing for existing tests
    - feedback: Approve/reject/revoke generated tests
    - validate_scenario: Validate YAML scenario files
    - analyze_failure: AI-powered failure analysis
    - manage_memory: LanceDB maintenance (list/remove/rebuild/stats)
    - get_cost_summary: Per-operation cost reporting
    - validate_prompt_change: Prompt regression testing (Pipeline 7)

Distribution:
    uvx cognova-mcp@latest  (PyPI)

Installation (IDE config):
    {
      "mcpServers": {
        "Cognova": {
          "command": "uvx",
          "args": ["cognova-mcp@latest"],
          "env": { "ANTHROPIC_API_KEY": "sk-ant-..." }
        }
      }
    }
"""

from mcp.server.fastmcp import FastMCP

# Tool imports (one per module)
# from cognova.context.analyzer import analyze_project
# from cognova.generator.generator import generate
# etc.

mcp = FastMCP("Cognova")

# --- Tool registrations ---
# Each @mcp.tool() function delegates to the appropriate module.
# The tool description helps the IDE agent know when to call it.

# @mcp.tool()
# async def init_project(project_path: str) -> dict: ...

# @mcp.tool()
# async def generate_test(scenario_path: str, framework: str, quality: str = "standard") -> dict: ...

# ... (12 tools total, see MASTER_SPEC.md Section 8 for full specs)
