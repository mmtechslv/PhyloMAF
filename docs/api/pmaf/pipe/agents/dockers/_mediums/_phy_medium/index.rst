:orphan:

:mod:`pmaf.pipe.agents.dockers._mediums._phy_medium`
====================================================

.. py:module:: pmaf.pipe.agents.dockers._mediums._phy_medium


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.dockers._mediums._phy_medium.DockerPhylogenyMedium



.. py:class:: DockerPhylogenyMedium(trees, ignore_tips=False, **kwargs)

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerPhylogenyMetabase`, :class:`pmaf.pipe.agents.dockers._base.DockerBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_node_names(self, indices=None, dtype=None, include_missing=False)

      :param indices: (Default value = None)
      :param dtype: (Default value = None)
      :param include_missing: (Default value = False)

      Returns:


   .. method:: get_tip_names(self, indices=None, dtype=None)

      :param indices: (Default value = None)
      :param dtype: (Default value = None)

      Returns:


   .. method:: get_tree(self, indices=None, exclude_missing=False)

      :param indices: (Default value = None)
      :param exclude_missing: (Default value = False)

      Returns:



