from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from pypdf import PageObject, PdfReader, PdfWriter

logger = logging.getLogger(__name__)

# PDF points: 1pt = 1/72 inch
# A4 portrait: 210mm * 297mm = 595.276pt * 841.890pt
A4_WIDTH_PT = 595.276
A4_HEIGHT_PT = 841.890
# A3 landscape: 420mm × 297mm  = 1190.551pt × 841.890pt
A3_WIDTH_PT = A4_WIDTH_PT * 2
A3_HEIGHT_PT = A4_HEIGHT_PT


def generate_booklet(
    source: Path, destination: Path | None, output_name: str | None
) -> None:
    source = source.expanduser()

    logger.debug(f"Processing PDF at {source}")

    if not source.is_file():
        raise FileNotFoundError(f"Expected `source` ({source}) to be a file")

    if destination is not None:
        destination = destination.expanduser()
        if not destination.is_dir():
            raise NotADirectoryError(
                f"Expected `destination` ({destination}) to be a directory"
            )
    else:
        destination = source.parent

    if output_name is None:
        output_name = source.stem

    reader = PdfReader(source)
    pages = [scale_to_a4(p) for p in reader.pages]

    parts = partition(pages)

    if parts.a4 is not None:
        writer = PdfWriter()
        writer.add_page(parts.a4.left)
        writer.add_page(parts.a4.right)
        full_dest = destination / f"{output_name}-a4.pdf"
        logger.info(f"Writing a4 middle page to {full_dest}")
        writer.write(full_dest)

    writer = PdfWriter()
    for page_parts in parts.a3:
        writer.add_page(merge_page_group(page_parts))

    full_dest = destination / f"{output_name}-a3.pdf"
    if len(parts.a3) == 0:
        logger.info(f"Writing a3 booklet to {full_dest}")
        writer.write(full_dest)
    else:
        logger.debug("Skipping empty a3 part")


def scale_to_a4(page: PageObject) -> PageObject:
    page.scale_to(A4_WIDTH_PT, A4_HEIGHT_PT)
    return page


def blank(width_pt: float, height_pt: float) -> PageObject:
    writer = PdfWriter()
    return writer.add_blank_page(width_pt, height_pt)


def blank_landscape_a3() -> PageObject:
    return blank(A3_WIDTH_PT, A3_HEIGHT_PT)


def blank_portrait_a4() -> PageObject:
    return blank(A4_WIDTH_PT, A4_HEIGHT_PT)


def multiple_of_4_booklet[T](pages: list[T]) -> list[Group[T]]:
    length = len(pages)
    assert length % 4 == 0

    midpoint = length // 2

    groups = []

    for front_index in range(midpoint):
        back_index = -(front_index + 1)

        if front_index % 2 == 0:
            left = pages[back_index]
            right = pages[front_index]
        else:
            left = pages[front_index]
            right = pages[back_index]

        groups.append(Group(left, right))

    return groups


@dataclass(slots=True)
class Group[T]:
    left: T
    right: T


class PageGroup(Group[PageObject]):
    """A group of two A4 pages."""


def merge_page_group(group: PageGroup) -> PageObject:
    """Merge the two A4 pages into an A3 page on the shared long edge."""

    a3 = blank_landscape_a3()
    a3.merge_translated_page(group.left, 0, 0)
    a3.merge_translated_page(group.right, A4_WIDTH_PT, 0)

    return a3


@dataclass(slots=True)
class Partitioned_[G]:
    a4: G | None
    a3: list[G]


class Partitioned(Partitioned_[PageGroup]):
    """Represents partitioned pages. See `partition` for details."""


def partition(pages: list[PageObject]) -> Partitioned:
    """Partition the pages into a booklet structure.

    A double sided a4 "middle page" will be extracted if the booklet requires
    more than a single blank page of padding.

    All other pages are grouped into A3 booklet pages which are meant to be
    flipped on the short edge when printing.

    Raises:
        ValueError: If the input list is empty.
    """
    return partition_(pages, blank_portrait_a4)


def partition_[T](pages: list[T], create_blank: Callable[[], T]) -> Partitioned[T]:
    length = len(pages)

    if length == 0:
        raise ValueError("Cannot partition an empty list of pages")

    if length == 1:
        return Partitioned_(Group(pages[0], create_blank()), [])

    if length == 2:
        return Partitioned_(Group(pages[0], pages[1]), [])

    # We have now covered the cases where A3 pages cannot be generated.

    # The length of a valid booklet must be a multiple of 4.
    if length % 4 == 0:
        return Partitioned_(None, multiple_of_4_booklet(pages))

    if length % 4 == 3:
        return Partitioned_(None, multiple_of_4_booklet([*pages, create_blank()]))

    if length % 4 == 2:
        midpoint = length // 2
        return Partitioned_(
            Group(
                pages[midpoint - 1],
                pages[midpoint],
            ),
            multiple_of_4_booklet(
                [
                    *pages[: midpoint - 1],
                    *pages[midpoint + 1 :],
                ],
            ),
        )

    assert length % 4 == 1
    midpoint = length // 2 + 1
    return Partitioned_(
        Group(
            pages[midpoint - 1],
            pages[midpoint],
        ),
        multiple_of_4_booklet(
            [
                *pages[: midpoint - 1],
                *pages[midpoint + 1 :],
                create_blank(),
            ],
        ),
    )
