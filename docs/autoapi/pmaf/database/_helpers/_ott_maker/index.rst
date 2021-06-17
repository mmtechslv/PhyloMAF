:orphan:

:mod:`pmaf.database._helpers._ott_maker`
========================================

.. py:module:: pmaf.database._helpers._ott_maker


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.database._helpers._ott_maker.make_ott_taxonomy


.. function:: make_ott_taxonomy(reference_taxonomy_path: str, new_taxonomy_path: str, otl_reftax_src: str) -> bool

   Reconstructs OpenTreeOfLife taxonomy by removing non-microbial life clades.

   :param reference_taxonomy_path: Path to reference taxonomy directory. `
                                   Download Latest OTT <https://tree.opentreeoflife.org/about/taxonomy-version>`_
                                   Run Make to compile OTT Jython files.
   :param new_taxonomy_path: Path to output taxonomy directory.
   :param otl_reftax_src: Path to OTL reference-taxonomy tool('smasher')'s source code.
                          `Link to repo <https://github.com/OpenTreeOfLife/reference-taxonomy>`_

   :returns: Result status


