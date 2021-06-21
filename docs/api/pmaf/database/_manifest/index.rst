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

   Database class for Greengenes database :cite:t:`mcdonaldImprovedGreengenesTaxonomy2012a`

   .. attribute:: DATABASE_NAME
      :annotation: = Greengenes

      

   .. attribute:: INVALID_TAXA
      :annotation: = uncultured

      

   .. method:: build_database_storage(cls, storage_hdf5_fp: str, taxonomy_map_csv_fp: str, tree_newick_fp: str, sequence_fasta_fp: str, sequence_alignment_fasta_fp: str, stamp_dict: dict, force: bool = False, chunksize: int = 500, **kwargs: Any) -> None
      :classmethod:

      Factory method to build new database `HDF5 <https://www.hdfgroup.org/solutions/hdf5/>`_ file.

      :param storage_hdf5_fp: Output path for `HDF5 <https://www.hdfgroup.org/solutions/hdf5/>`_ file
      :param taxonomy_map_csv_fp: Path to taxonomy file
      :param tree_newick_fp: Path to Newick tree file
      :param sequence_fasta_fp: Path to FASTA sequences file
      :param sequence_alignment_fasta_fp: Path to FASTA alignment file
      :param stamp_dict: Dictionary with metadata that will be stamped to the database
      :param force: Force output file overwrite
      :param chunksize: Sequence/Alignment data processing chunk size. Longer chunks are
                        faster to process but require more memory.
      :param \*\*kwargs: Compatibility.

      :returns: None if file was created successfully.


   .. method:: name(self) -> str
      :property:

      Database name/label



.. py:class:: DatabaseOTL(*args, **kwargs)

   Bases: :class:`pmaf.database._core._tax_base.DatabaseTaxonomyMixin`, :class:`pmaf.database._core._phy_base.DatabasePhylogenyMixin`, :class:`pmaf.database._core._acs_base.DatabaseAccessionMixin`, :class:`pmaf.database._core._base.DatabaseBase`

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



