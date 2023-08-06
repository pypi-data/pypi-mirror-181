"""Main function."""

import asyncio

import click

from .generate_image import generate_image


@click.command()
@click.argument(
    "source",
    nargs=1,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
def main(source: str):
    """Generate an image from SOURCE using LaTeX."""
    asyncio.run(generate_image(source))
