import logging
from pathlib import Path
from typing import Annotated

import typer

from booklet_generator._internal.core import generate_booklet

app = typer.Typer(
    rich_markup_mode=None,
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
)


@app.command()
def main_command(
    source: Annotated[
        Path,
        typer.Argument(
            help="Path to the source PDF.",
        ),
    ],
    output: Annotated[
        Path | None,
        typer.Option(
            "-o",
            "--output",
            "-d",
            "--destination",
            help="The directory to save the output PDF(s). Uses the source directory by default.",
        ),
    ],
    name: Annotated[
        str | None,
        typer.Option(
            "-n",
            "--name",
            help="The name of the output PDF(s). Uses the source file name by default.",
        ),
    ] = None,
) -> None:
    """Rearranges pages of a PDF into booklet order for double-sided A3 printing.

    Input pages are scaled to A4 and paired onto A3 spreads so the printed
    sheets can be folded and stapled into a booklet. A separate A4 PDF is
    produced for the middle sheet if the page count doesn't fit nicely on A3s.
    """
    generate_booklet(source, output, name)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app()


if __name__ == "__main__":
    main()
