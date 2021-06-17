:orphan:

:mod:`pmaf.sequence._multiple._multiple`
========================================

.. py:module:: pmaf.sequence._multiple._multiple


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.sequence._multiple._multiple.MultiSequence



.. py:class:: MultiSequence(sequences, name=None, mode=None, metadata=None, aligned=False, **kwargs)

   Bases: :class:`pmaf.sequence._metakit.MultiSequenceMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: buckle_for_alignment(self)


   .. method:: copy(self)


   .. method:: count(self)
      :property:


   .. method:: from_buckled(cls, sequences, buckled_pack, **kwargs)
      :classmethod:

      :param sequences:
      :param buckled_pack:
      :param \*\*kwargs:

      Returns:


   .. method:: get_consensus(self, indices=None)

      :param indices: (Default value = None)

      Returns:


   .. method:: get_iter(self, method='asis')

      :param method: (Default value = 'asis')

      Returns:


   .. method:: get_string_as(self, **kwargs)

      :param \*\*kwargs:

      Returns:


   .. method:: get_subset(self, indices=None)

      :param indices: (Default value = None)

      Returns:


   .. method:: index(self)
      :property:


   .. method:: is_alignment(self)
      :property:


   .. method:: is_buckled(self)
      :property:


   .. method:: metadata(self)
      :property:


   .. method:: mode(self)
      :property:


   .. method:: name(self)
      :property:


   .. method:: restore_buckle(self, buckled_pack)

      :param buckled_pack:

      Returns:


   .. method:: sequences(self)
      :property:


   .. method:: skbio_mode(self)
      :property:


   .. method:: to_skbio_msa(self, indices=None)

      :param indices: (Default value = None)

      Returns:


   .. method:: write(self, file, mode='w', **kwargs)

      :param file:
      :param mode: (Default value = 'w')
      :param \*\*kwargs:

      Returns:



