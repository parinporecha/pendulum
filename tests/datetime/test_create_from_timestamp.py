from __future__ import annotations

import pendulum

from pendulum import timezone
from tests.conftest import assert_datetime


def test_create_from_timestamp_returns_pendulum():
    d = pendulum.from_timestamp(pendulum.datetime(1975, 5, 21, 22, 32, 5).timestamp())
    assert_datetime(d, 1975, 5, 21, 22, 32, 5)
    assert d.timezone_name == "UTC"


def test_create_from_timestamp_with_timezone_string():
    d = pendulum.from_timestamp(0, "America/Toronto")
    assert d.timezone_name == "America/Toronto"
    assert_datetime(d, 1969, 12, 31, 19, 0, 0)


def test_create_from_timestamp_with_timezone():
    d = pendulum.from_timestamp(0, timezone("America/Toronto"))
    assert d.timezone_name == "America/Toronto"
    assert_datetime(d, 1969, 12, 31, 19, 0, 0)


def test_create_from_timestamp_negative():
    """Negative timestamps earlier than 12h before the Unix epoch should work.

    Regression test for issue 956: on Windows (and potentially other
    platforms), datetime.fromtimestamp raises OSError for timestamps
    below a platform-specific minimum.  pendulum should still return a
    correct DateTime.
    """
    # -43201 is 1 second past the 12h-before-epoch boundary reported in the issue
    d = pendulum.from_timestamp(-43201)
    assert_datetime(d, 1969, 12, 31, 11, 59, 59)
    assert d.timezone_name == "UTC"


def test_create_from_timestamp_negative_with_timezone():
    """Negative timestamps with an explicit timezone should also work."""
    d = pendulum.from_timestamp(-43201, "America/Toronto")
    assert d.timezone_name == "America/Toronto"
    assert_datetime(d, 1969, 12, 31, 6, 59, 59)


def test_create_from_timestamp_negative_with_microseconds():
    """Negative float timestamps preserving microseconds."""
    d = pendulum.from_timestamp(-43201.5)
    assert_datetime(d, 1969, 12, 31, 11, 59, 58, 500000)
    assert d.timezone_name == "UTC"
