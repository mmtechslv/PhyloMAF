:orphan:

:mod:`pmaf.database._shared._assemblers`
========================================

.. py:module:: pmaf.database._shared._assemblers


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.database._shared._assemblers.finalize_storage_construction
   pmaf.database._shared._assemblers.make_column_details
   pmaf.database._shared._assemblers.make_interxmaps
   pmaf.database._shared._assemblers.make_repseq_map_generator
   pmaf.database._shared._assemblers.make_rid_index_mapper
   pmaf.database._shared._assemblers.make_tree_map
   pmaf.database._shared._assemblers.produce_rep_stats
   pmaf.database._shared._assemblers.produce_tax_stats
   pmaf.database._shared._assemblers.rebuild_phylo
   pmaf.database._shared._assemblers.reconstruct_taxonomy
   pmaf.database._shared._assemblers.reindex_frame
   pmaf.database._shared._assemblers.reparse_tree


.. function:: finalize_storage_construction(storage_manager, stamp_data, prior_recap, **kwargs)

   :param storage_manager:
   :param stamp_data:
   :param prior_recap:
   :param \*\*kwargs:

   Returns:


.. function:: make_column_details(storage_manager)

   :param storage_manager:

   Returns:


.. function:: make_interxmaps(storage_manager)

   :param storage_manager:

   Returns:


.. function:: make_repseq_map_generator(transformation_details, chunksize=500)

   :param transformation_details:
   :param chunksize: (Default value = 500)

   Returns:


.. function:: make_rid_index_mapper(rids_index)

   :param rids_index:

   Returns:


.. function:: make_tree_map(tree_object)

   :param tree_object:

   Returns:


.. function:: produce_rep_stats(storage_manager, chunksize)

   :param storage_manager:
   :param chunksize:

   Returns:


.. function:: produce_tax_stats(storage_manager, novel_tids)

   :param storage_manager:
   :param novel_tids:

   Returns:


.. function:: rebuild_phylo(tree_object)

   :param tree_object:

   Returns:


.. function:: reconstruct_taxonomy(master_taxonomy_sheet_df, index_mapper, reject_taxa=None)

   :param master_taxonomy_sheet_df:
   :param index_mapper:
   :param reject_taxa: (Default value = None)

   Returns:


.. function:: reindex_frame(target_df, index_mapper)

   :param target_df:
   :param index_mapper:

   Returns:


.. function:: reparse_tree(tree_object, index_mapper)

   :param tree_object:
   :param index_mapper:

   Returns:


