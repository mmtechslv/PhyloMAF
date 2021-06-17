:orphan:

:mod:`pmaf.remote._entrez._entrez`
==================================

.. py:module:: pmaf.remote._entrez._entrez


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.remote._entrez._entrez.Entrez



.. py:class:: Entrez(email, api_key=None, tool='PhyloMAF')

   Bases: :class:`pmaf.remote._entrez._base.EntrezBase`

   .. autoapi-inheritance-diagram:: pmaf.remote._entrez._entrez.Entrez
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: get_chromosome_id_by_genome_id(self, genome_id)

      :param genome_id:

      Returns:


   .. method:: get_fasta_sequence_by_param(self, accession_id, start_pos, stop_pos, strand)

      :param accession_id:
      :param start_pos:
      :param stop_pos:
      :param strand:

      Returns:


   .. method:: get_gene_features_by_chromosome_id(self, chromosome_id, gene='rRNA')

      :param chromosome_id:
      :param gene: (Default value = 'rRNA')

      Returns:


   .. method:: get_genome_id_by_taxid(self, taxid)

      :param taxid:

      Returns:


   .. method:: get_taxid_by_query(self, query)

      :param query:

      Returns:



