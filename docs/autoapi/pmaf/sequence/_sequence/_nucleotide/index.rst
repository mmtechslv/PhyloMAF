:orphan:

:mod:`pmaf.sequence._sequence._nucleotide`
==========================================

.. py:module:: pmaf.sequence._sequence._nucleotide


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.sequence._sequence._nucleotide.Nucleotide



.. py:class:: Nucleotide(sequence, name=None, metadata=None, mode='DNA', **kwargs)

   Bases: :class:`pmaf.sequence._metakit.NucleotideMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: buckle_by_uid(self, uid)

      :param uid:

      Returns:


   .. method:: complement(self)


   .. method:: copy(self)


   .. method:: get_string_as(self, format='fasta', **kwargs)

      :param format: (Default value = 'fasta')
      :param \*\*kwargs:

      Returns:


   .. method:: is_buckled(self)
      :property:


   .. method:: length(self)
      :property:


   .. method:: metadata(self)
      :property:


   .. method:: mode(self)
      :property:


   .. method:: name(self)
      :property:


   .. method:: read(cls, file, name=None, metadata=None, mode='DNA', **kwargs)
      :classmethod:

      :param file:
      :param name: (Default value = None)
      :param metadata: (Default value = None)
      :param mode: (Default value = 'DNA')
      :param \*\*kwargs:

      Returns:


   .. method:: restore_buckle(self, buckled_pack)

      :param buckled_pack:

      Returns:


   .. method:: skbio(self)
      :property:


   .. method:: skbio_mode(self)
      :property:


   .. method:: text(self)
      :property:


   .. method:: unbuckle_uid(self)


   .. method:: write(self, file, format='fasta', **kwargs)

      :param file:
      :param format: (Default value = 'fasta')
      :param \*\*kwargs:

      Returns:



