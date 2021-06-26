r"""
Pipe (pmaf.pipe)
================

.. currentmodule:: pmaf.pipe

Working with data mining pipelines
-----------------------------------

This package :mod:`~pmaf.pipe` is responsible for creating and using taxonomic,
phylogenetic, sequence and accession data pipeline.


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
