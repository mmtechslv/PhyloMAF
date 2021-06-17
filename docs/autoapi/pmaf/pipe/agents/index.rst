:mod:`pmaf.pipe.agents`
=======================

.. py:module:: pmaf.pipe.agents


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   dockers/index.rst
   mediators/index.rst
   miners/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.DockerAccessionMedium
   pmaf.pipe.agents.DockerIdentifierMedium
   pmaf.pipe.agents.DockerPhylogenyMedium
   pmaf.pipe.agents.DockerSequenceMedium
   pmaf.pipe.agents.DockerTaxonomyMedium
   pmaf.pipe.agents.Miner
   pmaf.pipe.agents.NCBIMediator



Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.LocalMediator


.. py:class:: DockerAccessionMedium(accessions, **kwargs)

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerAccessionMetabase`, :class:`pmaf.pipe.agents.dockers._base.DockerBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.DockerAccessionMedium
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: sources(self)
      :property:


   .. method:: to_identifier_by_src(self, source, exclude_missing=False)

      :param source:
      :param exclude_missing: (Default value = False)

      Returns:



.. py:class:: DockerIdentifierMedium(identifiers, **kwargs)

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerIdentifierMetabase`, :class:`pmaf.pipe.agents.dockers._base.DockerBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.DockerIdentifierMedium
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: to_array(self, indices=None, exclude_missing=False, unique=False)

      :param indices: (Default value = None)
      :param exclude_missing: (Default value = False)
      :param unique: (Default value = False)

      Returns:



.. py:class:: DockerPhylogenyMedium(trees, ignore_tips=False, **kwargs)

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerPhylogenyMetabase`, :class:`pmaf.pipe.agents.dockers._base.DockerBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.DockerPhylogenyMedium
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_node_names(self, indices=None, dtype=None, include_missing=False)

      :param indices: (Default value = None)
      :param dtype: (Default value = None)
      :param include_missing: (Default value = False)

      Returns:


   .. method:: get_tip_names(self, indices=None, dtype=None)

      :param indices: (Default value = None)
      :param dtype: (Default value = None)

      Returns:


   .. method:: get_tree(self, indices=None, exclude_missing=False)

      :param indices: (Default value = None)
      :param exclude_missing: (Default value = False)

      Returns:



.. py:class:: DockerSequenceMedium(sequences, mode='DNA', aligned=None, **kwargs)

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerSequenceMetabase`, :class:`pmaf.pipe.agents.dockers._base.DockerBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.DockerSequenceMedium
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: aligned(self)
      :property:


   .. method:: get_records(self, indices=None, exclude_missing=False)

      :param indices: (Default value = None)
      :param exclude_missing: (Default value = False)

      Returns:


   .. method:: get_stats(self, indices=None, exclude_missing=False)

      :param indices: (Default value = None)
      :param exclude_missing: (Default value = False)

      Returns:


   .. method:: mode(self)
      :property:


   .. method:: to_multiseq(self, indices=None)

      :param indices: (Default value = None)

      Returns:



.. py:class:: DockerTaxonomyMedium(taxonomy, **kwargs)

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerTaxonomyMetabase`, :class:`pmaf.pipe.agents.dockers._base.DockerBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.DockerTaxonomyMedium
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_avail_ranks(self, indices=None)

      :param indices: (Default value = None)

      Returns:


   .. method:: to_dataframe(self, indices=None, ranks=None, exclude_missing=False)

      :param indices: (Default value = None)
      :param ranks: (Default value = None)
      :param exclude_missing: (Default value = False)

      Returns:



.. py:class:: Miner(*args, **kwargs)

   Bases: :class:`pmaf.pipe.agents.miners._base.MinerBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.Miner
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: yield_accession_by_identifier(self, docker, **kwargs)

      :param docker:
      :param \*\*kwargs:

      Returns:


   .. method:: yield_identifier_by_docker(self, docker, **kwargs)

      :param docker:
      :param \*\*kwargs:

      Returns:


   .. method:: yield_phylogeny_by_identifier(self, docker, **kwargs)

      :param docker:
      :param \*\*kwargs:

      Returns:


   .. method:: yield_sequence_by_identifier(self, docker, **kwargs)

      :param docker:
      :param \*\*kwargs:

      Returns:


   .. method:: yield_taxonomy_by_identifier(self, docker, **kwargs)

      :param docker:
      :param \*\*kwargs:

      Returns:



.. py:class:: NCBIMediator(entrez, seq_method='asis', seq_aligner=None, **kwargs)

   Bases: :class:`pmaf.pipe.agents.mediators._base.MediatorBase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorSequenceMetabase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorTaxonomyMetabase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorAccessionMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.NCBIMediator
      :parts: 1

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



.. function:: LocalMediator(database, **kwargs)

   :param database:
   :param \*\*kwargs:

   Returns:


