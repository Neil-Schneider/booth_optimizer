from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List, Tuple


class Cell(Enum):
    EMPTY = "."
    AISLE = "A"
    BOOTH = "B"


@dataclass
class Grid:
    """A simple 2'x2' cell grid representation."""

    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Grid dimensions must be positive")
        self.cells: List[List[Cell]] = [
            [Cell.EMPTY for _ in range(self.width)] for _ in range(self.height)
        ]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def fill_rect(self, x: int, y: int, w: int, h: int, value: Cell) -> None:
        for row in range(y, y + h):
            for col in range(x, x + w):
                if not self.in_bounds(col, row):
                    raise ValueError("Rectangle exceeds grid bounds")
                self.cells[row][col] = value

    def area_is(self, x: int, y: int, w: int, h: int, allowed: Iterable[Cell]) -> bool:
        allowed_set = set(allowed)
        for row in range(y, y + h):
            for col in range(x, x + w):
                if not self.in_bounds(col, row) or self.cells[row][col] not in allowed_set:
                    return False
        return True

    def count_adjacent(self, x: int, y: int, w: int, h: int, target: Cell) -> int:
        """Count target cells that touch the rectangle on its perimeter."""
        count = 0
        # Top and bottom edges
        for col in range(max(0, x - 1), min(self.width, x + w + 1)):
            if y - 1 >= 0 and self.cells[y - 1][col] == target:
                count += 1
            if y + h < self.height and self.cells[y + h][col] == target:
                count += 1
        # Left and right edges
        for row in range(y, y + h):
            if x - 1 >= 0 and self.cells[row][x - 1] == target:
                count += 1
            if x + w < self.width and self.cells[row][x + w] == target:
                count += 1
        return count

    def as_lines(self) -> List[str]:
        return ["".join(cell.value for cell in row) for row in self.cells]

    def render(self) -> str:
        return "\n".join(self.as_lines())

    def clone(self) -> "Grid":
        new_grid = Grid(self.width, self.height)
        new_grid.cells = [row.copy() for row in self.cells]
        return new_grid

    def booth_positions(self) -> List[Tuple[int, int]]:
        positions: List[Tuple[int, int]] = []
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if cell == Cell.BOOTH:
                    positions.append((x, y))
        return positions
