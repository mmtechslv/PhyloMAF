:mod:`pmaf.phylo.builders.fasttree2`
====================================

.. py:module:: pmaf.phylo.builders.fasttree2


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.phylo.builders.fasttree2.TreeBuilderFastTree2



.. py:class:: TreeBuilderFastTree2(bin_fp: Optional[str] = 'fasttree', cache_dir: Optional[str] = None)

   Bases: :class:`pmaf.phylo.builders._metakit.TreeBuilderBackboneMetabase`

   Phylogenetic *de-novo* tree builder

   FastTree infers approximately-maximum-likelihood phylogenetic trees from alignments of nucleotide or protein sequences. :cite:`priceFastTreeApproximatelyMaximumLikelihood2010`

   :param bin_fp: Path to 'fasttree' executable or None for default.
   :param cache_dir: Cache directory to use or None for seamless caching.

   .. method:: build(self, alignment: MultiSequenceMetabase, **kwargs: Any) -> PhyloTree

      Constructs a *de-novo* phylogenetic tree from MSA(param `alignment`).

      :param alignment: MSA alignment of representative sequences
      :param \*\*kwargs: Compatibility

      :returns: Phylogenetic tree with estimated branches


   .. method:: last_error(self)
      :property:

      Latest Error


   .. method:: last_out(self)
      :property:

      Latest Output



