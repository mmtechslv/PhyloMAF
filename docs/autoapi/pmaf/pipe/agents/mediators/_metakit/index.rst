:orphan:

:mod:`pmaf.pipe.agents.mediators._metakit`
==========================================

.. py:module:: pmaf.pipe.agents.mediators._metakit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.mediators._metakit.MediatorAccessionMetabase
   pmaf.pipe.agents.mediators._metakit.MediatorBackboneMetabase
   pmaf.pipe.agents.mediators._metakit.MediatorPhylogenyMetabase
   pmaf.pipe.agents.mediators._metakit.MediatorSequenceMetabase
   pmaf.pipe.agents.mediators._metakit.MediatorTaxonomyMetabase



.. py:class:: MediatorAccessionMetabase

   Bases: :class:`pmaf.pipe.agents.mediators._metakit.MediatorBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.mediators._metakit.MediatorAccessionMetabase
      :parts: 1

   .. method:: get_accession_by_identifier(self, docker, factor, **kwargs)
      :abstractmethod:

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



.. py:class:: MediatorBackboneMetabase

   Bases: :class:`abc.ABC`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.mediators._metakit.MediatorBackboneMetabase
      :parts: 1

   .. method:: client(self)
      :property:


   .. method:: configs(self)
      :property:


   .. method:: reconfig(self, name, value)
      :abstractmethod:

      :param name:
      :param value:

      Returns:


   .. method:: state(self)
      :property:


   .. method:: verify_factor(self, factor)
      :abstractmethod:

      :param factor:

      Returns:



.. py:class:: MediatorPhylogenyMetabase

   Bases: :class:`pmaf.pipe.agents.mediators._metakit.MediatorBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.mediators._metakit.MediatorPhylogenyMetabase
      :parts: 1

   .. method:: get_identifier_by_phylogeny(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_phylogeny_by_identifier(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:



.. py:class:: MediatorSequenceMetabase

   Bases: :class:`pmaf.pipe.agents.mediators._metakit.MediatorBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.mediators._metakit.MediatorSequenceMetabase
      :parts: 1

   .. method:: get_identifier_by_sequence(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_sequence_by_identifier(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:



.. py:class:: MediatorTaxonomyMetabase

   Bases: :class:`pmaf.pipe.agents.mediators._metakit.MediatorBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.mediators._metakit.MediatorTaxonomyMetabase
      :parts: 1

   .. method:: get_identifier_by_taxonomy(self, docker, factor, **kwargs)
      :abstractmethod:

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



