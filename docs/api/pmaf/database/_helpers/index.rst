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


.. function:: export_database_by_rid(database: ExportableDatabase, output_fasta_fp: str, output_tax_fp: str, ids: Optional[AnyGenericIdentifier] = None, chunksize: int = 100)

   Export database into QIIME formatted files.

   :param database: Database to extract data from.
   :param output_fasta_fp: Path to output FASTA file
   :param output_tax_fp: Path to output taxonomy file (QIIME/Greengenes notation)
   :param ids: Reference identifiers to extract. Default is None to extract all.
   :param chunksize: Process data in chunks. Default is 100 records per chunk.


.. function:: ott_maker(reftax_path: str, newtax_path: str, reftax_src_path: str) -> bool

   Reconstructs OpenTreeOfLife taxonomy by removing non-microbial life clades.

   :param reftax_path: Path to reference taxonomy directory.
                       `Download Latest OTT <https://tree.opentreeoflife.org/about/taxonomy-version>`_
                       Run Make to compile OTT Jython files.
   :param newtax_path: Path to output taxonomy directory.
   :param reftax_src_path: Path to OTL reference-taxonomy tool('smasher')'s source code.
                           `Link to repo <https://github.com/OpenTreeOfLife/reference-taxonomy>`_

   :returns: Result status


