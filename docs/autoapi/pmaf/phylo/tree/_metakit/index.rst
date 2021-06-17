:orphan:

:mod:`pmaf.phylo.tree._metakit`
===============================

.. py:module:: pmaf.phylo.tree._metakit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.phylo.tree._metakit.PhyloTreeMetabase



.. py:class:: PhyloTreeMetabase

   Bases: :class:`abc.ABC`

   .. autoapi-inheritance-diagram:: pmaf.phylo.tree._metakit.PhyloTreeMetabase
      :parts: 1

   .. method:: annotate_nodes_by_map(self, node_mapping, only_tips)
      :abstractmethod:

      :param node_mapping:
      :param only_tips:

      Returns:


   .. method:: copy(self)
      :abstractmethod:


   .. method:: get_ascii_art(self)
      :abstractmethod:


   .. method:: internal_node_names(self)
      :property:


   .. method:: internal_nodes(self)
      :property:


   .. method:: node_names(self)
      :property:


   .. method:: nodes(self)
      :property:


   .. method:: prune_by_ids(self, ids)
      :abstractmethod:

      :param ids:

      Returns:


   .. method:: render(self, output_fp)
      :abstractmethod:

      :param output_fp:

      Returns:


   .. method:: replace_nodes_by_map(self, node_mapping, only_tips)
      :abstractmethod:

      :param node_mapping:
      :param only_tips:

      Returns:


   .. method:: sort_by_name(self)
      :abstractmethod:


   .. method:: tip_names(self)
      :property:


   .. method:: tips(self)
      :property:


   .. method:: total_internal_nodes(self)
      :property:


   .. method:: total_nodes(self)
      :property:


   .. method:: total_tips(self)
      :property:


   .. method:: unroot(self)
      :abstractmethod:


   .. method:: write(self, tree_fp, tree_format, root_node, output_format)
      :abstractmethod:

      :param tree_fp:
      :param tree_format:
      :param root_node:
      :param output_format:

      Returns:



