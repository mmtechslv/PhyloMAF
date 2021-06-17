:orphan:

:mod:`pmaf.database._core._acs_base`
====================================

.. py:module:: pmaf.database._core._acs_base


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._core._acs_base.DatabaseAccessionMixin



.. py:class:: DatabaseAccessionMixin(storage_hdf5_fp, **kwargs)

   Bases: :class:`pmaf.database._metakit.DatabaseAccessionMetabase`

   .. autoapi-inheritance-diagram:: pmaf.database._core._acs_base.DatabaseAccessionMixin
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_accession_by_rid(self, ids=None, iterator=False)

      :param ids: (Default value = None)
      :param iterator: (Default value = False)

      Returns:


   .. method:: get_accession_by_tid(self, ids=None, subs=False, iterator=True)

      :param ids: (Default value = None)
      :param subs: (Default value = False)
      :param iterator: (Default value = True)

      Returns:



