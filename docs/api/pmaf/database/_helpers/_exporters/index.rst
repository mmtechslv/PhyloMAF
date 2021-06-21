:orphan:

:mod:`pmaf.database._helpers._exporters`
========================================

.. py:module:: pmaf.database._helpers._exporters


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._helpers._exporters.ExportableDatabase



Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.database._helpers._exporters.export_database_by_rid


.. py:class:: ExportableDatabase(storage_hdf5_fp, **kwargs)

   Bases: :class:`pmaf.database._core._tax_base.DatabaseTaxonomyMixin`, :class:`pmaf.database._core._seq_base.DatabaseSequenceMixin`, :class:`pmaf.database._core._base.DatabaseBase`

   Dummy Class that represent two exportable mixins.

   Initialize self.  See help(type(self)) for accurate signature.


.. function:: export_database_by_rid(database: ExportableDatabase, output_fasta_fp: str, output_tax_fp: str, ids: Optional[AnyGenericIdentifier] = None, chunksize: int = 100)

   Export database into QIIME formatted files.

   :param database: Database to extract data from.
   :param output_fasta_fp: Path to output FASTA file
   :param output_tax_fp: Path to output taxonomy file (QIIME/Greengenes notation)
   :param ids: Reference identifiers to extract. Default is None to extract all.
   :param chunksize: Process data in chunks. Default is 100 records per chunk.


