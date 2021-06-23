r"""
Database (pmaf.database)
========================

Building and management of databases
------------------------------------

.. currentmodule:: pmaf.database

This package :mod:`~pmaf.database` is responsible for construction, maintenance and
management of taxonomic classification databases.

Database Manifests (Classes)
----------------------------

.. autosummary::
   :toctree: generated/

    DatabaseGreengenes
    DatabaseOTL
    DatabaseGTDB
    DatabaseUNITE
    DatabaseSILVA

Other (Classes)
---------------

.. autosummary::
   :toctree: generated/

   DatabaseStorageManager


"""

from ._helpers import *  # noqa: F401,F403
from ._manifest import *  # noqa: F401,F403
from ._manager import DatabaseStorageManager

__all__ = [
    "DatabaseStorageManager",
    "DatabaseGreengenes",
    "DatabaseOTL",
    "DatabaseGTDB",
    "DatabaseUNITE",
    "DatabaseSILVA",
]
