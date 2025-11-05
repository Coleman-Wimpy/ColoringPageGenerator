"""Small CLI wrapper to convert an image into a coloring-page outline.

Usage:
    python scripts/convert_image.py input.jpg output.png --blur 5 --th1 50 --th2 150
"""
from pathlib import Path
import argparse
import sys
from pathlib import Path as _Path


# If the package isn't installed, allow running this script directly from the repo
# by adding the repository `src/` directory to sys.path. This mirrors what
# `tests/conftest.py` does for pytest and makes the CLI usable without an
# editable install during development.
try:
    from coloring_page_generator.processor import convert_to_coloring_page
except Exception:
    # compute repo/src and insert to sys.path
    repo_root = _Path(__file__).resolve().parents[1]
    src_path = str(repo_root / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from coloring_page_generator.processor import convert_to_coloring_page


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert image to coloring-page outline")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path (PNG recommended)")
    parser.add_argument("--blur", type=int, default=5, help="Gaussian blur kernel (odd int)")
    parser.add_argument("--th1", type=int, default=50, help="Canny threshold1")
    parser.add_argument("--th2", type=int, default=150, help="Canny threshold2")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    out = convert_to_coloring_page(
        input_path,
        output_path,
        blur_ksize=args.blur,
        canny_thresh1=args.th1,
        canny_thresh2=args.th2,
    )
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
