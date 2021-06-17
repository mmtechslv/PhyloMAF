:orphan:

:mod:`pmaf.pipe.agents.mediators.local._components`
===================================================

.. py:module:: pmaf.pipe.agents.mediators.local._components


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.mediators.local._components.MediatorLocalAccessionMixin
   pmaf.pipe.agents.mediators.local._components.MediatorLocalPhylogenyMixin
   pmaf.pipe.agents.mediators.local._components.MediatorLocalSequenceMixin
   pmaf.pipe.agents.mediators.local._components.MediatorLocalTaxonomyMixin



.. py:class:: MediatorLocalAccessionMixin(database, acs_refrep='tid', acs_sub_nodes=False, acs_filter_method=None, acs_filter_value=None, **kwargs)

   Bases: :class:`pmaf.pipe.agents.mediators.local._base.MediatorLocalBase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorAccessionMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.mediators.local._components.MediatorLocalAccessionMixin
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: ACS_FILTER_METHODS
      :annotation: = ['random', 'first']

      

   .. method:: get_accession_by_identifier(self, docker, factor, **kwargs)

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_identifier_by_accession(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:



.. py:class:: MediatorLocalPhylogenyMixin(database, phy_method='infer', phy_sub_nodes=True, phy_ignore_tips=False, phy_refrep='tid', **kwargs)

   Bases: :class:`pmaf.pipe.agents.mediators.local._base.MediatorLocalBase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorPhylogenyMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.mediators.local._components.MediatorLocalPhylogenyMixin
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: PHYLO_EXTRACT_METHODS
      :annotation: = ['infer', 'prune']

      

   .. method:: get_identifier_by_phylogeny(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_phylogeny_by_identifier(self, docker, factor, **kwargs)

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:



.. py:class:: MediatorLocalSequenceMixin(database, seq_method='refseq', seq_subs=False, seq_aligner=None, seq_force_align=False, seq_refrep='tid', seq_filter_method=None, seq_filter_value=None, **kwargs)

   Bases: :class:`pmaf.pipe.agents.mediators.local._base.MediatorLocalBase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorSequenceMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.mediators.local._components.MediatorLocalSequenceMixin
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: SEQ_EXTRACT_METHODS
      :annotation: = ['refseq', 'consensus']

      

   .. attribute:: SEQ_FILTER_METHODS
      :annotation: = ['random', 'tab']

      

   .. method:: get_identifier_by_sequence(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_sequence_by_identifier(self, docker, factor, **kwargs)

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:



.. py:class:: MediatorLocalTaxonomyMixin(database, tax_rank_tolerance=None, tax_corr_method='lineage', tax_fuzzy_cutoff=95, tax_fuzzy_mode=False, tax_format=None, tax_refrep='tid', **kwargs)

   Bases: :class:`pmaf.pipe.agents.mediators.local._base.MediatorLocalBase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorTaxonomyMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.mediators.local._components.MediatorLocalTaxonomyMixin
      :parts: 1

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



