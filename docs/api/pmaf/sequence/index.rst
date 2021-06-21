:mod:`pmaf.sequence`
====================

.. py:module:: pmaf.sequence


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.sequence.MultiSequence
   pmaf.sequence.MultiSequenceStream
   pmaf.sequence.Nucleotide



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



.. py:class:: MultiSequenceStream(filepath=None, expected_rows=1000, mode='DNA', aligned=False, name=None, compressor=False)

   Bases: :class:`pmaf.sequence._metakit.MultiSequenceStreamBackboneMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: accession_numbers(self)
      :property:


   .. method:: append_sequence(self, sequence)

      :param sequence:

      Returns:


   .. method:: append_string(self, name, mode, sequence_str, metadata_dict={})

      :param name:
      :param mode:
      :param sequence_str:
      :param metadata_dict: (Default value = {})

      Returns:


   .. method:: close(self, copy_filepath=None)

      :param copy_filepath: (Default value = None)

      Returns:


   .. method:: count(self)
      :property:


   .. method:: extend_multiseq(self, multiseq)

      :param multiseq:

      Returns:


   .. method:: get_multiseq_by_accs(self, acc_numbers)

      :param acc_numbers:

      Returns:


   .. method:: get_sequence_by_acc(self, acc_number)

      :param acc_number:

      Returns:


   .. method:: iter_sequences(self)


   .. method:: mode(self)
      :property:


   .. method:: name(self)
      :property:


   .. method:: summarize(self)
      :property:


   .. method:: write_all_to_fasta(self, fasta_fp, write_in_chunks=100)

      :param fasta_fp:
      :param write_in_chunks: (Default value = 100)

      Returns:



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



