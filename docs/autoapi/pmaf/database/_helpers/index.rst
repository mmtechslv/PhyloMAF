:orphan:

:mod:`pmaf.database._helpers`
=============================

.. py:module:: pmaf.database._helpers


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.database._helpers.export_database_by_rid
   pmaf.database._helpers.ott_maker


.. function:: export_database_by_rid(database, output_fasta_fp, output_tax_fp, ids=None, chunksize=100)

   :param database:
   :param output_fasta_fp:
   :param output_tax_fp:
   :param ids: (Default value = None)
   :param chunksize: (Default value = 100)

   Returns:


.. function:: ott_maker(reference_taxonomy_path: str, new_taxonomy_path: str, otl_reftax_src: str) -> bool

   Reconstructs OpenTreeOfLife taxonomy by removing non-microbial life clades.

   :param reference_taxonomy_path: Path to reference taxonomy directory. `
                                   Download Latest OTT <https://tree.opentreeoflife.org/about/taxonomy-version>`_
                                   Run Make to compile OTT Jython files.
   :param new_taxonomy_path: Path to output taxonomy directory.
   :param otl_reftax_src: Path to OTL reference-taxonomy tool('smasher')'s source code.
                          `Link to repo <https://github.com/OpenTreeOfLife/reference-taxonomy>`_

   :returns: Result status


