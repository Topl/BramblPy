import pytest

from brambl.method import Method, _apply_request_formatters


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


def test_get_formatters_default_formatter_for_falsy_config():
    method = Method(
        mungers=[],
        json_rpc_method='topl_method',
    )

    default_request_formatters = method.request_formatters(method.method_selector_fn())
    assert _apply_request_formatters(['a', 'b', 'c'], default_request_formatters) == ('a', 'b', 'c')


def test_get_formatters_non_falsy_config_retrieval():
    method = Method(
        mungers=[],
        json_rpc_method='topl_rawPolyTransfer',
    )
    method_name = method.method_selector_fn()
    first_formatter = method.request_formatters(method_name)
    assert first_formatter is not None

def test_input_munger_parameter_passthrough_matching_arity():
    method = Method(
        mungers=[lambda m, z, y: ['success']],
        json_rpc_method='topl_method',
    )
    method.input_munger(object(), ['first', 'second'], {}) == 'success'

def test_input_munger_falsy_config_result_in_default_munger():
    method = Method(
        mungers=[],
        json_rpc_method='topl_method',
    )
    method.input_munger(object(), [], {}) == []


