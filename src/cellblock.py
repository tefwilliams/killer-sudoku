import itertools
from .cell import Cell


class CellBlock:
    def __init__(self, cells: list[Cell], total: int) -> None:
        self.__cells = cells
        self.__total = total

    def __values(self) -> set[int]:
        return set(cell.value for cell in self.__cells if cell.value is not None)

    def __remaining_cells(self) -> list[Cell]:
        return [cell for cell in self.__cells if cell.value is None]

    def update(self) -> bool:
        disallowed_values = self.__values()
        remaining_cells = self.__remaining_cells()

        # Group cells by their possible values
        # (ordered by length of possible values)
        # go through each group
        # if the number of cells in the group is equal to the number of possible values
        # then remove the possible values from the other cells in the block
        # if the number of cells is greater than the number of possible values throw an error
        # if the number of cells is less than the number of possible values
        # then see if the possible values is a subset of

        changed = False
        for cell in remaining_cells:
            cell.possible_values.discard(*disallowed_values)

            if len(cell.possible_values) == 1:
                cell.value = cell.possible_values.pop()
                changed = True

        return changed

    def find_naked_subsets(self, max_subset_size=4):
        changed = False
        for size in range(2, max_subset_size + 1):
            for cells in itertools.combinations(self.__cells, size):
                # Combine the values from these cells
                possible_values = set(
                    value for cell in cells for value in cell.possible_values
                )

                if len(possible_values) == size:
                    other_cells = set(self.__cells) - set(cells)

                    # This is a naked subset
                    for other_cell in other_cells:
                        before = other_cell.possible_values.copy()
                        other_cell.possible_values.discard(*possible_values)

                        if other_cell.possible_values != before:
                            changed = True
        return changed


def find_combinations_recursive(
    cells: list[Cell], total: int
) -> list[list[tuple[Cell, int]]]:
    if len(cells) == 1:
        cell = cells[0]

        if total in cell.possible_values:
            return [[(cell, total)]]

        return []

    first_cell, *rest_cells = cells

    return [
        [(first_cell, value)] + combination
        for value in first_cell.possible_values
        for combination in find_combinations_recursive(rest_cells, total - value)
        if value < total
    ]
