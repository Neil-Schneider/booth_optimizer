from __future__ import annotations

from typing import Iterable

from .grid import Cell, Grid

AISLE_WIDTH_CELLS = 4  # 8' wide aisles
MIN_SEGMENT_CELLS = 4
EXTENSION_LENGTH = 4


def _apply_vertical_aisle(grid: Grid, x: int) -> None:
    grid.fill_rect(x, 0, AISLE_WIDTH_CELLS, grid.height, Cell.AISLE)


def _apply_horizontal_aisle(grid: Grid, y: int) -> None:
    grid.fill_rect(0, y, grid.width, AISLE_WIDTH_CELLS, Cell.AISLE)


def _add_extensions(grid: Grid, xs: Iterable[int], ys: Iterable[int]) -> None:
    """Create 1x4 stubs from intersections to satisfy extension rule."""
    for x in xs:
        for y in ys:
            # Extend right
            if x + AISLE_WIDTH_CELLS < grid.width:
                grid.fill_rect(x + AISLE_WIDTH_CELLS, y, 1, EXTENSION_LENGTH, Cell.AISLE)
            # Extend downward
            if y + AISLE_WIDTH_CELLS < grid.height:
                grid.fill_rect(x, y + AISLE_WIDTH_CELLS, EXTENSION_LENGTH, 1, Cell.AISLE)


def generate_aisles(grid: Grid, booth_span: int = 5) -> Grid:
    """Populate the grid with aisle cells respecting width and length rules."""
    plan = grid.clone()

    # Perimeter aisles run horizontally so booths only need a single side against an aisle.
    _apply_horizontal_aisle(plan, 0)
    _apply_horizontal_aisle(plan, max(0, plan.height - AISLE_WIDTH_CELLS))

    horizontal_lines = []

    # Allow two booth depths between aisles so only one side of each booth borders an aisle.
    spacing = (booth_span * 2) + AISLE_WIDTH_CELLS

    y = spacing
    while y + AISLE_WIDTH_CELLS < plan.height - AISLE_WIDTH_CELLS:
        _apply_horizontal_aisle(plan, y)
        horizontal_lines.append(y)
        y += spacing

    # Add small stubs to satisfy 1x4 extensions where aisles meet (no-op without vertical aisles
    # but keeps compatibility if vertical aisles are introduced later).
    _add_extensions(plan, [], horizontal_lines)

    return plan


def is_valid_aisle(grid: Grid) -> bool:
    """Ensure all aisle stripes meet minimum size constraints."""

    for y in range(grid.height):
        for x in range(grid.width):
            if grid.cells[y][x] != Cell.AISLE:
                continue

            horizontal = 1
            cx = x - 1
            while cx >= 0 and grid.cells[y][cx] == Cell.AISLE:
                horizontal += 1
                cx -= 1
            cx = x + 1
            while cx < grid.width and grid.cells[y][cx] == Cell.AISLE:
                horizontal += 1
                cx += 1

            vertical = 1
            cy = y - 1
            while cy >= 0 and grid.cells[cy][x] == Cell.AISLE:
                vertical += 1
                cy -= 1
            cy = y + 1
            while cy < grid.height and grid.cells[cy][x] == Cell.AISLE:
                vertical += 1
                cy += 1

            if max(horizontal, vertical) < MIN_SEGMENT_CELLS:
                return False

    return True
