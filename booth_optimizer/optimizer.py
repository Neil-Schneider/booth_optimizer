from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .aisles import generate_aisles, is_valid_aisle
from .booths import place_booths_greedily
from .grid import Cell, Grid
from .parser import build_grid


@dataclass
class LayoutResult:
    grid: Grid
    booth_count: int

    def render(self) -> str:
        return self.grid.render()


def optimize_layout(shape: str) -> LayoutResult:
    base_grid = build_grid(shape)
    aisle_grid = generate_aisles(base_grid)
    if not is_valid_aisle(aisle_grid):
        raise ValueError("Generated aisles do not meet minimum segment requirements")
    booth_grid = place_booths_greedily(aisle_grid)
    booth_cells = sum(cell == Cell.BOOTH for row in booth_grid.cells for cell in row)
    booth_count = booth_cells // 25
    return LayoutResult(grid=booth_grid, booth_count=booth_count)


def layout_as_text(layout: LayoutResult) -> str:
    return layout.render()
