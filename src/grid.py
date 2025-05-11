from itertools import groupby
from typing import NamedTuple
from .cell import Cell
from .cellblock import CellBlock


class CellCage(NamedTuple):
    cells: list[tuple[int, int]]
    total: int


class CellConfig(NamedTuple):
    cells: list[list[int | None]]
    cages: list[CellCage]


class Grid:
    def __init__(self, cell_config: CellConfig) -> None:
        cells = [[Cell(value) for value in row] for row in cell_config.cells]

        self.__cells = [cell for row in cells for cell in row]
        self.__blocks = [
            CellBlock(block, 45)
            for block in get_rows(cells) + get_columns(cells) + get_squares(cells)
        ] + [
            CellBlock(cells, total)
            for cells, total in get_cages(cells, cell_config.cages)
        ]

    def is_solved(self) -> bool:
        # Doesn't account for incorrect values
        return all(cell.value is not None for cell in self.__cells)

    def guess(self) -> bool:
        for block in self.__blocks:
            if block.update():
                return True

        return False


def get_rows(cells: list[list[Cell]]) -> list[list[Cell]]:
    return cells


def get_columns(cells: list[list[Cell]]) -> list[list[Cell]]:
    return [cells[:][j] for j in range(9)]


def get_squares(cells: list[list[Cell]]) -> list[list[Cell]]:
    # TEFW TODO - implement this function
    return [cells[:][j] for j in range(9)]


def get_cages(
    cells: list[list[Cell]], cages: list[CellCage]
) -> list[tuple[list[Cell], int]]:
    return [([cells[i][j] for i, j in cage.cells], cage.total) for cage in cages]
