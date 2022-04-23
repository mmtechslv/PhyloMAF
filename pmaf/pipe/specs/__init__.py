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

    SpecIP
    SpecIS
    SpecTI
    SpecIT
    SpecIA

Composite Specs
^^^^^^^^^^^^^^^

.. autosummary::

    SpecTP
    SpecTS
    SpecTSPBP
    SpecTSBP

Special Functions
^^^^^^^^^^^^^^^^^

.. autosummary::

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
    "SpecAI"
]
