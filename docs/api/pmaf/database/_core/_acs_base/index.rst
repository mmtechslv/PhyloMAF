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

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_accession_by_rid(self, ids=None, iterator=False)

      :param ids: (Default value = None)
      :param iterator: (Default value = False)

      Returns:


   .. method:: get_accession_by_tid(self, ids: Optional[AnyGenericIdentifier] = None, subs: bool = False, iterator: bool = True) -> Union[Dict[GenericIdentifier, Dict[str, str]], Generator[Tuple[GenericIdentifier, Dict[str, str]], None, None]]

      Get accession numbers from the database.

      :param ids: Target :term:`tids`. Use None for all :term:`tids`
      :param subs: If True :term:`subs` will be included. Default is False.
      :param iterator: If True return a generator object. Default is True.

      :returns: Returns a :class:`Generator` that yields (:term:`tid<tids>`, dict)
                if `iterator` is False: Returns a dictionary where keys are :term:`tid<tids>` and values are dict with accession numbers.
      :rtype: If `iterator` is True



