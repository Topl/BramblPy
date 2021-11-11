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


class TransactionNotFound(Exception):
    """
    Raised when a tx hash used to lookup a tx in a jsonrpc call cannot be found.
    """
    pass


class TimeExhausted(Exception):
    """
    Raised when a method has not retrieved the desired result within a specified timeout.
    """
    pass


class BlockNotFound(Exception):
    """
    Raised when the block id used to lookup a block in a jsonrpc call cannot be found.
    """
    pass


class InvalidAddress(ValueError):
    """
    The supplied address does not have a valid checksum
    """
    pass
