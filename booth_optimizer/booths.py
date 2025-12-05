from __future__ import annotations

from typing import Iterable, List, Tuple

from .grid import Cell, Grid

BOOTH_SIZE = 5  # 5x5 cells
REQUIRED_AISLE_TOUCH_POINTS = 5


class BoothPlanner:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def find_candidates(self) -> Iterable[Tuple[int, int]]:
        for y in range(self.grid.height - BOOTH_SIZE + 1):
            for x in range(self.grid.width - BOOTH_SIZE + 1):
                yield x, y

    def fits(self, x: int, y: int) -> bool:
        if not self.grid.area_is(x, y, BOOTH_SIZE, BOOTH_SIZE, {Cell.EMPTY}):
            return False
        adjacency = self.grid.count_adjacent(x, y, BOOTH_SIZE, BOOTH_SIZE, Cell.AISLE)
        return adjacency >= REQUIRED_AISLE_TOUCH_POINTS

    def place(self, x: int, y: int) -> None:
        self.grid.fill_rect(x, y, BOOTH_SIZE, BOOTH_SIZE, Cell.BOOTH)


def validate_booth(grid: Grid, x: int, y: int) -> bool:
    planner = BoothPlanner(grid)
    return planner.fits(x, y)


def count_booths(grid: Grid) -> int:
    return sum(cell == Cell.BOOTH for row in grid.cells for cell in row) // (BOOTH_SIZE * BOOTH_SIZE)


def place_booths_greedily(grid: Grid) -> Grid:
    plan = grid.clone()
    planner = BoothPlanner(plan)

    # Try multiple offsets to reduce alignment artifacts.
    best_plan: Grid | None = None
    best_count = -1

    offsets: List[Tuple[int, int]] = [(0, 0), (BOOTH_SIZE // 2, BOOTH_SIZE // 2)]

    for ox, oy in offsets:
        attempt = plan.clone()
        planner = BoothPlanner(attempt)
        for y in range(oy, attempt.height - BOOTH_SIZE + 1):
            for x in range(ox, attempt.width - BOOTH_SIZE + 1):
                if planner.fits(x, y):
                    planner.place(x, y)
        booth_cells = sum(cell == Cell.BOOTH for row in attempt.cells for cell in row)
        booth_count = booth_cells // (BOOTH_SIZE * BOOTH_SIZE)
        if booth_count > best_count:
            best_count = booth_count
            best_plan = attempt

    return best_plan if best_plan is not None else plan
