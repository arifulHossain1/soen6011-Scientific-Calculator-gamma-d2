"""Core numerical implementation for Gamma Guard.

This module contains the from-scratch numerical work for SOEN 6011:
manual input parsing, custom exceptions, sine/exponential/logarithm
approximations, domain checks, Lanczos evaluation, and result formatting.

The production calculation intentionally does not import Python's math module.
"""

# ---------------------------------------------------------------------------
# Numerical constants
# ---------------------------------------------------------------------------

PI = 3.14159265358979323846264338327950288419716939937510
TWO_PI = 6.28318530717958647692528676655900576839433879875020
LN_2 = 0.69314718055994530941723212145817656807550013436026
LN_PI = 1.1447298858494001741434273513530587116472948129153
LN_SQRT_TWO_PI = 0.91893853320467274178032973640561763986139747363778

LANCZOS_G = 7.0
LANCZOS_COEFFICIENTS = (
    0.99999999999980993,
    676.5203681218851,
    -1259.1392167224028,
    771.32342877765313,
    -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
    9.9843695780195716e-6,
    1.5056327351493116e-7,
)

POLE_WARNING_TOLERANCE = 1.0e-12
MAX_EXP_ARGUMENT = 709.782712893384
MIN_EXP_ARGUMENT = -745.0
MAX_RESULT_MAGNITUDE = 1.7976931348623157e308


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------

class GammaGuardError(Exception):
    """Base class for expected, user-facing Gamma Guard errors."""


class InputFormatError(GammaGuardError):
    """Raised when text is not one supported finite real number."""


class GammaDomainError(GammaGuardError):
    """Raised when Gamma is requested at an exact real pole."""


class GammaRangeError(GammaGuardError):
    """Raised when the result exceeds supported floating-point range."""


class GammaUnderflowError(GammaGuardError):
    """Raised when a nonzero result becomes numerical zero."""


# ---------------------------------------------------------------------------
# Manual input parsing
# ---------------------------------------------------------------------------

def text_length(text):
    """Return string length using indexing and a manual counter."""
    count = 0
    while True:
        try:
            text[count]
        except IndexError:
            return count
        count = count + 1


def digit_value(character):
    """Return the numeric value of one decimal digit, or -1."""
    digits = "0123456789"
    value = 0
    limit = text_length(digits)
    while value < limit:
        if character == digits[value]:
            return value
        value = value + 1
    return -1


def power_of_ten(exponent):
    """Return ten raised to an integer exponent by repeated arithmetic."""
    if exponent > 308:
        raise InputFormatError(
            "number is too large for double-precision input"
        )
    if exponent < -324:
        return 0.0

    result = 1.0
    if exponent >= 0:
        count = 0
        while count < exponent:
            result = result * 10.0
            count = count + 1
        return result

    count = 0
    while count < -exponent:
        result = result / 10.0
        count = count + 1
    return result


def parse_real(text):
    """Parse one finite decimal number, optionally in exponent notation."""
    raw = text.strip()
    if raw == "":
        raise InputFormatError(
            "enter a finite real number, such as 0.5 or -1.5"
        )

    sign = 1.0
    index = 0
    length = text_length(raw)

    if raw[index] == "+":
        index = index + 1
    elif raw[index] == "-":
        sign = -1.0
        index = index + 1

    if index >= length:
        raise InputFormatError("enter digits after the sign")

    integer_part = 0.0
    fraction_part = 0.0
    fraction_scale = 1.0
    digit_seen = False

    while index < length:
        digit = digit_value(raw[index])
        if digit < 0:
            break
        integer_part = integer_part * 10.0 + digit
        digit_seen = True
        index = index + 1

    if index < length and raw[index] == ".":
        index = index + 1
        while index < length:
            digit = digit_value(raw[index])
            if digit < 0:
                break
            fraction_scale = fraction_scale / 10.0
            fraction_part = fraction_part + digit * fraction_scale
            digit_seen = True
            index = index + 1

    if not digit_seen:
        raise InputFormatError(
            "enter a finite real number, such as 0.5 or -1.5"
        )

    exponent = 0
    exponent_sign = 1
    if index < length and (raw[index] == "e" or raw[index] == "E"):
        index = index + 1
        if index >= length:
            raise InputFormatError("enter digits after the exponent symbol")
        if raw[index] == "+":
            index = index + 1
        elif raw[index] == "-":
            exponent_sign = -1
            index = index + 1
        if index >= length:
            raise InputFormatError("enter digits after the exponent sign")

        exponent_digit_seen = False
        while index < length:
            digit = digit_value(raw[index])
            if digit < 0:
                break
            exponent = exponent * 10 + digit
            exponent_digit_seen = True
            index = index + 1
        if not exponent_digit_seen:
            raise InputFormatError("enter digits in the exponent")

    if index != length:
        raise InputFormatError("enter only one finite real number")

    value = (
        sign
        * (integer_part + fraction_part)
        * power_of_ten(exponent_sign * exponent)
    )
    if value > MAX_RESULT_MAGNITUDE or value < -MAX_RESULT_MAGNITUDE:
        raise InputFormatError(
            "input is outside the supported double-precision range"
        )
    return value


# ---------------------------------------------------------------------------
# From-scratch numerical helpers
# ---------------------------------------------------------------------------

def abs_value(value):
    """Return absolute value using comparison and unary negation."""
    if value < 0.0:
        return -value
    return value


def nearest_integer(value):
    """Return the nearest integer for pole and sensitivity checks."""
    if value >= 0.0:
        return int(value + 0.5)
    return int(value - 0.5)


def reduce_angle(angle):
    """Reduce an angle to approximately [-pi, pi]."""
    multiple = int(angle / TWO_PI)
    reduced = angle - multiple * TWO_PI
    while reduced > PI:
        reduced = reduced - TWO_PI
    while reduced < -PI:
        reduced = reduced + TWO_PI
    return reduced


def sin_taylor(angle):
    """Approximate sin(angle) using range reduction and a Taylor series."""
    x_value = reduce_angle(angle)
    term = x_value
    total = x_value
    n_value = 1
    while n_value <= 16:
        denominator = (2 * n_value) * (2 * n_value + 1)
        term = -term * x_value * x_value / denominator
        total = total + term
        n_value = n_value + 1
    return total


def exp_taylor(exponent):
    """Approximate e raised to exponent using range reduction and a series."""
    if exponent > MAX_EXP_ARGUMENT:
        raise GammaRangeError(
            "Gamma(x) is outside the supported double-precision range."
        )
    if exponent < MIN_EXP_ARGUMENT:
        return 0.0

    pieces = int(abs_value(exponent)) + 1
    reduced = exponent / pieces

    term = 1.0
    total = 1.0
    n_value = 1
    while n_value <= 45:
        term = term * reduced / n_value
        total = total + term
        n_value = n_value + 1

    result = 1.0
    count = 0
    while count < pieces:
        result = result * total
        count = count + 1
    return result


def natural_log(value):
    """Approximate natural logarithm using scaling and an atanh series."""
    if value <= 0.0:
        raise GammaRangeError("logarithm input must be positive")

    scaled = value
    scale_count = 0
    while scaled > 1.5:
        scaled = scaled / 2.0
        scale_count = scale_count + 1
    while scaled < 0.75:
        scaled = scaled * 2.0
        scale_count = scale_count - 1

    z_value = (scaled - 1.0) / (scaled + 1.0)
    z_squared = z_value * z_value
    term = z_value
    total = 0.0
    denominator = 1
    count = 0
    while count < 80:
        total = total + term / denominator
        term = term * z_squared
        denominator = denominator + 2
        count = count + 1

    return 2.0 * total + scale_count * LN_2


def power_positive(base, exponent):
    """Compute a positive base raised to a real exponent without math.pow."""
    if base <= 0.0:
        raise GammaRangeError("power base must be positive")
    return exp_taylor(exponent * natural_log(base))


# ---------------------------------------------------------------------------
# Gamma calculation and user-facing service
# ---------------------------------------------------------------------------

def is_gamma_pole(x_value):
    """Return True only for exact poles: 0, -1, -2, ..."""
    if x_value > 0.0:
        return False

    nearest = nearest_integer(x_value)
    return x_value == nearest


def is_near_gamma_pole(x_value):
    """Return True for a non-pole close to a nonpositive integer."""
    if x_value > 0.0 or is_gamma_pole(x_value):
        return False
    nearest = nearest_integer(x_value)
    if nearest > 0:
        return False
    return abs_value(x_value - nearest) < POLE_WARNING_TOLERANCE


def log_gamma_lanczos_positive(x_value):
    """Return ln(Gamma(x)) for x >= 0.5 using Lanczos."""
    z_value = x_value - 1.0
    series = LANCZOS_COEFFICIENTS[0]
    index = 1
    while index <= 8:
        series = series + LANCZOS_COEFFICIENTS[index] / (z_value + index)
        index = index + 1

    if series <= 0.0:
        raise GammaRangeError("Lanczos series became nonpositive")

    t_value = z_value + LANCZOS_G + 0.5
    return (
        LN_SQRT_TWO_PI
        + (z_value + 0.5) * natural_log(t_value)
        - t_value
        + natural_log(series)
    )


def gamma_lanczos(x_value):
    """Compute Gamma(x) using Lanczos and Euler reflection in log space."""
    if is_gamma_pole(x_value):
        raise GammaDomainError(
            "Gamma(x) is undefined at 0 and negative integers. "
            "Enter a positive value or a negative non-integer."
        )

    sign = 1.0
    if x_value < 0.5:
        sine_value = sin_taylor(PI * x_value)
        sine_magnitude = abs_value(sine_value)
        if sine_magnitude == 0.0:
            raise GammaDomainError(
                "Gamma(x) is undefined at 0 and negative integers. "
                "Enter a positive value or a negative non-integer."
            )
        if sine_value < 0.0:
            sign = -1.0
        log_magnitude = (
            LN_PI
            - natural_log(sine_magnitude)
            - log_gamma_lanczos_positive(1.0 - x_value)
        )
    else:
        log_magnitude = log_gamma_lanczos_positive(x_value)

    if log_magnitude > MAX_EXP_ARGUMENT:
        raise GammaRangeError(
            "Gamma(x) is outside the supported double-precision range."
        )
    if log_magnitude < MIN_EXP_ARGUMENT:
        raise GammaUnderflowError(
            "Gamma(x) underflowed to zero in double precision. "
            "Try an input farther from extreme values."
        )

    result = sign * exp_taylor(log_magnitude)
    if result == 0.0:
        raise GammaUnderflowError(
            "Gamma(x) underflowed to zero in double precision. "
            "Try an input farther from extreme values."
        )
    if result > MAX_RESULT_MAGNITUDE or result < -MAX_RESULT_MAGNITUDE:
        raise GammaRangeError(
            "Gamma(x) is outside the supported double-precision range."
        )
    return result


def method_name(x_value):
    """Return the numerical path used for an input."""
    if x_value < 0.5:
        return "Euler reflection formula + Lanczos approximation"
    return "Lanczos approximation"


def format_input_number(value):
    """Format an input value in a familiar compact form."""
    integer_value = int(value)
    if value == integer_value:
        return str(integer_value)
    return format(value, ".12g")


def format_result_number(value):
    """Show at least ten significant digits without needless notation."""
    magnitude = abs_value(value)
    if magnitude != 0.0 and (magnitude >= 1.0e12 or magnitude < 1.0e-6):
        return format(value, ".12e")
    return format(value, ".12f")


def evaluate_input(text):
    """Evaluate one GUI input and return a user-facing result message."""
    x_value = parse_real(text)
    warning = ""
    if is_near_gamma_pole(x_value):
        warning = (
            "Warning: input is very close to a Gamma pole; "
            "the result may be numerically sensitive.\n"
        )

    result = gamma_lanczos(x_value)
    return (
        warning
        + "Gamma(" + format_input_number(x_value) + ") = "
        + format_result_number(result) + "\n"
        + "Method: " + method_name(x_value)
    )
