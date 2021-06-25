r"""
Database Mediators  (:mod:`pmaf.pipe.agents.mediators`)
=======================================================

.. currentmodule:: pmaf.pipe.agents.mediators

This sub-package :mod:`~pmaf.pipe.agents.mediators` contains classes called
`mediator`-classes. These are group of classes that are responsible for exploitation
of various remote and local databases. Each mediator class consist of multiple mixin
classes composition of which depends on the database instance that will be mediated.
Although, `mediators` are be directly used it is recommended to use `miner` instance
instead.

Mediators (Classes)
-------------------

.. autosummary::
   :toctree: generated/

   LocalMediator
   NCBIMediator

"""
from ._local import *
from ._remote import *

__all__ = ["LocalMediator", "NCBIMediator"]
