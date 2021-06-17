:orphan:

:mod:`pmaf.pipe.agents.miners._metakit`
=======================================

.. py:module:: pmaf.pipe.agents.miners._metakit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.miners._metakit.MinerBackboneMetabase



.. py:class:: MinerBackboneMetabase

   Bases: :class:`abc.ABC`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.miners._metakit.MinerBackboneMetabase
      :parts: 1

   .. method:: factor(self)
      :property:


   .. method:: mediator(self)
      :property:


   .. method:: state(self)
      :property:


   .. method:: verify_docker(self, docker)
      :abstractmethod:

      :param docker:

      Returns:


   .. method:: yield_accession_by_identifier(self, docker, **kwargs)
      :abstractmethod:

      :param docker:
      :param \*\*kwargs:

      Returns:


   .. method:: yield_identifier_by_docker(self, docker, **kwargs)
      :abstractmethod:

      :param docker:
      :param \*\*kwargs:

      Returns:


   .. method:: yield_phylogeny_by_identifier(self, docker, **kwargs)
      :abstractmethod:

      :param docker:
      :param \*\*kwargs:

      Returns:


   .. method:: yield_sequence_by_identifier(self, docker, **kwargs)
      :abstractmethod:

      :param docker:
      :param \*\*kwargs:

      Returns:


   .. method:: yield_taxonomy_by_identifier(self, docker, **kwargs)
      :abstractmethod:

      :param docker:
      :param \*\*kwargs:

      Returns:



