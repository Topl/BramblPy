class CannotHandleRequest(Exception):
    """
    Raised by a provider to signal that it cannot handle an RPC request and
    that the manager should proceed to the next provider.
    """
    pass


class BadResponseFormat(ValueError, KeyError):
    # Inherits from KeyError and ValueError for backwards compatibility
    """
    Raised when a JSON-RPC response comes back in an unexpected format
    """
    pass
