"""Entry point — works from the repo without a broken editable install."""

import sys
from pathlib import Path

# Allow `python main.py` even when `pip install -e .` did not configure sys.path.
_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from pycommonist.__main__ import main

if __name__ == "__main__":
    main()
