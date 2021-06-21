:orphan:

:mod:`pmaf.database._parsers._qiime`
====================================

.. py:module:: pmaf.database._parsers._qiime


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.database._parsers._qiime.parse_qiime_sequence_generator
   pmaf.database._parsers._qiime.parse_qiime_taxonomy_map
   pmaf.database._parsers._qiime.read_qiime_taxonomy_map


.. function:: parse_qiime_sequence_generator(sequence_fasta_fp: str, chunk_size: int, alignment: bool) -> Generator[Union[Tuple[dict, pd.DataFrame], pd.DataFrame], None, None]

   Parser for sequence/alignment data in FASTA format provided in QIIME-styled databases.

   :param sequence_fasta_fp: Sequence data in FASTA format
   :param chunk_size: Chunk size to generate chunk :class:`~pandas.DataFrame`.
   :param alignment: True if MSA are supplied.

   :Yields: *First round* -- (Metadata :class:`dict`, Chunk :class:`~pandas.DataFrame`)
            Other rounds: Chunk :class:`~pandas.DataFrame`


.. function:: parse_qiime_taxonomy_map(taxonomy_map_df: pd.DataFrame) -> pd.DataFrame

   Parse taxonomy :class:`~pandas.DataFrame` in QIIME/Greengenes notation.
   Result produce class:`~pandas.DataFrame` where taxa are reorganized into ordered but unvalidated ranks.

   :param taxonomy_map_df: :class:`~pandas.DataFrame` with taxonomy data.

   :returns: Taxonomy sheet of type :class:`~pandas.DataFrame`


.. function:: read_qiime_taxonomy_map(taxonomy_tsv_fp: str) -> pd.Series

   Reads taxonomy file in QIIME/Greengenes notation.

   :param taxonomy_tsv_fp: Path to QIIME/Greengenes formatted taxonomy map.

   :returns: :class:`~pandas.Series` of taxonomy map.


