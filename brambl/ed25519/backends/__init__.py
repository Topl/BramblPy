import os
from typing import Type

from brambl.ed25519.backends.base import BaseEd25519Backend
from brambl.ed25519.utils.moduleloading import import_string

from .base import BaseEd25519Backend
from .native import NativeECCBackend


def get_default_backend_class() -> str:
    return 'brambl.ed25519.backends.native.main.NativeECCBackend'


def get_backend_class(import_path: str = None) -> Type[BaseEd25519Backend]:
    if import_path is None:
        import_path = os.environ.get(
            'ECC_BACKEND_CLASS',
            get_default_backend_class(),
        )
    return import_string(import_path)


def get_backend(import_path: str = None) -> BaseEd25519Backend:
    backend_class = get_backend_class(import_path)
    return backend_class()
