import pytest
from src import Cell, CellBlock


def generate_block(
    config: list[tuple[int | None, list[int] | None]], total=0
) -> CellBlock:
    cells = []

    for value, possible_values in config:
        cell = Cell(value)
        if possible_values is not None:
            cell.possible_values = set(possible_values)
        cells.append(cell)

    return CellBlock(cells, total)


@pytest.mark.parametrize(
    "block",
    [
        generate_block(
            [
                (None, [1, 2]),
                (None, [2, 3]),
                (None, [1, 3]),
                (None, [3, 4, 5]),
                (None, [3, 4, 5]),
            ]
        )
    ],
)
def test_find_naked_subsets__removes_expected_values(block: CellBlock) -> None:
    block.find_naked_subsets()

    cells = block.cells()

    assert [cell.possible_values for cell in cells] == [
        {1, 2},
        {2, 3},
        {1, 3},
        {4, 5},
        {4, 5},
    ]
