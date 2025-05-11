class Cell:
    def __init__(self, value: int | None) -> None:
        self.possible_values: set[int] = set() if value is None else set(range(1, 10))
        self.value = value
