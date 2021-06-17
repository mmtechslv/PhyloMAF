:mod:`pmaf.phylo`
=================

.. py:module:: pmaf.phylo


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   branchest/index.rst
   builders/index.rst
   tree/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.phylo.BranchestERABLE
   pmaf.phylo.BranchestFastTree2
   pmaf.phylo.PhyloTree
   pmaf.phylo.TreeBuilderFastTree2



.. py:class:: BranchestERABLE(cache_dir=None)

   Bases: :class:`pmaf.phylo.branchest._metakit.BranchEstimatorBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.phylo.BranchestERABLE
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: estimate(self, alignment, tree, **kwargs)

      :param alignment:
      :param tree:
      :param \*\*kwargs:

      Returns:


   .. method:: last_error(self)
      :property:


   .. method:: last_out(self)
      :property:


   .. method:: last_rates(self)
      :property:



.. py:class:: BranchestFastTree2(cache_dir=None)

   Bases: :class:`pmaf.phylo.branchest._metakit.BranchEstimatorBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.phylo.BranchestFastTree2
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: estimate(self, alignment, tree, **kwargs)

      :param alignment:
      :param tree:
      :param \*\*kwargs:

      Returns:


   .. method:: last_error(self)
      :property:


   .. method:: last_out(self)
      :property:



.. py:class:: PhyloTree(tree, tree_format='newick', copy=False)

   Bases: :class:`pmaf.phylo.tree._metakit.PhyloTreeMetabase`

   .. autoapi-inheritance-diagram:: pmaf.phylo.PhyloTree
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: annotate_nodes_by_map(self, node_mapping, only_tips=False)

      :param node_mapping:
      :param only_tips: (Default value = False)

      Returns:


   .. method:: clear_internal_node_names(self)


   .. method:: copy(self)


   .. method:: get_ascii_art(self)


   .. method:: get_mcra_for_nodes(self, node_names)

      :param node_names:

      Returns:


   .. method:: get_newick_str(self, **kwargs)

      :param \*\*kwargs:

      Returns:


   .. method:: get_node_by_name(self, node_name)

      :param node_name:

      Returns:


   .. method:: internal_node_names(self)
      :property:


   .. method:: internal_nodes(self)
      :property:


   .. method:: ladderize(self)


   .. method:: merge_nodes(self, tip_names)

      :param tip_names:

      Returns:


   .. method:: node_names(self)
      :property:


   .. method:: nodes(self)
      :property:


   .. method:: prune_by_ids(self, node_ids)

      :param node_ids:

      Returns:


   .. method:: remove_node(self, node)

      :param node:

      Returns:


   .. method:: remove_node_by_name(self, node_name)

      :param node_name:

      Returns:


   .. method:: render(self, output_fp)

      :param output_fp:

      Returns:


   .. method:: replace_nodes_by_map(self, node_mapping, only_tips=False)

      :param node_mapping:
      :param only_tips: (Default value = False)

      Returns:


   .. method:: resolve_polytomy(self)


   .. method:: sort_by_name(self)


   .. method:: tip_names(self)
      :property:


   .. method:: tips(self)
      :property:


   .. method:: to_skbio(self, rooted=False)

      :param rooted: (Default value = False)

      Returns:


   .. method:: total_internal_nodes(self)
      :property:


   .. method:: total_nodes(self)
      :property:


   .. method:: total_tips(self)
      :property:


   .. method:: unroot(self)


   .. method:: write(self, tree_fp, **kwargs)

      :param tree_fp:
      :param \*\*kwargs:

      Returns:



.. py:class:: TreeBuilderFastTree2(cache_dir=None)

   Bases: :class:`pmaf.phylo.builders._metakit.TreeBuilderBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.phylo.TreeBuilderFastTree2
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: build(self, alignment, **kwargs)

      :param alignment:
      :param \*\*kwargs:

      Returns:


   .. method:: last_error(self)
      :property:


   .. method:: last_out(self)
      :property:



