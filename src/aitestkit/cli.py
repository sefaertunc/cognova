import click

from aitestkit.frameworks.registry import FrameworkCategory, format_framework_table, list_frameworks


@click.group()
def cli() -> None:
    """AITestKit - AI-Powered Multi-Framework Test Generation Toolkit."""
    pass


@cli.command()
def info() -> None:
    """Display current configuration settings."""
    click.echo("Current configuration settings:")
    click.echo(" - Model for Code Generation: claude-opus-4-5-20251101")
    click.echo(" - Model for Analysis: claude-sonnet-4-5-20250929")
    click.echo(" - Model for Regression: claude-haiku-4-5-20251001")


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
