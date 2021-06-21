:orphan:

:mod:`pmaf.phylo.tree._backends._ete3`
======================================

.. py:module:: pmaf.phylo.tree._backends._ete3


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.phylo.tree._backends._ete3.TreeEte3Base



.. py:class:: TreeEte3Base(tree, src='newick', copy=False)

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: add_str_node_names(self, map_dict, only_tips)

      :param map_dict:
      :param only_tips:

      Returns:


   .. method:: copy(self)


   .. method:: count(self)


   .. method:: detach_node(self, node)

      :param node:

      Returns:


   .. method:: engine(self)
      :property:


   .. method:: find_node_by_name(self, node_name)

      :param node_name:

      Returns:


   .. method:: get_ascii_art(self)


   .. method:: get_internal_nodes(self, names=False)

      :param names: (Default value = False)

      Returns:


   .. method:: get_mcra_node_for_nodes(self, nodes)

      :param nodes:

      Returns:


   .. method:: get_node_copy(node)
      :staticmethod:

      :param node:

      Returns:


   .. method:: get_nodes(self, names=False)

      :param names: (Default value = False)

      Returns:


   .. method:: get_string(self, tree_format=1, root_node=False, output_format='newick', quoted_nodes=False, **kwargs)

      :param tree_format: (Default value = 1)
      :param root_node: (Default value = False)
      :param output_format: (Default value = 'newick')
      :param quoted_nodes: (Default value = False)
      :param \*\*kwargs:

      Returns:


   .. method:: get_tips(self, names=False)

      :param names: (Default value = False)

      Returns:


   .. method:: ladderize(self)


   .. method:: make_tree_art(self, tree_art_file_path)

      :param tree_art_file_path:

      Returns:


   .. method:: name(self)
      :property:


   .. method:: prune_for_ids(self, node_ids)

      :param node_ids:

      Returns:


   .. method:: replace_node_names(self, map_dict, only_tips)

      :param map_dict:
      :param only_tips:

      Returns:


   .. method:: resolve_polytomy(self)


   .. method:: sort(self)


   .. method:: unroot(self)


   .. method:: write_newick(self, tree_fp, tree_format=1, root_node=False, output_format='newick', quoted_nodes=False, **kwargs)

      :param tree_fp:
      :param tree_format: (Default value = 1)
      :param root_node: (Default value = False)
      :param output_format: (Default value = 'newick')
      :param quoted_nodes: (Default value = False)
      :param \*\*kwargs:

      Returns:



