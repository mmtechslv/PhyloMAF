:orphan:

:mod:`pmaf.phylo.branchest.fasttree2._fasttree2`
================================================

.. py:module:: pmaf.phylo.branchest.fasttree2._fasttree2


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.phylo.branchest.fasttree2._fasttree2.BranchestFastTree2



.. py:class:: BranchestFastTree2(bin_fp: Optional[str] = 'fasttree', cache_dir: Optional[str] = None)

   Bases: :class:`pmaf.phylo.branchest._metakit.BranchEstimatorBackboneMetabase`

   Branch estimator for phylogenetic trees.

   FastTree infers approximately-maximum-likelihood phylogenetic trees from alignments of nucleotide or protein sequences. :cite:`priceFastTreeApproximatelyMaximumLikelihood2010`

   :param bin_fp: Path to 'fasttree' executable or None for default.
   :param cache_dir: Cache directory to use or None for seamless caching.

   .. method:: estimate(self, alignment: MultiSequenceMetabase, tree: PhyloTree, **kwargs: Any) -> PhyloTree

      Estimate branches of on fixed tree topology(param `tree`) using MSA of representative sequences(param `alignment`)

      :param alignment: MSA alignment of representative sequences
      :param tree: Phylogenetic tree topology.
      :param \*\*kwargs: Compatibility

      :returns: Phylogenetic tree with estimated branches


   .. method:: last_error(self)
      :property:

      Latest Error


   .. method:: last_out(self)
      :property:

      Latest Output



