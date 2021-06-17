:orphan:

:mod:`pmaf.database._manifest._otl`
===================================

.. py:module:: pmaf.database._manifest._otl


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.database._manifest._otl.DatabaseOTL



.. py:class:: DatabaseOTL(*args, **kwargs)

   Bases: :class:`pmaf.database._core._tax_base.DatabaseTaxonomyMixin`, :class:`pmaf.database._core._phy_base.DatabasePhylogenyMixin`, :class:`pmaf.database._core._acs_base.DatabaseAccessionMixin`, :class:`pmaf.database._core._base.DatabaseBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: DATABASE_NAME
      :annotation: = OpenTreeOfLife

      

   .. attribute:: INVALID_TAXA
      

      

   .. method:: build_database_storage(cls, storage_hdf5_fp, taxonomy_map_csv_fp, tree_newick_fp, stamp_dict, force=False, chunksize=500, delimiter='|', **kwargs)
      :classmethod:

      :param storage_hdf5_fp:
      :param taxonomy_map_csv_fp:
      :param tree_newick_fp:
      :param stamp_dict:
      :param force: (Default value = False)
      :param chunksize: (Default value = 500)
      :param delimiter: (Default value = '|')
      :param \*\*kwargs:

      Returns:


   .. method:: name(self)
      :property:



