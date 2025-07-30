"""
__main__.py
-----------

Module entry point for running `python -m imagefox`.
Delegates to the CLI handler defined in cli.py.

Author: Pradyumna Das Roy
License: MIT
"""

from .cli import main

if __name__ == "__main__":
    main()
