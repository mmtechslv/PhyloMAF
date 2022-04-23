r"""
Internals (pmaf.internal)
=========================

Internal classes and methods
----------------------------

Subpackages
-----------

.. toctree::
   :maxdepth: 1

   I/O <pmaf.internal.io>

"""
from . import _shared as SharedMethods

from . import _constants as Consts
from . import _extensions as Extensions

__all__ = ["io"]
