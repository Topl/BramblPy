from __future__ import absolute_import

import warnings
import sys


if sys.version_info.major < 3:
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn(DeprecationWarning(
        "The `eth-keyfile` library is dropping support for Python 2.  Upgrade to Python 3."
    ))
    warnings.resetwarnings()
