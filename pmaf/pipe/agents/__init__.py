r"""
Pipe Agents (:mod:`pmaf.pipe.agents`)
=====================================

.. currentmodule:: pmaf.pipe.agents

.. rubric:: Working with data mining pipelines

This sub-package :mod:`~pmaf.pipe.agents` contains classes for transitional data
management,  mediator classes for remote and local databases and data main miner
class.

Agents (Packages)
-----------------

.. autosummary::
   :toctree:

   dockers
   mediators
   miners

"""

from . import dockers
from . import mediators
from . import miners

__all__ = ["dockers", "mediators", "miners"]
