:orphan:

:mod:`pmaf.database._manifest._unite`
=====================================

.. py:module:: pmaf.database._manifest._unite


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._manifest._unite.DatabaseUNITE



.. py:class:: DatabaseUNITE(*args, **kwargs)

   Bases: :class:`pmaf.database._core._tax_base.DatabaseTaxonomyMixin`, :class:`pmaf.database._core._seq_base.DatabaseSequenceMixin`, :class:`pmaf.database._core._acs_base.DatabaseAccessionMixin`, :class:`pmaf.database._core._base.DatabaseBase`

   .. attribute:: DATABASE_NAME
      :annotation: = UNITE

      

   .. attribute:: INVALID_TAXA
      :annotation: = unidentified

      

   .. method:: build_database_storage(cls, storage_hdf5_fp, taxonomy_map_csv_fp, sequence_fasta_fp, stamp_dict, force=False, chunksize=500, **kwargs)
      :classmethod:

      :param storage_hdf5_fp:
      :param taxonomy_map_csv_fp:
      :param sequence_fasta_fp:
      :param stamp_dict:
      :param force: (Default value = False)
      :param chunksize: (Default value = 500)
      :param \*\*kwargs:

      Returns:


   .. method:: name(self)
      :property:



