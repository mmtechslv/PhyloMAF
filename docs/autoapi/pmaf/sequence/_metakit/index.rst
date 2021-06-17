:orphan:

:mod:`pmaf.sequence._metakit`
=============================

.. py:module:: pmaf.sequence._metakit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.sequence._metakit.MultiSequenceMetabase
   pmaf.sequence._metakit.MultiSequenceStreamBackboneMetabase
   pmaf.sequence._metakit.NucleotideMetabase
   pmaf.sequence._metakit.SequenceBackboneMetabase



.. py:class:: MultiSequenceMetabase

   Bases: :class:`pmaf.sequence._metakit.SequenceBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.sequence._metakit.MultiSequenceMetabase
      :parts: 1

   .. method:: buckle_for_alignment(self)
      :abstractmethod:


   .. method:: count(self)
      :property:


   .. method:: from_buckled(cls, sequences, buckled_pack, **kwargs)
      :classmethod:
      :abstractmethod:

      :param sequences:
      :param buckled_pack:
      :param \*\*kwargs:

      Returns:


   .. method:: get_consensus(self, indices)
      :abstractmethod:

      :param indices:

      Returns:


   .. method:: get_iter(self, method)
      :abstractmethod:

      :param method:

      Returns:


   .. method:: get_subset(self, indices)
      :abstractmethod:

      :param indices:

      Returns:


   .. method:: index(self)
      :property:


   .. method:: is_alignment(self)
      :property:


   .. method:: restore_buckle(self, packed_metadata)
      :abstractmethod:

      :param packed_metadata:

      Returns:


   .. method:: sequences(self)
      :property:


   .. method:: to_skbio_msa(self, indices)
      :abstractmethod:

      :param indices:

      Returns:



.. py:class:: MultiSequenceStreamBackboneMetabase(filepath, mode, aligned, name, compressor)

   Bases: :class:`abc.ABC`

   .. autoapi-inheritance-diagram:: pmaf.sequence._metakit.MultiSequenceStreamBackboneMetabase
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: accession_numbers(self)
      :property:


   .. method:: append_sequence(self, sequence)
      :abstractmethod:

      :param sequence:

      Returns:


   .. method:: append_string(self, name, mode, sequence_str, metadata_dict)
      :abstractmethod:

      :param name:
      :param mode:
      :param sequence_str:
      :param metadata_dict:

      Returns:


   .. method:: count(self)
      :property:


   .. method:: extend_multiseq(self, multiseq)
      :abstractmethod:

      :param multiseq:

      Returns:


   .. method:: get_multiseq_by_accs(self, acc_numbers)
      :abstractmethod:

      :param acc_numbers:

      Returns:


   .. method:: get_sequence_by_acc(self, acc_number)
      :abstractmethod:

      :param acc_number:

      Returns:


   .. method:: mode(self)
      :property:


   .. method:: name(self)
      :property:


   .. method:: summarize(self)
      :property:



.. py:class:: NucleotideMetabase

   Bases: :class:`pmaf.sequence._metakit.SequenceBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.sequence._metakit.NucleotideMetabase
      :parts: 1

   .. method:: buckle_by_uid(self, tmp_uid)
      :abstractmethod:

      :param tmp_uid:

      Returns:


   .. method:: complement(self)
      :abstractmethod:


   .. method:: copy(self)
      :abstractmethod:


   .. method:: length(self)
      :property:


   .. method:: read(cls, file, name=None, metadata=None, mode='DNA', **kwargs)
      :classmethod:
      :abstractmethod:

      :param file:
      :param name: (Default value = None)
      :param metadata: (Default value = None)
      :param mode: (Default value = 'DNA')
      :param \*\*kwargs:

      Returns:


   .. method:: restore_buckle(self, packed_metadata)
      :abstractmethod:

      :param packed_metadata:

      Returns:


   .. method:: skbio(self)
      :property:


   .. method:: text(self)
      :property:


   .. method:: unbuckle_uid(self)
      :abstractmethod:



.. py:class:: SequenceBackboneMetabase

   Bases: :class:`abc.ABC`

   .. autoapi-inheritance-diagram:: pmaf.sequence._metakit.SequenceBackboneMetabase
      :parts: 1

   .. method:: get_string_as(self, **kwargs)
      :abstractmethod:

      :param \*\*kwargs:

      Returns:


   .. method:: is_buckled(self)
      :property:


   .. method:: metadata(self)
      :property:


   .. method:: mode(self)
      :property:


   .. method:: name(self)
      :property:


   .. method:: skbio_mode(self)
      :property:


   .. method:: write(self, file, **kwargs)
      :abstractmethod:

      :param file:
      :param \*\*kwargs:

      Returns:



