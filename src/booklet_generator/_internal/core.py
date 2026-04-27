import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def generate_booklet(
    source: Path, destination: Path | None, output_name: str | None
) -> None:
    source = source.expanduser()

    if source.is_file():
        raise FileNotFoundError(f"Expected `source` ({source}) to be a file")

    if destination is not None:
        destination = destination.expanduser()
        if not destination.is_dir():
            raise NotADirectoryError(
                f"Expected `destination` ({destination}) to be a directory"
            )

    if output_name is None:
        output_name = source.stem
