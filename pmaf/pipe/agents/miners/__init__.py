r"""
Data Miners  (:mod:`pmaf.pipe.agents.miners`)
=============================================

.. currentmodule:: pmaf.pipe.agents.miners

This sub-package :mod:`~pmaf.pipe.agents.miners` contains single class
:class:`~pmaf.pipe.agents.miners.Miner` that can be used to mine the data via
mediators without implicitly using `mediators`. Miners are recommended way for mining
data in PhyloMAF.


Miners (Classes)
----------------

.. autosummary::
   :toctree: generated/

   Miner

"""
from ._miner import Miner

__all__ = ['Miner']