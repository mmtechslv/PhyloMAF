:orphan:

:mod:`pmaf.database._core._base`
================================

.. py:module:: pmaf.database._core._base


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._core._base.DatabaseBase



.. py:class:: DatabaseBase(storage_hdf5_fp)

   Bases: :class:`pmaf.database._metakit.DatabaseBackboneMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: avail_ranks(self)
      :property:


   .. method:: close(self)

      Closes local client by shutting down storage manager.


   .. method:: find_rid_by_tid(self, ids=None, subs=False, iterator=False, flatten=False, mode='frame')

      :param ids: (Default value = None)
      :param subs: (Default value = False)
      :param iterator: (Default value = False)
      :param flatten: (Default value = False)
      :param mode: (Default value = 'frame')

      Returns:


   .. method:: find_sub_tids_by_tid(self, ids=None, ter_rank=None, flatten=False, mode='frame')

      :param ids: (Default value = None)
      :param ter_rank: (Default value = None)
      :param flatten: (Default value = False)
      :param mode: (Default value = 'frame')

      Returns:


   .. method:: find_tid_by_rid(self, ids=None, levels=None, flatten=False, method='legal', mode='frame')

      :param ids: (Default value = None)
      :param levels: (Default value = None)
      :param flatten: (Default value = False)
      :param method: (Default value = 'legal')
      :param mode: (Default value = 'frame')

      Returns:


   .. method:: get_stats_by_rid(self, ids=None, include=None, exclude=None)

      :param ids: (Default value = None)
      :param include: (Default value = None)
      :param exclude: (Default value = None)

      Returns:


   .. method:: get_stats_by_tid(self, ids=None, include=None, exclude=None)

      :param ids: (Default value = None)
      :param include: (Default value = None)
      :param exclude: (Default value = None)

      Returns:


   .. method:: novel_tids(self)
      :property:


   .. method:: stamp(self)
      :property:


   .. method:: state(self)
      :property:


   .. method:: storage_manager(self)
      :property:


   .. method:: summary(self)
      :property:


   .. method:: take_rids_by_rank(self, levels=None, iterator=False, flatten=False, mode='dict')

      :param levels: (Default value = None)
      :param iterator: (Default value = False)
      :param flatten: (Default value = False)
      :param mode: (Default value = 'dict')

      Returns:


   .. method:: take_tids_by_rank(self, levels=None, iterator=False, flatten=False, mode='dict')

      :param levels: (Default value = None)
      :param iterator: (Default value = False)
      :param flatten: (Default value = False)
      :param mode: (Default value = 'dict')

      Returns:


   .. method:: xrid(self)
      :property:


   .. method:: xtid(self)
      :property:



