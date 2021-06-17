:mod:`pmaf.pipe.agents.dockers`
===============================

.. py:module:: pmaf.pipe.agents.dockers


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.dockers.DockerAccessionMedium
   pmaf.pipe.agents.dockers.DockerIdentifierMedium
   pmaf.pipe.agents.dockers.DockerPhylogenyMedium
   pmaf.pipe.agents.dockers.DockerSequenceMedium
   pmaf.pipe.agents.dockers.DockerTaxonomyMedium



.. py:class:: DockerAccessionMedium(accessions, **kwargs)

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerAccessionMetabase`, :class:`pmaf.pipe.agents.dockers._base.DockerBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers.DockerAccessionMedium
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

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers.DockerIdentifierMedium
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: to_array(self, indices=None, exclude_missing=False, unique=False)

      :param indices: (Default value = None)
      :param exclude_missing: (Default value = False)
      :param unique: (Default value = False)

      Returns:



.. py:class:: DockerPhylogenyMedium(trees, ignore_tips=False, **kwargs)

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerPhylogenyMetabase`, :class:`pmaf.pipe.agents.dockers._base.DockerBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers.DockerPhylogenyMedium
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

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers.DockerSequenceMedium
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

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers.DockerTaxonomyMedium
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



