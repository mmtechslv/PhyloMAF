r"""
Sub-Package Factors  (:mod:`pmaf.pipe.factors`)
===============================================

.. currentmodule:: pmaf.pipe.factors

This sub-package :mod:`~pmaf.pipe.factors` contain `factor` classes required to
perform any mining activity. Essentially factors help `miners` to know what kind of
data will be mined.

Factors (Classes)
-----------------

.. autosummary::
   :toctree: generated/

   Factor16S

"""
from ._inventory import Factor16S

__all__ = ['Factor16S']