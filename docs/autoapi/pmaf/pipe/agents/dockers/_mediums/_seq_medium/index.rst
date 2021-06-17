:orphan:

:mod:`pmaf.pipe.agents.dockers._mediums._seq_medium`
====================================================

.. py:module:: pmaf.pipe.agents.dockers._mediums._seq_medium


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.dockers._mediums._seq_medium.DockerSequenceMedium



.. py:class:: DockerSequenceMedium(sequences, mode='DNA', aligned=None, **kwargs)

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerSequenceMetabase`, :class:`pmaf.pipe.agents.dockers._base.DockerBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.dockers._mediums._seq_medium.DockerSequenceMedium
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



