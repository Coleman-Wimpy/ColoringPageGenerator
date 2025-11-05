"""Image processing utilities for converting photos into coloring-book pages.

The main entrypoint is `convert_to_coloring_page(input_path, output_path, *,
blur_ksize=5, canny_thresh1=50, canny_thresh2=150, invert=True)`.

This implementation uses OpenCV and Pillow to produce a clean black-outline on a
white background suitable for printing or coloring.
"""
from typing import Optional
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def convert_to_coloring_page(
    input_path: str | Path,
    output_path: str | Path,
    *,
    blur_ksize: int = 5,
    canny_thresh1: int = 50,
    canny_thresh2: int = 150,
    invert: bool = True,
) -> Path:
    """Convert an image file to a black-outline coloring page and save it.

    Args:
        input_path: Path to the source image.
        output_path: Path where the output PNG will be written.
        blur_ksize: Kernel size for Gaussian blur (odd int >=1).
        canny_thresh1: First threshold for the hysteresis procedure in Canny.
        canny_thresh2: Second threshold for the hysteresis procedure in Canny.
        invert: If True, ensure output has black lines on white background.

    Returns:
        Path to the written output file.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if blur_ksize % 2 == 0:
        blur_ksize += 1

    # Read via OpenCV (BGR)
    img_bgr = cv2.imdecode(np.fromfile(str(input_path), dtype=np.uint8), cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise ValueError(f"Could not read image: {input_path}")

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Optional denoise / blur to remove small details
    if blur_ksize > 1:
        gray = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)

    # Use Canny edge detector
    edges = cv2.Canny(gray, canny_thresh1, canny_thresh2)

    # Dilate edges slightly to make lines thicker and continuous
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # Convert edges (white on black) to black lines on white background
    if invert:
        # edges currently: 255 where edges; make a white background with black lines
        output = 255 - edges
    else:
        output = edges

    # Ensure binary (0 or 255)
    _, output = cv2.threshold(output, 127, 255, cv2.THRESH_BINARY)

    # Save via Pillow to preserve unicode paths on Windows
    pil = Image.fromarray(output)
    pil = pil.convert("L")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pil.save(str(output_path))

    return output_path
