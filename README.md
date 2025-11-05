# ColoringPageGenerator
This takes a picture and turns it into a coloring book page.

Getting started
---------------
This repository contains a small Python utility that turns photos into black-and-white outline images suitable for coloring-book pages.

Quick setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Convert an image using the provided script:

```powershell
python scripts/convert_image.py input.jpg output.png --blur 5 --th1 50 --th2 150
```

Run tests:

```powershell
pytest -q
```

Notes
-----
- The implementation uses OpenCV's Canny edge detector and Pillow for reading/writing image files. Adjust Canny thresholds and blur to match your input images.

Install editable (recommended for development)
-------------------------------------------
During development you can install the package in editable mode so scripts and imports work as if the package were installed:

```powershell
python -m pip install -e .
```

Quick fixes if you see "ModuleNotFoundError: No module named 'coloring_page_generator'"
---------------------------------------------------------------------------------
- Run the script with `PYTHONPATH` pointing at the `src/` directory:

```powershell
python -c "import sys; sys.path.insert(0, ("$(Resolve-Path .\src).Path")); from coloring_page_generator.processor import convert_to_coloring_page; print('import ok')"
```

- Or (short-term) run the CLI script directly; it now attempts to add `src/` to `sys.path` automatically when the package isn't installed.


