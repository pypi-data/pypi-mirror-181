"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """G Node Factory."""


if __name__ == "__main__":
    main(prog_name="g-node-factory")  # pragma: no cover
