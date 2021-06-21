:mod:`pmaf.phylo.branchest`
===========================

.. py:module:: pmaf.phylo.branchest


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   erable/index.rst
   fasttree2/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.phylo.branchest.BranchestERABLE
   pmaf.phylo.branchest.BranchestFastTree2



.. py:class:: BranchestERABLE(bin_fp: Optional[str] = 'erable', cache_dir: Optional[str] = None)

   Bases: :class:`pmaf.phylo.branchest._metakit.BranchEstimatorBackboneMetabase`

   Branch estimator for phylogenetic trees.

   ERaBLE phylogenetic tree estimator on fixed tree topology. :cite:t:`binetFastAccurateBranch2016`

   :param bin_fp: Path to 'erable' executable or None for default.
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

      Lastest Output


   .. method:: last_rates(self)
      :property:

      Latest Rates Product



.. py:class:: BranchestFastTree2(bin_fp: Optional[str] = 'fasttree', cache_dir: Optional[str] = None)

   Bases: :class:`pmaf.phylo.branchest._metakit.BranchEstimatorBackboneMetabase`

   Branch estimator for phylogenetic trees.

   FastTree infers approximately-maximum-likelihood phylogenetic trees from alignments of nucleotide or protein sequences. :cite:t:`priceFastTreeApproximatelyMaximumLikelihood2010`

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



