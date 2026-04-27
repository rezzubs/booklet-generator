from booklet_generator._internal.core import Group, Partitioned_, partition_


def for_length(length: int, expected: Partitioned_[Group[int | None]]) -> None:
    pages: list[int | None] = list(range(1, length + 1))
    result = partition_(pages, lambda: None)
    assert result == expected


def test_page_order():
    for_length(0, Partitioned_(None, []))
    for_length(1, Partitioned_(Group(1, None), []))
    for_length(2, Partitioned_(Group(1, 2), []))
    for_length(3, Partitioned_(None, [Group(None, 1), Group(2, 3)]))
    for_length(4, Partitioned_(None, [Group(4, 1), Group(2, 3)]))
    for_length(5, Partitioned_(Group(3, 4), [Group(None, 1), Group(2, 5)]))
    for_length(6, Partitioned_(Group(3, 4), [Group(6, 1), Group(2, 5)]))
    for_length(
        7, Partitioned_(None, [Group(None, 1), Group(2, 7), Group(6, 3), Group(4, 5)])
    )
    for_length(
        8, Partitioned_(None, [Group(8, 1), Group(2, 7), Group(6, 3), Group(4, 5)])
    )
    for_length(
        9,
        Partitioned_(
            Group(5, 6), [Group(None, 1), Group(2, 9), Group(8, 3), Group(4, 7)]
        ),
    )
    for_length(
        10,
        Partitioned_(
            Group(5, 6), [Group(10, 1), Group(2, 9), Group(8, 3), Group(4, 7)]
        ),
    )
