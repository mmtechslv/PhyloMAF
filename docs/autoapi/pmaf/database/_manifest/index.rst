:orphan:

:mod:`pmaf.database._manifest`
==============================

.. py:module:: pmaf.database._manifest


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._manifest.DatabaseGTDB
   pmaf.database._manifest.DatabaseGreengenes
   pmaf.database._manifest.DatabaseOTL
   pmaf.database._manifest.DatabaseSILVA
   pmaf.database._manifest.DatabaseUNITE



.. py:class:: DatabaseGTDB(*args, **kwargs)

   Bases: :class:`pmaf.database._core._tax_base.DatabaseTaxonomyMixin`, :class:`pmaf.database._core._seq_base.DatabaseSequenceMixin`, :class:`pmaf.database._core._phy_base.DatabasePhylogenyMixin`, :class:`pmaf.database._core._acs_base.DatabaseAccessionMixin`, :class:`pmaf.database._core._base.DatabaseBase`

   .. autoapi-inheritance-diagram:: pmaf.database._manifest.DatabaseGTDB
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: DATABASE_NAME
      :annotation: = GTDP

      

   .. attribute:: INVALID_TAXA
      

      

   .. method:: build_database_storage(cls, storage_hdf5_fp, taxonomy_map_csv_fp, tree_newick_fp, sequence_fasta_fp, metadata_csv_fp, stamp_dict, force=False, chunksize=500, **kwargs)
      :classmethod:

      :param storage_hdf5_fp:
      :param taxonomy_map_csv_fp:
      :param tree_newick_fp:
      :param sequence_fasta_fp:
      :param metadata_csv_fp:
      :param stamp_dict:
      :param force: (Default value = False)
      :param chunksize: (Default value = 500)
      :param \*\*kwargs:

      Returns:


   .. method:: name(self)
      :property:



.. py:class:: DatabaseGreengenes(*args, **kwargs)

   Bases: :class:`pmaf.database._core._tax_base.DatabaseTaxonomyMixin`, :class:`pmaf.database._core._seq_base.DatabaseSequenceMixin`, :class:`pmaf.database._core._phy_base.DatabasePhylogenyMixin`, :class:`pmaf.database._core._acs_base.DatabaseAccessionMixin`, :class:`pmaf.database._core._base.DatabaseBase`

   .. autoapi-inheritance-diagram:: pmaf.database._manifest.DatabaseGreengenes
      :parts: 1

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



.. py:class:: DatabaseOTL(*args, **kwargs)

   Bases: :class:`pmaf.database._core._tax_base.DatabaseTaxonomyMixin`, :class:`pmaf.database._core._phy_base.DatabasePhylogenyMixin`, :class:`pmaf.database._core._acs_base.DatabaseAccessionMixin`, :class:`pmaf.database._core._base.DatabaseBase`

   .. autoapi-inheritance-diagram:: pmaf.database._manifest.DatabaseOTL
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: DATABASE_NAME
      :annotation: = OpenTreeOfLife

      

   .. attribute:: INVALID_TAXA
      

      

   .. method:: build_database_storage(cls, storage_hdf5_fp, taxonomy_map_csv_fp, tree_newick_fp, stamp_dict, force=False, chunksize=500, delimiter='|', **kwargs)
      :classmethod:

      :param storage_hdf5_fp:
      :param taxonomy_map_csv_fp:
      :param tree_newick_fp:
      :param stamp_dict:
      :param force: (Default value = False)
      :param chunksize: (Default value = 500)
      :param delimiter: (Default value = '|')
      :param \*\*kwargs:

      Returns:


   .. method:: name(self)
      :property:



.. py:class:: DatabaseSILVA(*args, **kwargs)

   Bases: :class:`pmaf.database._core._tax_base.DatabaseTaxonomyMixin`, :class:`pmaf.database._core._seq_base.DatabaseSequenceMixin`, :class:`pmaf.database._core._phy_base.DatabasePhylogenyMixin`, :class:`pmaf.database._core._acs_base.DatabaseAccessionMixin`, :class:`pmaf.database._core._base.DatabaseBase`

   .. autoapi-inheritance-diagram:: pmaf.database._manifest.DatabaseSILVA
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: DATABASE_NAME
      :annotation: = SILVA

      

   .. attribute:: INVALID_TAXA
      :annotation: = ['unidentified', 'metagenome', 'uncultured']

      

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



.. py:class:: DatabaseUNITE(*args, **kwargs)

   Bases: :class:`pmaf.database._core._tax_base.DatabaseTaxonomyMixin`, :class:`pmaf.database._core._seq_base.DatabaseSequenceMixin`, :class:`pmaf.database._core._acs_base.DatabaseAccessionMixin`, :class:`pmaf.database._core._base.DatabaseBase`

   .. autoapi-inheritance-diagram:: pmaf.database._manifest.DatabaseUNITE
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

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



