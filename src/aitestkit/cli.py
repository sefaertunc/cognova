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


@cli.command()
@click.option("--list", "list_all", is_flag=True, help="List all supported frameworks.")
@click.option(
    "--category",
    "-c",
    type=click.Choice(
        ["unit", "bdd", "e2e", "performance", "security", "api", "mobile"], case_sensitive=False
    ),
    help="Filter frameworks by category.",
)
def frameworks(list_all: bool, category: str | None) -> None:
    """Manage supported testing frameworks."""
    if list_all:
        table = format_framework_table()
        click.echo(table)
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
