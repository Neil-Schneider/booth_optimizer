from __future__ import annotations

import argparse

from .optimizer import layout_as_text, optimize_layout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Optimize booth layouts")
    parser.add_argument(
        "--shape",
        required=True,
        help="Building shape in feet, WIDTHxHEIGHT (e.g. 120x80)",
    )
    parser.add_argument(
        "--show-grid",
        action="store_true",
        help="Print the resulting layout grid",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    layout = optimize_layout(args.shape)
    print(f"Booth count: {layout.booth_count}")
    if args.show_grid:
        print(layout_as_text(layout))


if __name__ == "__main__":
    main()
