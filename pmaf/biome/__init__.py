r"""
Module Biome  (:mod:`pmaf.biome`)
===================================

.. currentmodule:: pmaf.biome

This Module :mod:`~pmaf.biome` is responsible for processing and analysis of data
like OTU/ASV Taxonomy, OTU-tables with frequency/count data, Representative sequences
of OTUs, Representative phylogenetic tree of OTUs and Sample metadata


Examples
--------
New sequences are created with optional metadata and positional metadata.
Metadata is stored as a Python ``dict``, while positional metadata is stored as
a pandas ``DataFrame``.

>>> from skbio import DNA, RNA
>>> d = DNA('ACCGGGTA', metadata={'id':"my-sequence", 'description':"GFP"},
...          positional_metadata={'quality':[22, 25, 22, 18, 23, 25, 25, 25]})
>>> d

"""

from .assembly import *  # noqa: F401,F403
from .essentials import *  # noqa: F401,F403
from .survey import *  # noqa: F401,F403
