import tempfile
from pathlib import Path
from PIL import Image, ImageDraw

from coloring_page_generator.processor import convert_to_coloring_page


def test_convert_simple_shape(tmp_path: Path):
    # Create a simple image with a black rectangle on white background
    img_path = tmp_path / "in.png"
    out_path = tmp_path / "out.png"

    img = Image.new("RGB", (200, 200), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 160, 160], outline="black", width=5)
    img.save(img_path)

    # Run conversion
    convert_to_coloring_page(img_path, out_path, blur_ksize=3, canny_thresh1=30, canny_thresh2=100)

    assert out_path.exists()

    out = Image.open(out_path)
    assert out.mode in ("L", "RGB")
    # Output should be roughly the same size
    assert out.size == (200, 200)
