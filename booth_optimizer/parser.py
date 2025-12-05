from __future__ import annotations

from typing import Tuple

from .grid import Grid

CELL_FEET = 2


def parse_building_shape(shape: str) -> Tuple[int, int]:
    """Parse a shape string like "100x80" (feet) into cell dimensions."""
    if "x" not in shape:
        raise ValueError("Shape must be in the form WIDTHxHEIGHT (feet)")
    width_part, height_part = shape.lower().split("x", 1)
    width_ft = int(width_part)
    height_ft = int(height_part)
    width_cells = max(1, width_ft // CELL_FEET)
    height_cells = max(1, height_ft // CELL_FEET)
    return width_cells, height_cells


def build_grid(shape: str) -> Grid:
    width_cells, height_cells = parse_building_shape(shape)
    return Grid(width_cells, height_cells)
