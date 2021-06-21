:orphan:

:mod:`pmaf.biome.essentials._repsequence`
=========================================

.. py:module:: pmaf.biome.essentials._repsequence


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.essentials._repsequence.RepSequence



.. py:class:: RepSequence(sequences: Union[str, MultiSequence, pd.DataFrame, pd.Series], **kwargs: Any)

   Bases: :class:`pmaf.biome.essentials._base.EssentialBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialFeatureMetabase`

   An `essential` class for handling feature sequence data.

   Constructor for :class:`.RepSequence`

   :param sequences: Sequence data
   :param \*\*kwargs: Compatibility

   .. method:: copy(self) -> 'RepSequence'

      Copy of the instance.


   .. method:: data(self) -> pd.DataFrame
      :property:

      :class:`pandas.DataFrame` with sequence data


   .. method:: export(self, output_fp: str, *args, _add_ext: bool = False, **kwargs: Any) -> None

      Exports the FASTA sequences into the specified file.

      :param output_fp: Export filepath
      :param \*args: Compatibility
      :param _add_ext: Add file extension or not.
      :param \*\*kwargs: Compatibility


   .. method:: get_subset(self, rids: Optional[AnyGenericIdentifier] = None, *args: Any, **kwargs: Any) -> 'RepSequence'

      Get subset of the :class:`.RepSequence`.

      :param rids: Feature identifiers.
      :param \*args: Compatibility
      :param \*\*kwargs: Compatibility

      :returns: :class:`.RepSequence`


   .. method:: to_multiseq(self) -> MultiSequence

      Creates an instance of :class:`~pmaf.sequence._multiple._multiple.MultiSequence` containing sequences.

      :returns: :class:`~pmaf.sequence._multiple._multiple.MultiSequence`


   .. method:: xrid(self) -> pd.Index
      :property:

      Feature identifiers



