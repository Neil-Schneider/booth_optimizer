# booth_optimizer

A Python package that models a building as a 2'x2' cell grid, builds aisles, and places 10'x10' booths (5x5 cells). It returns a layout that maximizes booth count while satisfying access constraints.

## Features
- Parse building shapes in feet (e.g., `120x80`) into a grid of 2'x2' cells.
- Generate aisle stripes that are always 8' (4-cell) wide with 4x4 minimum footprints and 1x4 extensions.
- Place 5x5 cell booths that each touch at least five aisle cells.
- Greedy optimization that tests staggered offsets to maximize booth count.
- CLI entry point: `python -m booth_optimizer --shape 120x80 --show-grid`.

## Installation
The package is self contained; you can run it directly from the repository with Python 3.11+.

## Usage
Optimize a layout for a 120'x80' rectangular hall and print the grid:

```bash
python -m booth_optimizer --shape 120x80 --show-grid
```

Example output for a more compact 40'x40' hall:

```
Booth count: 1
AAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAA
AAAABBBBBAAAA...AAAA
AAAABBBBBAAAA...AAAA
AAAABBBBBAAAA...AAAA
AAAABBBBBAAAA...AAAA
AAAABBBBBAAAA...AAAA
AAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAA
AAAA.....AAAA...AAAA
AAAA.....AAAA...AAAA
AAAA.....AAAA...AAAA
AAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAA
```

Each character represents a 2'x2' cell (`A` = aisle, `B` = booth, `.` = empty). The optimizer ensures aisles are at least 8' wide and every booth has sufficient aisle access.

## Library API
You can also import the package to embed the optimizer:

```python
from booth_optimizer import optimize_layout, layout_as_text

layout = optimize_layout("120x80")
print(layout.booth_count)
print(layout_as_text(layout))
```

## Notes
- Shapes use feet and are automatically converted to cells with 2' resolution.
- Aisle generation uses evenly spaced cross-aisles and short extensions at intersections to satisfy the minimum 4x4 area rule.
- The greedy booth placer attempts two offsets to find a denser packing while respecting aisle adjacency.
