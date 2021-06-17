:orphan:

:mod:`pmaf.database._core._tax_base`
====================================

.. py:module:: pmaf.database._core._tax_base


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._core._tax_base.DatabaseTaxonomyMixin



.. py:class:: DatabaseTaxonomyMixin(storage_hdf5_fp, **kwargs)

   Bases: :class:`pmaf.database._metakit.DatabaseTaxonomyMetabase`

   .. autoapi-inheritance-diagram:: pmaf.database._core._tax_base.DatabaseTaxonomyMixin
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_lineage_by_rid(self, ids=None, missing_rank=False, desired_ranks=False, drop_ranks=False)

      Generates lineages for taxon ids

      :param ids: (Default value = None)
      :param missing_rank: (Default value = False)
      :param desired_ranks: (Default value = False)
      :param drop_ranks: (Default value = False)

      Returns:


   .. method:: get_lineage_by_tid(self, ids=None, missing_rank=False, desired_ranks=False, drop_ranks=False)

      Generates lineages for taxon ids

      :param ids: (Default value = None)
      :param missing_rank: (Default value = False)
      :param desired_ranks: (Default value = False)
      :param drop_ranks: (Default value = False)

      Returns:


   .. method:: get_taxonomy_by_rank(self, levels)

      :param level:
      :param ids:
      :param levels:

      Returns:


   .. method:: get_taxonomy_by_rid(self, ids=None, levels=None, tax_format=None)

      Return taxonomy dataframe for given TaxonIDs or all if id=None

      :param ids: List of TaxonIDs or None (Default value = None)
      :param levels: Default value
      :param tax_format: Default value

      Returns:



   .. method:: get_taxonomy_by_tid(self, ids=None, levels=None)

      Return taxonomy dataframe for given TaxonIDs or all if id=None

      :param ids: List of TaxonIDs or None (Default value = None)
      :param levels: Default value

      Returns:




