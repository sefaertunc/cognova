"""
Framework registry for multi-framework test generation support.

This module defines all supported testing frameworks with their metadata,
enabling dynamic framework selection and validation in the CLI and generator.

Supported Categories:
- Unit Testing: pytest, jest, junit, nunit
- E2E Testing: playwright (py/ts), cypress, selenium
- BDD Testing: pytest-bdd, cucumber (java/js)
- Performance Testing: locust, k6, jmeter, gatling
- Security Testing: nuclei, owasp-zap
- API Testing: httpx, postman

Example Usage:
    from cognova.frameworks.registry import get_framework, list_frameworks

    # Get specific framework
    fw = get_framework("pytest")
    print(fw.extension)  # ".py"

    # List all performance frameworks
    perf_frameworks = list_frameworks(category=FrameworkCategory.PERFORMANCE)
"""

from dataclasses import dataclass
from enum import Enum


class FrameworkCategory(str, Enum):
    """Testing framework categories."""

    UNIT = "unit"
    API = "api"
    E2E = "e2e"
    BDD = "bdd"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MOBILE = "mobile"


@dataclass(frozen=True)
class FrameworkInfo:
    """
    Framework metadata for test generation.

    Attributes:
        name: Display name of the framework
        category: Testing category (unit, e2e, performance, etc.)
        language: Primary programming language
        extension: Output file extension
        prompt_template: Path to prompt template (relative to prompts/templates/code-generation/)
        description: Human-readable description
        priority: Implementation priority (0=core, 1=important, 2=nice-to-have)
        multi_file: Whether framework generates multiple files (e.g., BDD feature + steps)
        secondary_extension: Extension for secondary file (if multi_file=True)
    """

    name: str
    category: FrameworkCategory
    language: str
    extension: str
    prompt_template: str
    description: str
    priority: int = 0
    multi_file: bool = False
    secondary_extension: str | None = None


# =============================================================================
# FRAMEWORK DEFINITIONS
# =============================================================================

FRAMEWORKS: dict[str, FrameworkInfo] = {
    # -------------------------------------------------------------------------
    # UNIT TESTING
    # -------------------------------------------------------------------------
    "pytest": FrameworkInfo(
        name="pytest",
        category=FrameworkCategory.UNIT,
        language="Python",
        extension=".py",
        prompt_template="unit/pytest.md",
        description="Python unit and integration testing framework",
        priority=0,
    ),
    "jest": FrameworkInfo(
        name="Jest",
        category=FrameworkCategory.UNIT,
        language="TypeScript",
        extension=".test.ts",
        prompt_template="unit/jest.md",
        description="JavaScript/TypeScript testing framework",
        priority=0,
    ),
    "junit": FrameworkInfo(
        name="JUnit 5",
        category=FrameworkCategory.UNIT,
        language="Java",
        extension=".java",
        prompt_template="unit/junit.md",
        description="Java unit testing framework",
        priority=1,
    ),
    "nunit": FrameworkInfo(
        name="NUnit",
        category=FrameworkCategory.UNIT,
        language="C#",
        extension=".cs",
        prompt_template="unit/nunit.md",
        description=".NET unit testing framework",
        priority=2,
    ),
    # -------------------------------------------------------------------------
    # E2E / WEB TESTING
    # -------------------------------------------------------------------------
    "playwright-py": FrameworkInfo(
        name="Playwright",
        category=FrameworkCategory.E2E,
        language="Python",
        extension=".py",
        prompt_template="e2e/playwright_python.md",
        description="Cross-browser E2E testing (Python)",
        priority=0,
    ),
    "playwright-ts": FrameworkInfo(
        name="Playwright",
        category=FrameworkCategory.E2E,
        language="TypeScript",
        extension=".spec.ts",
        prompt_template="e2e/playwright_typescript.md",
        description="Cross-browser E2E testing (TypeScript)",
        priority=0,
    ),
    "cypress": FrameworkInfo(
        name="Cypress",
        category=FrameworkCategory.E2E,
        language="JavaScript",
        extension=".cy.js",
        prompt_template="e2e/cypress.md",
        description="JavaScript E2E testing framework",
        priority=1,
    ),
    "selenium-py": FrameworkInfo(
        name="Selenium",
        category=FrameworkCategory.E2E,
        language="Python",
        extension=".py",
        prompt_template="e2e/selenium_python.md",
        description="Browser automation (Python)",
        priority=2,
    ),
    # -------------------------------------------------------------------------
    # BDD / ACCEPTANCE TESTING
    # -------------------------------------------------------------------------
    "pytest-bdd": FrameworkInfo(
        name="pytest-bdd",
        category=FrameworkCategory.BDD,
        language="Python",
        extension=".feature",
        prompt_template="bdd/pytest_bdd.md",
        description="BDD with Gherkin syntax (Python)",
        priority=0,
        multi_file=True,
        secondary_extension="_steps.py",
    ),
    "cucumber-java": FrameworkInfo(
        name="Cucumber",
        category=FrameworkCategory.BDD,
        language="Java",
        extension=".feature",
        prompt_template="bdd/cucumber_java.md",
        description="BDD with Gherkin syntax (Java)",
        priority=0,
        multi_file=True,
        secondary_extension="Steps.java",
    ),
    "cucumber-js": FrameworkInfo(
        name="Cucumber",
        category=FrameworkCategory.BDD,
        language="JavaScript",
        extension=".feature",
        prompt_template="bdd/cucumber_js.md",
        description="BDD with Gherkin syntax (JavaScript)",
        priority=1,
        multi_file=True,
        secondary_extension=".steps.js",
    ),
    "behave": FrameworkInfo(
        name="Behave",
        category=FrameworkCategory.BDD,
        language="Python",
        extension=".feature",
        prompt_template="bdd/behave.md",
        description="BDD framework for Python",
        priority=2,
        multi_file=True,
        secondary_extension="_steps.py",
    ),
    "robot": FrameworkInfo(
        name="Robot Framework",
        category=FrameworkCategory.BDD,
        language="Python",
        extension=".robot",
        prompt_template="bdd/robot.md",
        description="Keyword-driven test automation framework",
        priority=0,
    ),
    # -------------------------------------------------------------------------
    # PERFORMANCE TESTING
    # -------------------------------------------------------------------------
    "locust": FrameworkInfo(
        name="Locust",
        category=FrameworkCategory.PERFORMANCE,
        language="Python",
        extension=".py",
        prompt_template="performance/locust.md",
        description="Python load testing framework",
        priority=0,
    ),
    "k6": FrameworkInfo(
        name="k6",
        category=FrameworkCategory.PERFORMANCE,
        language="JavaScript",
        extension=".js",
        prompt_template="performance/k6.md",
        description="Modern load testing tool",
        priority=0,
    ),
    "jmeter": FrameworkInfo(
        name="JMeter",
        category=FrameworkCategory.PERFORMANCE,
        language="XML",
        extension=".jmx",
        prompt_template="performance/jmeter.md",
        description="Enterprise performance testing tool",
        priority=1,
    ),
    "gatling": FrameworkInfo(
        name="Gatling",
        category=FrameworkCategory.PERFORMANCE,
        language="Scala",
        extension=".scala",
        prompt_template="performance/gatling.md",
        description="High-performance load testing",
        priority=2,
    ),
    "artillery": FrameworkInfo(
        name="Artillery",
        category=FrameworkCategory.PERFORMANCE,
        language="YAML",
        extension=".yml",
        prompt_template="performance/artillery.md",
        description="Cloud-scale load testing",
        priority=2,
    ),
    # -------------------------------------------------------------------------
    # SECURITY TESTING
    # -------------------------------------------------------------------------
    "nuclei": FrameworkInfo(
        name="Nuclei",
        category=FrameworkCategory.SECURITY,
        language="YAML",
        extension=".yaml",
        prompt_template="security/nuclei.md",
        description="Template-based vulnerability scanner",
        priority=0,
    ),
    "zap": FrameworkInfo(
        name="OWASP ZAP",
        category=FrameworkCategory.SECURITY,
        language="Python",
        extension=".py",
        prompt_template="security/zap.md",
        description="Web application security scanner",
        priority=1,
    ),
    "bandit": FrameworkInfo(
        name="Bandit",
        category=FrameworkCategory.SECURITY,
        language="Python",
        extension=".py",
        prompt_template="security/bandit.md",
        description="Python security linter",
        priority=2,
    ),
    # -------------------------------------------------------------------------
    # API TESTING
    # -------------------------------------------------------------------------
    "httpx": FrameworkInfo(
        name="pytest + httpx",
        category=FrameworkCategory.API,
        language="Python",
        extension=".py",
        prompt_template="api/httpx.md",
        description="Python API testing with httpx",
        priority=0,
    ),
    "postman": FrameworkInfo(
        name="Postman/Newman",
        category=FrameworkCategory.API,
        language="JSON",
        extension=".postman_collection.json",
        prompt_template="api/postman.md",
        description="API collection testing",
        priority=1,
    ),
    "rest-assured": FrameworkInfo(
        name="REST Assured",
        category=FrameworkCategory.API,
        language="Java",
        extension=".java",
        prompt_template="api/rest_assured.md",
        description="Java REST API testing",
        priority=2,
    ),
    "supertest": FrameworkInfo(
        name="Supertest",
        category=FrameworkCategory.API,
        language="JavaScript",
        extension=".test.js",
        prompt_template="api/supertest.md",
        description="Node.js API testing",
        priority=2,
    ),
}


# =============================================================================
# REGISTRY FUNCTIONS
# =============================================================================


def get_framework(name: str) -> FrameworkInfo:
    """
    Get framework information by name.

    Args:
        name: Framework identifier (e.g., "pytest", "playwright-py")

    Returns:
        FrameworkInfo dataclass with framework metadata

    Raises:
        ValueError: If framework name is not found

    Example:
        >>> fw = get_framework("pytest")
        >>> fw.language
        'Python'
    """
    if name not in FRAMEWORKS:
        available = ", ".join(sorted(FRAMEWORKS.keys()))
        raise ValueError(
            f"Unknown framework: '{name}'. " f"Available frameworks: {available}"
        )
    return FRAMEWORKS[name]


def list_frameworks(
    category: FrameworkCategory | None = None,
    language: str | None = None,
    priority: int | None = None,
) -> list[FrameworkInfo]:
    """
    List frameworks with optional filtering.

    Args:
        category: Filter by testing category
        language: Filter by programming language
        priority: Filter by implementation priority (0, 1, or 2)

    Returns:
        List of matching FrameworkInfo objects, sorted by priority then name

    Example:
        >>> perf = list_frameworks(category=FrameworkCategory.PERFORMANCE)
        >>> [fw.name for fw in perf]
        ['Locust', 'k6', 'JMeter', 'Gatling', 'Artillery']
    """
    frameworks = list(FRAMEWORKS.values())

    if category is not None:
        frameworks = [f for f in frameworks if f.category == category]

    if language is not None:
        frameworks = [f for f in frameworks if f.language.lower() == language.lower()]

    if priority is not None:
        frameworks = [f for f in frameworks if f.priority == priority]

    return sorted(frameworks, key=lambda f: (f.priority, f.name))


def get_framework_choices() -> list[str]:
    """
    Get list of all framework identifiers for CLI choices.

    Returns:
        Sorted list of framework names

    Example:
        >>> choices = get_framework_choices()
        >>> "pytest" in choices
        True
    """
    return sorted(FRAMEWORKS.keys())


def get_frameworks_by_category() -> dict[FrameworkCategory, list[FrameworkInfo]]:
    """
    Get all frameworks organized by category.

    Returns:
        Dictionary mapping categories to framework lists

    Example:
        >>> by_cat = get_frameworks_by_category()
        >>> len(by_cat[FrameworkCategory.UNIT])
        4
    """
    result: dict[FrameworkCategory, list[FrameworkInfo]] = {cat: [] for cat in FrameworkCategory}

    for framework in FRAMEWORKS.values():
        result[framework.category].append(framework)

    # Sort each category by priority then name
    for cat in result:
        result[cat] = sorted(result[cat], key=lambda f: (f.priority, f.name))

    return result


def get_core_frameworks() -> list[FrameworkInfo]:
    """
    Get priority 0 (core) frameworks that should be implemented first.

    Returns:
        List of core frameworks sorted by name
    """
    return list_frameworks(priority=0)


def validate_framework(name: str) -> bool:
    """
    Check if a framework name is valid.

    Args:
        name: Framework identifier to validate

    Returns:
        True if valid, False otherwise
    """
    return name in FRAMEWORKS


# =============================================================================
# CLI HELPER
# =============================================================================


def format_framework_table() -> str:
    """
    Format all frameworks as a table for CLI display.

    Returns:
        Formatted string table of all frameworks
    """
    lines = [
        "Supported Frameworks:",
        "-" * 80,
        f"{'Framework':<15} {'Category':<12} {'Language':<12} {'Extension':<20} {'Priority'}",
        "-" * 80,
    ]

    for name, fw in sorted(FRAMEWORKS.items(), key=lambda x: (x[1].priority, x[0])):
        priority_label = {0: "Core", 1: "Standard", 2: "Extended"}.get(fw.priority, "?")
        lines.append(
            f"{name:<15} {fw.category.value:<12} {fw.language:<12} {fw.extension:<20} {priority_label}"
        )

    lines.append("-" * 80)
    lines.append(f"Total: {len(FRAMEWORKS)} frameworks")

    return "\n".join(lines)
