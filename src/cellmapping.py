from itertools import groupby
from typing import NamedTuple
from .cell import Cell


class CellPossibleValuePair(NamedTuple):
    cell: Cell
    possible_value: int


class CellMapping:
    def __init__(self, cells: list[Cell]) -> None:
        grouping = [
            CellPossibleValuePair(cell, possible_value)
            for cell in cells
            for possible_value in cell.possible_values
        ]
        self.__possible_value_lookup = {
            cell: set(item.possible_value for item in group)
            for cell, group in groupby(grouping, lambda c: c.cell)
        }
        self.__cell_lookup = {
            possible_value: set(item.cell for item in group)
            for possible_value, group in groupby(grouping, lambda c: c.possible_value)
        }
