import logging
from pathlib import Path
from typing import Annotated

import typer

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
    ] = None,
) -> None:
    raise NotImplementedError


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app()


if __name__ == "__main__":
    main()
