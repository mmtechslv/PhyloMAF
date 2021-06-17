:orphan:

:mod:`pmaf.database._core._phy_base`
====================================

.. py:module:: pmaf.database._core._phy_base


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._core._phy_base.DatabasePhylogenyMixin



.. py:class:: DatabasePhylogenyMixin(storage_hdf5_fp, **kwargs)

   Bases: :class:`pmaf.database._metakit.DatabasePhylogenyMetabase`

   .. autoapi-inheritance-diagram:: pmaf.database._core._phy_base.DatabasePhylogenyMixin
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: infer_topology_by_rid(self, ids)

      :param ids:

      Returns:


   .. method:: infer_topology_by_tid(self, ids, subreps=False, include_rid=False)

      Rapidly infers topology from map-tree.

      :param ids: Tips to infer for.
      :param subreps: (Default value = False)
      :param include_rid: (Default value = False)

      Returns:


   .. method:: prune_tree_by_rid(self, ids)

      :param ids:

      Returns:


   .. method:: prune_tree_by_tid(self, ids, subreps=False, include_rid=False)

      :param ids:
      :param subreps: (Default value = False)
      :param include_rid: (Default value = False)

      Returns:



