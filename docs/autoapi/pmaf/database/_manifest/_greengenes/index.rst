:orphan:

:mod:`pmaf.database._manifest._greengenes`
==========================================

.. py:module:: pmaf.database._manifest._greengenes


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._manifest._greengenes.DatabaseGreengenes



.. py:class:: DatabaseGreengenes(*args, **kwargs)

   Bases: :class:`pmaf.database._core._tax_base.DatabaseTaxonomyMixin`, :class:`pmaf.database._core._seq_base.DatabaseSequenceMixin`, :class:`pmaf.database._core._phy_base.DatabasePhylogenyMixin`, :class:`pmaf.database._core._acs_base.DatabaseAccessionMixin`, :class:`pmaf.database._core._base.DatabaseBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: DATABASE_NAME
      :annotation: = Greengenes

      

   .. attribute:: INVALID_TAXA
      :annotation: = uncultured

      

   .. method:: build_database_storage(cls, storage_hdf5_fp, taxonomy_map_csv_fp, tree_newick_fp, sequence_fasta_fp, sequence_alignment_fasta_fp, stamp_dict, force=False, chunksize=500, **kwargs)
      :classmethod:

      :param storage_hdf5_fp:
      :param taxonomy_map_csv_fp:
      :param tree_newick_fp:
      :param sequence_fasta_fp:
      :param sequence_alignment_fasta_fp:
      :param stamp_dict:
      :param force: (Default value = False)
      :param chunksize: (Default value = 500)
      :param \*\*kwargs:

      Returns:


   .. method:: name(self)
      :property:



