:mod:`pmaf.database`
====================

.. py:module:: pmaf.database


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database.DatabaseGTDB
   pmaf.database.DatabaseGreengenes
   pmaf.database.DatabaseOTL
   pmaf.database.DatabaseSILVA
   pmaf.database.DatabaseStorageManager
   pmaf.database.DatabaseUNITE



Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.database.export_database_by_rid
   pmaf.database.ott_maker


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



.. py:class:: DatabaseStorageManager(hdf5_filepath, storage_name, force_new=False)

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: active_elements(self)
      :property:


   .. method:: commit_to_storage(self, element_key, product_generator)

      This is a primary function that commit changes to the storage.

      :param element_key: element key to which product product must be put.
      :param product_generator: Primary generator that yields output that can be put into storage element.
      :param product_generator: Primary generator that yields output that can be put into storage element.

      All product generators and must follow following output rules.
        For `sequence-master` and `sequence-aligned`: Generator must first yield `product_inits`, `product_generator_first_chunk`. `product_inits` contain data such as `expectedrows` or `min_itemsize`, which are required if product processes file in chunks.
      Next generator must yield `product_product_chunk`
        For all others: Generator must first yield `product_inits`, `None`
      Next generator must yield `product_product`
        Note: Not all product generators are processed same way. For more details, view product documentation.

      :returns: Last result from generator if success. Otherwise RuntimeError is raised.


   .. method:: compress_storage(self, complevel=9, complib='blosc', overwrite=False)

      :param complevel: (Default value = 9)
      :param complib: (Default value = 'blosc')
      :param overwrite: (Default value = False)

      Returns:


   .. method:: element_state(self)
      :property:


   .. method:: get_element_data_by_ids(self, element_key, ids)

      :param element_key:
      :param ids:

      Returns:


   .. method:: get_index_by_element(self, element_key, condition=None)

      :param element_key:
      :param condition: (Default value = None)

      Returns:


   .. method:: has_accs(self)
      :property:


   .. method:: has_align(self)
      :property:


   .. method:: has_repseq(self)
      :property:


   .. method:: has_tax(self)
      :property:


   .. method:: has_tree(self)
      :property:


   .. method:: hdf5_filepath(self)
      :property:


   .. method:: imprint_database(self, stamp_dict)

      This is the final function that user local constructor must call. This function will add signature to the local and will lock it so that no changes can be performed.
      Locking is performed only stamp presence check via storage manager.

      :param stamp_dict:

      Returns:


   .. method:: initiate_memory_cache(self, level=1)

      Load various elements based on `level` from storage to the memory for rapid data access.

      :param level: Level of data caching.

      Levels:
      - Level 1: Only loads inter index map to the memory. # Run by default
      - Level 2: Additionally load taxonomy-sheet to the memory
      - Level 3: Additionally load all map-elements to the memory
      - Level 4: Additionally load all tree-instance to the memory

      :returns: True level until which data was cached.


   .. method:: repseq_ids(self)
      :property:


   .. method:: retrieve_data_by_element(self, element_key, columns=None, chunksize=None)

      :param element_key:
      :param columns: (Default value = None)
      :param chunksize: (Default value = None)

      Returns:


   .. method:: shutdown(self)


   .. method:: state(self)
      :property:


   .. method:: storage_name(self)
      :property:


   .. method:: summary(self)
      :property:


   .. method:: taxon_ids(self)
      :property:


   .. method:: validate_storage(hdf5_filepath, storage_name)
      :staticmethod:

      :param hdf5_filepath:
      :param storage_name:

      Returns:



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


