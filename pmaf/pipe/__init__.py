r"""
Pipe (pmaf.pipe)
================

Working with data mining pipelines
-----------------------------------

.. currentmodule:: pmaf.pipe

This package :mod:`~pmaf.pipe` is responsible for creating and using taxonomic,
phylogenetic, sequence and accession data pipeline.


.. toctree::
   :hidden:
   :maxdepth: 1

   pmaf.pipe.agents
   pmaf.pipe.factors
   pmaf.pipe.markers
   pmaf.pipe.specs

Sub-Packages
------------

.. autosummary::
   :toctree: generated/

   agents
   factors
   markers
   specs


"""
from . import specs
from . import factors
from . import agents
from . import markers

__all__ = ["agents", "factors", "markers", "specs"]
