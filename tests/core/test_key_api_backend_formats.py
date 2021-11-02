import pytest

from brambl.ed25519 import Ed25519CredentialAPI
from brambl.ed25519.backends.native import NativeECCBackend


@pytest.fixture(autouse=True)
def native_backend_env_var(monkeypatch):
    monkeypatch.setenv('ECC_BACKEND_CLASS', 'brambl.ed25519.backends.native.NativeECCBackend')


@pytest.mark.parametrize(
    'backend',
    (
            None,
            NativeECCBackend(),
            NativeECCBackend,
            'brambl.ed25519.backends.NativeECCBackend',
            'brambl.ed25519.backends.native.NativeECCBackend',
    ),
)
def test_supported_backend_formats(backend):
    keys = Ed25519CredentialAPI(backend=backend)
    assert isinstance(keys.backend, NativeECCBackend)
