:orphan:

:mod:`pmaf.pipe.agents.dockers._metakit`
========================================

.. py:module:: pmaf.pipe.agents.dockers._metakit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.dockers._metakit.DockerAccessionMetabase
   pmaf.pipe.agents.dockers._metakit.DockerBackboneMetabase
   pmaf.pipe.agents.dockers._metakit.DockerIdentifierMetabase
   pmaf.pipe.agents.dockers._metakit.DockerPhylogenyMetabase
   pmaf.pipe.agents.dockers._metakit.DockerSequenceMetabase
   pmaf.pipe.agents.dockers._metakit.DockerTaxonomyMetabase



.. py:class:: DockerAccessionMetabase

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers._metakit.DockerAccessionMetabase
      :parts: 1

   Interface for DockerAccession.

   .. method:: sources(self)
      :property:


   .. method:: to_identifier_by_src(self, source, exclude_missing)
      :abstractmethod:

      Converts the Docker elements to the DockerIdentifier for selected `source` parameter.

      :param source:
      :param exclude_missing:

      Returns:



.. py:class:: DockerBackboneMetabase

   Bases: :class:`abc.ABC`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers._metakit.DockerBackboneMetabase
      :parts: 1

   Base interface for all Docker classes.

   .. method:: count(self)
      :property:


   .. method:: data(self)
      :property:

      Returns objects with actual data that docker contains.


   .. method:: empty(self)
      :property:

      Returns true of instance is empty.


   .. method:: get_iterator(self, indices, exclude_missing)
      :abstractmethod:

      Returns an generator for that iterates over Docker elements.

      :param indices:
      :param exclude_missing:

      Returns:


   .. method:: get_subset(self, indices, exclude_missing)
      :abstractmethod:

      Returns subset of the Docker instance.

      :param indices:
      :param exclude_missing:

      Returns:


   .. method:: index(self)
      :property:

      Returns all IDs.


   .. method:: metadata(self)
      :property:

      Returns metadata of the Docker.


   .. method:: missing(self)
      :property:

      Returns IDs of elements that are set to None.


   .. method:: name(self)
      :property:

      Returns name/label of the docker.


   .. method:: singleton(self)
      :property:

      Returns true if instance is singleton.


   .. method:: valid(self)
      :property:

      Returns IDs of elements that are not set to None.


   .. method:: wrap_meta(self)
      :abstractmethod:

      Returns a wrapped metadata as a dictionary.



.. py:class:: DockerIdentifierMetabase

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers._metakit.DockerIdentifierMetabase
      :parts: 1

   Interface for DockerIdentifiers.

   .. method:: to_array(self, indices, exclude_missing)
      :abstractmethod:

      Converts Docker elements into array or Docker container into dict of arrays.

      :param indices:
      :param exclude_missing:

      Returns:



.. py:class:: DockerPhylogenyMetabase

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers._metakit.DockerPhylogenyMetabase
      :parts: 1

   Interface for DockerPhylogeny.

   .. method:: get_node_names(self, indices)
      :abstractmethod:

      :param indices:

      Returns:


   .. method:: get_tip_names(self, indices)
      :abstractmethod:

      Returns only tip names of the tree that Docker contains.

      :param indices:

      Returns:



.. py:class:: DockerSequenceMetabase

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers._metakit.DockerSequenceMetabase
      :parts: 1

   Interface for DockerSequence.

   .. method:: aligned(self)
      :property:

      Returns True if the sequences that Docker contains are aligned.


   .. method:: get_records(self, indices)
      :abstractmethod:

      Returns the Docker elements as "record" tuples.

      :param indices:

      Returns:


   .. method:: get_stats(self, indices)
      :abstractmethod:

      Returns the "stats" for "record" elements.

      :param indices): # FIXME: Same as DockerSequenceMetabase.get_records(...:
      :param indices): # FIXME: Same as DockerSequenceMetabase.get_records(...:
      :param indices): # FIXME: Same as DockerSequenceMetabase.get_records(...:

      Returns:


   .. method:: mode(self)
      :property:

      Returns mode of the Docker instance. Mode refers to DNA, RNA or Protein.


   .. method:: to_multiseq(self, indices)
      :abstractmethod:

      Converts Docker elements into Multiseq object.

      :param indices:

      Returns:



.. py:class:: DockerTaxonomyMetabase

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers._metakit.DockerTaxonomyMetabase
      :parts: 1

   Interface for DockerTaxonomy.

   .. method:: get_avail_ranks(self, indices)
      :abstractmethod:

      :param indices:

      Returns:


   .. method:: to_dataframe(self, indices, ranks)
      :abstractmethod:

      Converts docker elements into dataframe or Docker container into dict of dataframes.

      :param indices:
      :param ranks:

      Returns:



