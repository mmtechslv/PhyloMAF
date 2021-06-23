r"""
Biome (pmaf.biome)
==================

Processing and analysis of biome data
-------------------------------------

.. currentmodule:: pmaf.biome

This package :mod:`~pmaf.biome` is responsible for processing and analysis of data
like OTU/ASV Taxonomy, OTU-tables with frequency/count data, Representative sequences
of OTUs, Representative phylogenetic tree of OTUs and Sample metadata

Essentials (Classes)
--------------------

.. autosummary::
   :toctree: generated/
   
    RepTaxonomy
    RepSequence
    RepPhylogeny
    FrequencyTable
    SampleMetadata

Assemblies and Survey (Classes)
-------------------------------

.. autosummary::
   :toctree: generated/
   
   BiomeAssembly
   BiomeSurvey

"""

from .assembly import *  # noqa: F401,F403
from .essentials import *  # noqa: F401,F403
from .survey import *  # noqa: F401,F403

__all__ = [
    "RepTaxonomy",
    "RepSequence",
    "RepPhylogeny",
    "FrequencyTable",
    "SampleMetadata",
    "BiomeAssembly",
    "BiomeSurvey",
]
