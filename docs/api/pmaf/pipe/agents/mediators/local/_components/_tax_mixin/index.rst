:orphan:

:mod:`pmaf.pipe.agents.mediators.local._components._tax_mixin`
==============================================================

.. py:module:: pmaf.pipe.agents.mediators.local._components._tax_mixin


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.mediators.local._components._tax_mixin.MediatorLocalTaxonomyMixin



.. py:class:: MediatorLocalTaxonomyMixin(database, tax_rank_tolerance=None, tax_corr_method='lineage', tax_fuzzy_cutoff=95, tax_fuzzy_mode=False, tax_format=None, tax_refrep='tid', **kwargs)

   Bases: :class:`pmaf.pipe.agents.mediators.local._base.MediatorLocalBase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorTaxonomyMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: CORRELATION_METHODS
      :annotation: = ['lineage', 'complement', 'taxon']

      

   .. method:: get_identifier_by_taxonomy(self, docker, factor, **kwargs)

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_taxonomy_by_identifier(self, docker, factor, **kwargs)

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:



