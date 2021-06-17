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



.. py:class:: BranchestERABLE(cache_dir=None)

   Bases: :class:`pmaf.phylo.branchest._metakit.BranchEstimatorBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.phylo.branchest.BranchestERABLE
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

   .. autoapi-inheritance-diagram:: pmaf.phylo.branchest.BranchestFastTree2
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



