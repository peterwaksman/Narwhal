"""Tests for narwhal.nwfind."""

import pytest

from narwhal import nwfind


@pytest.mark.parametrize('kword, expected', [
    ('', 0),
    ('a#b', 1),
    ('a*b', 2),
    ('a', 1),
])
def test_kword_len(kword, expected):
    assert nwfind.kwordLen(kword) == expected
