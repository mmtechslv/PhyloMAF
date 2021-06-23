r"""
Dockers  (:mod:`pmaf.pipe.agents.dockers`)
======================================================

.. currentmodule:: pmaf.pipe.agents.dockers.

This sub-package :mod:`~pmaf.pipe.agents.dockers` contains classes for transitional
data management called `docker` instances. Any instance of `docker` can be seen as a
temporary data dock that is understood by :mod:`~pmaf.pipe.agents.mediators` and
:mod:`~pmaf.pipe.agents.miners`.


Classes
-------

.. autosummary::
   :toctree: generated/

   DockerAccessionMedium
   DockerIdentifierMedium
   DockerPhylogenyMedium
   DockerSequenceMedium
   DockerTaxonomyMedium

"""
from ._mediums import *

__all__ = [
    "DockerAccessionMedium",
    "DockerIdentifierMedium",
    "DockerPhylogenyMedium",
    "DockerSequenceMedium",
    "DockerTaxonomyMedium",
]
