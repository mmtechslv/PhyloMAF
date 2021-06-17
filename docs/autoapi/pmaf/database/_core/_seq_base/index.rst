:orphan:

:mod:`pmaf.database._core._seq_base`
====================================

.. py:module:: pmaf.database._core._seq_base


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._core._seq_base.DatabaseSequenceMixin



.. py:class:: DatabaseSequenceMixin(storage_hdf5_fp, **kwargs)

   Bases: :class:`pmaf.database._metakit.DatabaseSequenceMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_alignment_by_rid(self, ids=None, iterator=True, like='multiseq', chunksize=300)

      :param ids: (Default value = None)
      :param iterator: (Default value = True)
      :param like: (Default value = 'multiseq')
      :param chunksize: (Default value = 300)

      Returns:


   .. method:: get_alignment_by_tid(self, ids=None, subs=False, iterator=True, like='multiseq', chunksize=100)

      :param ids: (Default value = None)
      :param subs: (Default value = False)
      :param iterator: (Default value = True)
      :param like: (Default value = 'multiseq')
      :param chunksize: (Default value = 100)

      Returns:


   .. method:: get_sequence_by_rid(self, ids=None, iterator=True, like='multiseq', chunksize=100)

      :param ids: (Default value = None)
      :param iterator: (Default value = True)
      :param like: (Default value = 'multiseq')
      :param chunksize: (Default value = 100)

      Returns:


   .. method:: get_sequence_by_tid(self, ids=None, subs=False, iterator=True, like='multiseq', chunksize=100)

      :param ids: (Default value = None)
      :param subs: (Default value = False)
      :param iterator: (Default value = True)
      :param like: (Default value = 'multiseq')
      :param chunksize: (Default value = 100)

      Returns:



