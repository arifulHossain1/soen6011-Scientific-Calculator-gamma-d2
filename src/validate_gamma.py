"""Validation-only script.

Python's math.gamma() is used only as a trusted comparison reference and is
never imported by the production GUI or Gamma calculation modules.
"""

import math

from gamma_core import gamma_lanczos


VALIDATION_CASES = (0.1, 0.5, 1.0, 1.5, 2.5, 5.0, -0.5, -1.5)
MAX_ALLOWED_RELATIVE_ERROR = 1.0e-10


def relative_error(actual, reference):
    """Return relative error, with an absolute fallback at zero."""
    if reference == 0.0:
        return abs(actual - reference)
    return abs((actual - reference) / reference)


def main():
    """Print validation evidence for the eight D1/D2 cases."""
    maximum_error = 0.0
    all_passed = True

    print("x\tGamma Guard\tReference\tRelative error\tStatus")
    for x_value in VALIDATION_CASES:
        actual = gamma_lanczos(x_value)
        reference = math.gamma(x_value)
        error = relative_error(actual, reference)
        if error > maximum_error:
            maximum_error = error
        status = "PASS" if error <= MAX_ALLOWED_RELATIVE_ERROR else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(
            f"{x_value:g}\t{actual:.15g}\t{reference:.15g}\t"
            f"{error:.3e}\t{status}"
        )

    print()
    print(f"Maximum relative error: {maximum_error:.3e}")
    print(f"Required threshold: {MAX_ALLOWED_RELATIVE_ERROR:.1e}")
    print("Overall result:", "PASS" if all_passed else "FAIL")


if __name__ == "__main__":
    main()
