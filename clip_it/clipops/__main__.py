"""Entry point for python -m clipops"""

import sys
from clipops.cli import app

if __name__ == "__main__":
    sys.exit(app())