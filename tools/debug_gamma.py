"""Small driver used to demonstrate pdb debugging."""

import sys
from pathlib import Path

SRC_DIRECTORY = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIRECTORY))

from gamma_core import gamma_lanczos  # noqa: E402


def main():
    """Run one Gamma calculation for debugger inspection."""
    x_value = -0.5
    result = gamma_lanczos(x_value)

    print("Input:", x_value)
    print("Gamma result:", result)


if __name__ == "__main__":
    main()
