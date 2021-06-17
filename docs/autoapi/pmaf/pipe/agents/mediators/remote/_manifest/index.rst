:orphan:

:mod:`pmaf.pipe.agents.mediators.remote._manifest`
==================================================

.. py:module:: pmaf.pipe.agents.mediators.remote._manifest


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.mediators.remote._manifest.NCBIMediator



.. py:class:: NCBIMediator(entrez, seq_method='asis', seq_aligner=None, **kwargs)

   Bases: :class:`pmaf.pipe.agents.mediators._base.MediatorBase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorSequenceMetabase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorTaxonomyMetabase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorAccessionMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: SEQ_EXTRACT_METHODS
      :annotation: = ['asis', 'consensus']

      

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


   .. method:: get_identifier_by_sequence(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_identifier_by_taxonomy(self, docker, factor, **kwargs)

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_sequence_by_identifier(self, docker, factor, **kwargs)

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_taxonomy_by_identifier(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: state(self)
      :property:


   .. method:: verify_factor(self, factor)

      :param factor:

      Returns:



