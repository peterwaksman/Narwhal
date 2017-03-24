"""Tests for narwhal.nwutils."""

import pytest

from narwhal import nwutils


@pytest.mark.parametrize('t, ifound, expected', [
    (2, [], [False, False]),
    (2, [1], [False, True]),
    (2, [3], [False, False]),
])
def test_compress_found(t, ifound, expected):
    assert nwutils.compressFound(t, ifound) == expected


@pytest.mark.parametrize('t, tmp, expected', [
    (2, [False, False], []),
    (2, [False, True], [1]),
    (2, [True, False], [0]),
    (2, [True, True], [0, 1])
])
def test_expand_found(t, tmp, expected):
    assert nwutils.expandFound(t, tmp) == expected


@pytest.mark.parametrize('t, ifound, expected', [
    (2, [], 0),
    (2, [1], 1),
    (2, [3], 0),
    (2, [0, 1], 2),
])
def test_count_found0(t, ifound, expected):
    assert nwutils.countFound0(t, ifound) == expected
