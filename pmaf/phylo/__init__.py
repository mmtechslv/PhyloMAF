r"""
Phylo (pmaf.phylo)
==================

Working with phylogeny data
---------------------------

Classes
-------

.. autosummary::
   :toctree: generated/

    PhyloTree

Sub-Packages
------------

.. toctree::
   :maxdepth: 1

   Branch Estimators (pmaf.phylo.branchest) <pmaf.phylo.branchest>
   *De-novo* tree builders (pmaf.phylo.builders) <pmaf.phylo.builders>

"""
from .tree import PhyloTree
from . import branchest
from . import builders

__all__ = ["PhyloTree", "branchest", "builders"]
