import pytest

from brambl.method import Method


def test_method_accepts_callable_for_selector():
    method = Method(
        json_rpc_method=lambda *_: 'topl_method',
    )
    assert method.method_selector_fn() == 'topl_method'


def test_method_selector_fn_accepts_str():
    method = Method(
        json_rpc_method='topl_method',
    )
    assert method.method_selector_fn() == 'topl_method'


def test_method_selector_fn_invalid_arg():
    with pytest.raises(ValueError):
        method = Method(
            json_rpc_method=555555,
        )
        method.method_selector_fn()
