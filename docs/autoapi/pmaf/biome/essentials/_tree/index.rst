:orphan:

:mod:`pmaf.biome.essentials._tree`
==================================

.. py:module:: pmaf.biome.essentials._tree


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.essentials._tree.RepPhylogeny



.. py:class:: RepPhylogeny(tree: Union[PhyloTree, TreeEte3Base, StringIO, str], feature_ids: Optional[GenericIdentifier] = None, prune: bool = False, annotation: Union[dict, pd.Series, None] = None, copy: bool = True, ignore_polytomy: bool = False, **kwargs: Any)

   Bases: :class:`pmaf.biome.essentials._base.EssentialBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialFeatureMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.essentials._tree.RepPhylogeny
      :parts: 1

   An `essential` class for handling phylogeny data.

   Constructor for :class:`.RepPhylogeny`

   :param tree: Phylogeny data
   :param feature_ids: Target feature identifiers
   :param prune: Whether to prune for `feature_ids`
   :param annotation: Annotations for tips
   :param copy: Whether to copy the original tree.
                May require long time if tree is large.
   :param ignore_polytomy: Whether to resolve tree polytomy or not.
   :param \*\*kwargs: Compatibility

   .. method:: annotations(self) -> dict
      :property:

      Tip Annotations


   .. method:: copy(self) -> 'RepPhylogeny'

      Copy of the instance.


   .. method:: data(self) -> PhyloTree
      :property:

      Phylogenetic Tree


   .. method:: export(self, output_fp: str, _add_ext: bool = False, **kwargs: Any) -> None

      Exports the Newick formatted phylogenetic tree into specified file.

      :param output_fp: Export filepath
      :param _add_ext: Add file extension or not.
      :param \*\*kwargs: Compatibility


   .. method:: get_annotated_tree(self) -> PhyloTree

      Retrieves annotated tree

      :returns: Annotated tree of class :class:`~pmaf.phylo.tree.PhyloTree`


   .. method:: get_ascii_art(self, annotated: bool = False) -> str

      Creates ASCII art of the tree.

      :param annotated: Whether to create tree with annotated tips or not.

      :returns: String with ASCII art


   .. method:: get_subset(self, rids: Optional[GenericIdentifier] = None, *args, **kwargs: Any) -> 'RepPhylogeny'

      Get subset of the :class:`.RepPhylogeny`.

      :param rids: Feature Identifiers
      :param \*args: Compatibility
      :param \*\*kwargs: Compatibility

      :returns: Instance of :class:`.RepPhylogeny`.


   .. method:: render_art(self, output_fp: str, annotated: bool = False) -> Any

      Renders tree into file.

      :param output_fp: File to render into. File format depends on the extension.
                        For example, .pdf will produce PDF file and
                        while .png will produce PNG file.
      :param annotated: Whether to create tree with annotated tips or not.


   .. method:: resolve_polytomy(self) -> None

      Resolve tree polytomy.


   .. method:: write(self, output_fp: str, mode: str = 'w', **kwargs: Any) -> None

      Writes the Newick tree into specified file.

      :param output_fp: Output filepath
      :param mode: File write mode.
      :param \*\*kwargs: Compatibility


   .. method:: xrid(self) -> GenericIdentifier
      :property:

      Feature identifiers



