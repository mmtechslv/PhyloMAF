r"""
Pipe Specs  (:mod:`pmaf.pipe.specs`)
====================================================

.. currentmodule:: pmaf.pipe.specs

This sub-package :mod:`~pmaf.pipe.specs` contain collection of simple classes that
serve as specifications for data pipelines.

Specifications (Classes)
------------------------

Primitive Specs
^^^^^^^^^^^^^^^

.. autosummary::
   :recursive:
   :toctree: generated/

    SpecIP
    SpecIS
    SpecTI
    SpecIT
    SpecIA

Composite Specs
^^^^^^^^^^^^^^^

.. autosummary::
   :recursive:
   :toctree: generated/

    SpecTP
    SpecTS
    SpecTSPBP
    SpecTSBP

Special Functions
^^^^^^^^^^^^^^^^^

.. autosummary::
   :recursive:
   :toctree: generated/

    ForgeSpec

"""

from ._inventory import *

__all__ = [
    "SpecTP",
    "SpecTS",
    "SpecTSPBP",
    "SpecTSBP",
    "ForgeSpec",
    "SpecIP",
    "SpecIS",
    "SpecTI",
    "SpecIT",
    "SpecIA",
]
