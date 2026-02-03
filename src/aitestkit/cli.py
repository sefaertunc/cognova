import json
import shutil
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import click

from aitestkit.config import (
    HAIKU_MODEL,
    OPUS_MODEL,
    SONNET_MODEL,
    get_settings,
    load_project_config,
)
from aitestkit.frameworks.registry import FrameworkCategory, format_framework_table, list_frameworks


def get_version() -> str:
    """Get package version from metadata."""
    try:
        return version("aitestkit")
    except PackageNotFoundError:
        return "dev"

def _create_project_structure(base_dir: Path) -> None:
    folders = [".aitestkit", ".aitestkit/feedback", ".aitestkit/history"]
    json_files = [".aitestkit/history/generations.json", ".aitestkit/feedback/pending.json",
             ".aitestkit/feedback/approved.json", ".aitestkit/feedback/rejected.json",
             ".aitestkit/feedback/patterns.json"]
    yaml_files = [ ".aitestkit/config.yaml"]
    for folder in folders:
        folder_path = base_dir / folder
        folder_path.mkdir(exist_ok=True ,parents=True)
    for file in json_files:
        file_path = base_dir / file
        file_path.touch()
        with open(file_path, 'w') as f:
            json.dump({}, f, indent=4)
    for file in yaml_files:
        file_path = base_dir / file
        file_path.touch()


@click.group()
def cli() -> None:
    """AITestKit - AI-Powered Multi-Framework Test Generation Toolkit."""
    pass


@cli.command()
def info() -> None:
    """Display current configuration and environment status."""
    click.echo(f"AITestKit v{get_version()}\n")

    click.echo("Environment:")

    try:
        settings = get_settings()
        api_status = "Configured"
    except Exception:
        settings = None
        api_status = "Not configured (set ANTHROPIC_API_KEY)"

    click.echo(f"  API Key:        {api_status}")
    click.echo(f"  Working Dir:    {Path.cwd()}")

    project_config = load_project_config()
    if project_config:
        click.echo("  Project Config: Found (.aitestkit/project.yaml)")
    else:
        click.echo("  Project Config: Not found")

    click.echo("\nModels:")
    if settings:
        click.echo(f"  Code Generation: {settings.model_code_gen}")
        click.echo(f"  Analysis:        {settings.model_analysis}")
        click.echo(f"  Regression:      {settings.model_regression}")
    else:
        click.echo(f"  Code Generation: {OPUS_MODEL} (default)")
        click.echo(f"  Analysis:        {SONNET_MODEL} (default)")
        click.echo(f"  Regression:      {HAIKU_MODEL} (default)")

    click.echo("\nSettings:")
    if settings:
        click.echo(f"  Default Framework: {settings.default_framework}")
        click.echo(f"  Output Directory:  {settings.output_dir}")
        click.echo(f"  Max Tokens:        {settings.max_tokens}")
        click.echo(f"  Temperature:       {settings.temperature}")
    else:
        click.echo("  (using defaults - API key not configured)")

    if project_config:
        click.echo("\nProject:")
        click.echo(f"  Name:       {project_config.product.name}")
        click.echo(f"  Type:       {project_config.product.type}")
        if project_config.product.tech_stack:
            click.echo(f"  Tech Stack: {', '.join(project_config.product.tech_stack)}")


@cli.command(
    epilog="""\b
Examples:
  aitestkit frameworks --list
  aitestkit frameworks --category e2e
  aitestkit frameworks --language Python
  aitestkit frameworks --priority 0
  aitestkit frameworks -c unit -l Python
"""
)
@click.option("--list", "list_all", is_flag=True, help="Display all frameworks in a table format.")
@click.option(
    "--category",
    "-c",
    type=click.Choice(
        ["unit", "bdd", "e2e", "performance", "security", "api", "mobile"], case_sensitive=False
    ),
    show_choices=False,
    metavar="CATEGORY",
    help="Filter by category (unit, bdd, e2e, performance, security, api, mobile).",
)
@click.option(
    "--language",
    "-l",
    type=str,
    help="Filter by language (e.g., Python, TypeScript, Java, JavaScript).",
)
@click.option(
    "--priority",
    "-p",
    type=int,
    help="Filter by priority: 0 (Core), 1 (Standard), 2 (Extended).",
)
def frameworks(
    list_all: bool, category: str | None, language: str | None, priority: int | None
) -> None:
    """List and filter supported testing frameworks."""
    if list_all:
        table = format_framework_table()
        click.echo(table)
    elif category and language and priority is not None:
        frameworks = list_frameworks(
            category=FrameworkCategory(category) if category else None,
            language=language,
            priority=priority,
        )
        if not frameworks:
            click.echo("No frameworks found with the specified filters.", err=True)
            raise SystemExit(2)
        click.echo("Filtered Frameworks:")
        for fw in frameworks:
            click.echo(f" - {fw.name}")
    elif category:
        try:
            category_enum = FrameworkCategory(category)
            frameworks = list_frameworks(category_enum)
            click.echo(f"Frameworks in category '{category}':")
            for fw in frameworks:
                click.echo(f" - {fw.name}")
        except ValueError:
            click.echo(f"Invalid category: {category}", err=True)
            raise click.Abort() from None
    elif language:
        frameworks = list_frameworks(language=language)
        if not frameworks:
            click.echo(f"No frameworks found for language: {language}", err=True)
            raise SystemExit(2)
        click.echo(f"Frameworks for language '{language}':")
        for fw in frameworks:
            click.echo(f" - {fw.name}")
    elif priority is not None:
        if priority < 0 or priority > 2:
            click.echo(f"Invalid priority level: {priority}. Must be between 0 and 2.", err=True)
            raise SystemExit(2)
        frameworks = list_frameworks(priority=priority)
        if not frameworks:
            click.echo(f"No frameworks found for priority level: {priority}", err=True)
            raise SystemExit(2)
        click.echo(f"Frameworks with priority level '{priority}':")
        for fw in frameworks:
            click.echo(f" - {fw.name}")

@cli.command(
    epilog="""\b
Examples:
    aitestkit init
    aitestkit init --force
    """
)
@click.option("--force", is_flag=True, help="Overwrite existing project directory.")
def init(force:bool) -> None:
    current_dir = Path.cwd()
    if not force:
        if (current_dir / ".aitestkit").is_dir():
            click.echo("The project already exists.")
            raise SystemExit(2)
        else:
            _create_project_structure(current_dir)
    else:
        shutil.rmtree(current_dir / ".aitestkit")
        _create_project_structure(current_dir)
    click.echo("AITestKit project initialized successfully.")



def main() -> None:
    """Entry point for the CLI."""
    cli()
