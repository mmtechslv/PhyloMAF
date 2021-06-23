r"""
Pipe (pmaf.pipe)
================

Working with data mining pipelines
-----------------------------------

.. currentmodule:: pmaf.pipe

This package :mod:`~pmaf.pipe` is responsible for creating and using taxonomic,
phylogenetic, sequence and accession data pipeline.

Sub-Packages
------------

.. toctree::
   :maxdepth: 1

   Mining agents (pmaf.pipe.agents) <pmaf.pipe.agents>
   Basic mining factors (pmaf.pipe.factors) <pmaf.pipe.factors>
   Marker classes for easy mining (pmaf.pipe.markers) <pmaf.pipe.markers>
   Pipeline specifications (pmaf.pipe.specs) <pmaf.pipe.specs>

"""
from . import specs
from . import factors
from . import agents
from . import markers

__all__ = ["agents", "factors", "markers", "specs"]
