"""PyUnit tests for the Gamma Guard numerical core."""

import sys
import unittest
from pathlib import Path

SRC_DIRECTORY = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIRECTORY))

from gamma_core import (  # noqa: E402
    GammaDomainError,
    GammaRangeError,
    InputFormatError,
    evaluate_input,
    gamma_lanczos,
    is_gamma_pole,
    is_near_gamma_pole,
    method_name,
    parse_real,
)


class TestInputParsing(unittest.TestCase):
    """Test supported and unsupported user input."""

    def test_parse_decimal(self):
        """Parse a standard decimal value."""
        self.assertAlmostEqual(parse_real("2.5"), 2.5)

    def test_parse_negative_decimal(self):
        """Parse a negative decimal value."""
        self.assertAlmostEqual(parse_real("-1.5"), -1.5)

    def test_parse_exponent_notation(self):
        """Parse scientific notation."""
        self.assertAlmostEqual(parse_real("1e-3"), 0.001)

    def test_reject_empty_input(self):
        """Reject an empty input string."""
        with self.assertRaises(InputFormatError):
            parse_real("")

    def test_reject_non_numeric_input(self):
        """Reject alphabetic input."""
        with self.assertRaises(InputFormatError):
            parse_real("abc")

    def test_reject_multiple_values(self):
        """Reject input containing more than one value."""
        with self.assertRaises(InputFormatError):
            parse_real("1 2")


class TestGammaCalculation(unittest.TestCase):
    """Test representative Lanczos and reflection calculations."""

    def test_gamma_one(self):
        """Gamma(1) equals 1."""
        self.assertAlmostEqual(gamma_lanczos(1.0), 1.0, places=12)

    def test_gamma_five(self):
        """Gamma(5) equals 24."""
        self.assertAlmostEqual(gamma_lanczos(5.0), 24.0, places=11)

    def test_gamma_half(self):
        """Gamma(0.5) matches the known reference value."""
        expected = 1.772453850905516
        self.assertAlmostEqual(gamma_lanczos(0.5), expected, places=12)

    def test_gamma_negative_half(self):
        """Negative one-half uses reflection and matches its reference."""
        expected = -3.544907701811032
        self.assertAlmostEqual(gamma_lanczos(-0.5), expected, places=11)

    def test_gamma_negative_one_and_half(self):
        """Gamma(-1.5) matches its known reference value."""
        expected = 2.363271801207355
        self.assertAlmostEqual(gamma_lanczos(-1.5), expected, places=11)


class TestDomainAndRangeHandling(unittest.TestCase):
    """Test poles, near-pole detection, and supported numeric range."""

    def test_zero_is_pole(self):
        """Zero is an exact Gamma pole."""
        self.assertTrue(is_gamma_pole(0.0))

    def test_negative_integer_is_pole(self):
        """Negative integers are exact Gamma poles."""
        self.assertTrue(is_gamma_pole(-2.0))

    def test_non_integer_is_not_pole(self):
        """Negative non-integers remain valid Gamma inputs."""
        self.assertFalse(is_gamma_pole(-0.5))

    def test_gamma_zero_raises_domain_error(self):
        """Gamma(0) must be rejected."""
        with self.assertRaises(GammaDomainError):
            gamma_lanczos(0.0)

    def test_gamma_negative_integer_raises_domain_error(self):
        """Gamma at a negative integer must be rejected."""
        with self.assertRaises(GammaDomainError):
            gamma_lanczos(-1.0)

    def test_near_pole_is_detected(self):
        """A valid value very close to -1 should trigger sensitivity."""
        self.assertTrue(is_near_gamma_pole(-1.0000000000001))

    def test_large_positive_input_raises_range_error(self):
        """A Gamma result beyond double precision must be rejected."""
        with self.assertRaises(GammaRangeError):
            gamma_lanczos(172.0)


class TestUserFacingService(unittest.TestCase):
    """Test method reporting and user-facing evaluation output."""

    def test_lanczos_method_name(self):
        """Inputs at or above 0.5 use the direct Lanczos path."""
        self.assertEqual(method_name(5.0), "Lanczos approximation")

    def test_reflection_method_name(self):
        """Inputs below 0.5 report the reflection path."""
        self.assertEqual(
            method_name(-0.5),
            "Euler reflection formula + Lanczos approximation",
        )

    def test_evaluate_input_reports_result_and_method(self):
        """Successful evaluation includes the result and method."""
        message = evaluate_input("5")
        self.assertIn("Gamma(5) = 24", message)
        self.assertIn("Method: Lanczos approximation", message)

    def test_evaluate_input_reports_near_pole_warning(self):
        """Near-pole input includes a numerical-sensitivity warning."""
        message = evaluate_input("-1.0000000000001")
        self.assertIn("Warning:", message)
        self.assertIn("Gamma pole", message)
        self.assertIn("numerically sensitive", message)


if __name__ == "__main__":
    unittest.main()
