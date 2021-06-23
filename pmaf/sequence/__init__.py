r"""
Sequence (pmaf.sequence)
========================

Working with sequence data
--------------------------

Classes
-----------------

.. autosummary::
   :toctree: generated/

   MultiSequence
   MultiSequenceStream
   Nucleotide

"""
from ._sequence import * # noqa: F401,F403
from ._multiple import * # noqa: F401,F403

__all__ = ['MultiSequence', 'MultiSequenceStream', 'Nucleotide']

