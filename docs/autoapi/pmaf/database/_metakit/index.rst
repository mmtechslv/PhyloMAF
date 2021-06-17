:orphan:

:mod:`pmaf.database._metakit`
=============================

.. py:module:: pmaf.database._metakit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._metakit.DatabaseAccessionMetabase
   pmaf.database._metakit.DatabaseBackboneMetabase
   pmaf.database._metakit.DatabasePhylogenyMetabase
   pmaf.database._metakit.DatabaseSequenceMetabase
   pmaf.database._metakit.DatabaseTaxonomyMetabase



.. py:class:: DatabaseAccessionMetabase(storage_hdf5_fp, **kwargs)

   Bases: :class:`pmaf.database._metakit.DatabaseBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.database._metakit.DatabaseAccessionMetabase
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_accession_by_rid(self, ids, **kwargs)
      :abstractmethod:

      :param ids:
      :param \*\*kwargs:

      Returns:


   .. method:: get_accession_by_tid(self, ids, **kwargs)
      :abstractmethod:

      :param ids:
      :param \*\*kwargs:

      Returns:



.. py:class:: DatabaseBackboneMetabase(storage_hdf5_fp, **kwargs)

   Bases: :class:`abc.ABC`

   .. autoapi-inheritance-diagram:: pmaf.database._metakit.DatabaseBackboneMetabase
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: avail_ranks(self)
      :property:


   .. method:: build_database_storage(cls, **kwargs)
      :classmethod:
      :abstractmethod:

      :param \*\*kwargs:

      Returns:


   .. method:: close(self)
      :abstractmethod:


   .. method:: find_rid_by_tid(self, ids, subs, iterator, flatten, mode)
      :abstractmethod:

      :param ids:
      :param subs:
      :param iterator:
      :param flatten:
      :param mode:

      Returns:


   .. method:: find_sub_tids_by_tid(self, ids, ter_rank, flatten, mode)

      :param ids:
      :param ter_rank:
      :param flatten:
      :param mode:

      Returns:


   .. method:: find_tid_by_rid(self, ids, levels, flatten, method, mode)
      :abstractmethod:

      :param ids:
      :param levels:
      :param flatten:
      :param method:
      :param mode:

      Returns:


   .. method:: get_stats_by_rid(self, ids, include, exclude)
      :abstractmethod:

      :param ids:
      :param include:
      :param exclude:

      Returns:


   .. method:: get_stats_by_tid(self, ids, include, exclude)
      :abstractmethod:

      :param ids:
      :param include:
      :param exclude:

      Returns:


   .. method:: name(self)
      :property:


   .. method:: stamp(self)
      :property:


   .. method:: state(self)
      :property:


   .. method:: storage_manager(self)
      :property:


   .. method:: summary(self)
      :property:


   .. method:: take_rids_by_rank(self, levels, iterator, flatten, mode)
      :abstractmethod:

      :param levels:
      :param iterator:
      :param flatten:
      :param mode:

      Returns:


   .. method:: take_tids_by_rank(self, levels, iterator, flatten, mode)
      :abstractmethod:

      :param levels:
      :param iterator:
      :param flatten:
      :param mode:

      Returns:


   .. method:: xrid(self)
      :property:


   .. method:: xtid(self)
      :property:



.. py:class:: DatabasePhylogenyMetabase(storage_hdf5_fp, **kwargs)

   Bases: :class:`pmaf.database._metakit.DatabaseBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.database._metakit.DatabasePhylogenyMetabase
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: infer_topology_by_rid(self, ids)
      :abstractmethod:

      :param ids:

      Returns:


   .. method:: infer_topology_by_tid(self, ids)
      :abstractmethod:

      :param ids:

      Returns:


   .. method:: prune_tree_by_rid(self, ids)
      :abstractmethod:

      :param ids:

      Returns:


   .. method:: prune_tree_by_tid(self, ids)
      :abstractmethod:

      :param ids:

      Returns:



.. py:class:: DatabaseSequenceMetabase(storage_hdf5_fp, **kwargs)

   Bases: :class:`pmaf.database._metakit.DatabaseBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.database._metakit.DatabaseSequenceMetabase
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_alignment_by_rid(self, ids, **kwargs)
      :abstractmethod:

      :param ids:
      :param \*\*kwargs:

      Returns:


   .. method:: get_alignment_by_tid(self, ids, **kwargs)
      :abstractmethod:

      :param ids:
      :param \*\*kwargs:

      Returns:


   .. method:: get_sequence_by_rid(self, ids, **kwargs)
      :abstractmethod:

      :param ids:
      :param \*\*kwargs:

      Returns:


   .. method:: get_sequence_by_tid(self, ids, **kwargs)
      :abstractmethod:

      :param ids:
      :param \*\*kwargs:

      Returns:



.. py:class:: DatabaseTaxonomyMetabase(storage_hdf5_fp, **kwargs)

   Bases: :class:`pmaf.database._metakit.DatabaseBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.database._metakit.DatabaseTaxonomyMetabase
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_lineage_by_rid(self, ids, missing_rank, desired_ranks, drop_ranks)
      :abstractmethod:

      :param ids:
      :param missing_rank:
      :param desired_ranks:
      :param drop_ranks:

      Returns:


   .. method:: get_lineage_by_tid(self, ids, missing_rank, desired_ranks, drop_ranks)
      :abstractmethod:

      :param ids:
      :param missing_rank:
      :param desired_ranks:
      :param drop_ranks:

      Returns:


   .. method:: get_taxonomy_by_rank(self, levels)
      :abstractmethod:

      :param levels:

      Returns:


   .. method:: get_taxonomy_by_rid(self, ids, levels, result_format)
      :abstractmethod:

      :param ids:
      :param levels:
      :param result_format:

      Returns:


   .. method:: get_taxonomy_by_tid(self, ids, levels)
      :abstractmethod:

      :param ids:
      :param levels:

      Returns:



