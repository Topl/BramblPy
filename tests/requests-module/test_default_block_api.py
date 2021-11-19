import pytest


def test_uses_default_block(brambl, extra_addresses):
    assert (brambl.requests.default_block == 'latest')
    brambl.requests.default_block = brambl.requests.block_number
    assert (brambl.requests.default_block == brambl.requests.block_number)
