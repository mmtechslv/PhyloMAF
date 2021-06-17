:orphan:

:mod:`pmaf.sequence._multiple._stream`
======================================

.. py:module:: pmaf.sequence._multiple._stream


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.sequence._multiple._stream.MultiSequenceStream



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



