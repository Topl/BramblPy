
import sys

import pkg_resources

if sys.version_info < (3, 5):
    raise EnvironmentError(
        "Python 3.5 or above is required. ")

__version__ = pkg_resources.get_distribution("brambl").version