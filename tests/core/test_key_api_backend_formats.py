import pytest

from brambl.keys import KeyAPI
from brambl.keys.backends.native import NativeECCBackend


@pytest.fixture(autouse=True)
def native_backend_env_var(monkeypatch):
    monkeypatch.setenv('ECC_BACKEND_CLASS', 'brambl.keys.backends.native.NativeECCBackend')


@pytest.mark.parametrize(
    'backend',
    (
            None,
            NativeECCBackend(),
            NativeECCBackend,
            'brambl.keys.backends.NativeECCBackend',
            'brambl.keys.backends.native.NativeECCBackend',
    ),
)
def test_supported_backend_formats(backend):
    keys = KeyAPI(backend=backend)
    assert isinstance(keys.backend, NativeECCBackend)
