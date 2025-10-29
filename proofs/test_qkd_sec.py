import pytest

from src.qkd import bb84_keygen


def test_qkd_detects_eavesdropper():
    with pytest.raises(ValueError):
        bb84_keygen(length=1024, eve_is_present=True)
