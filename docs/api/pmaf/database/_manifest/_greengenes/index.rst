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



