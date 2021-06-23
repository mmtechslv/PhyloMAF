r"""
Phylogenetic tree builder (pmaf.phylo.builders)
===============================================

*De-novo* tree builders
-----------------------

.. currentmodule:: pmaf.phylo.builders

This package :mod:`~pmaf.phylo.builders` contain wrapper classes that utilize
external tools to build a *de-novo* phylogenetic tree.

Classes
-------

.. autosummary::
   :toctree: generated/

    TreeBuilderFastTree2

"""

from ._fasttree2 import TreeBuilderFastTree2

__all__ = ["TreeBuilderFastTree2"]
