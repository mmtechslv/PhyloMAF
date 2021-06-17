:orphan:

:mod:`pmaf.biome.essentials._frequency`
=======================================

.. py:module:: pmaf.biome.essentials._frequency


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.essentials._frequency.FrequencyTable



.. py:class:: FrequencyTable(frequency: Union[pd.DataFrame, str], skipcols: Union[Sequence[Union[str, int]], str, int] = None, allow_nan: bool = False, **kwargs)

   Bases: :class:`pmaf.biome.essentials._base.EssentialBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialFeatureMetabase`, :class:`pmaf.biome.essentials._metakit.EssentialSampleMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.essentials._frequency.FrequencyTable
      :parts: 1

   An essential class for handling frequency data.

   Constructor for :class:`.FrequencyTable`

   :param frequency: Data containing frequency data.
   :param skipcols: Columns to skip when processing data.
   :param allow_nan: Allow NA/NaN values or raise an error.
   :param \*\*kwargs: Remaining parameters passed to :func:`~pandas.read_csv` or :mod:`biom` loader.

   .. method:: any_nan(self) -> bool
      :property:

      Is there nan values present?


   .. method:: copy(self) -> 'FrequencyTable'

      Copy of the instance.


   .. method:: data(self) -> pd.DataFrame
      :property:

      Pandas dataframe of `FrequencyTable`


   .. method:: drop_features_by_id(self, ids: GenericIdentifier) -> Union[None, np.ndarray]

      Drop features by `ids`

      :param ids: Feature identifiers


   .. method:: drop_features_without_counts(self) -> Optional[np.ndarray]

      Drop features that has no counts. Typically required after dropping samples.


   .. method:: drop_samples_by_id(self, ids: GenericIdentifier) -> Optional[np.ndarray]

      Drop samples by `ids`.

      :param ids: Sample identifiers


   .. method:: export(self, output_fp: str, *args, _add_ext: bool = False, sep: str = ',', **kwargs) -> None

      Exports the sample metadata content into the specified file.

      :param output_fp: Export filepath.
      :type output_fp: str
      :param \*args: Compatibility
      :param _add_ext: Add file extension or not.
      :param sep: Delimiter
      :param \*\*kwargs: Compatibility


   .. method:: from_biom(cls, filepath: str, **kwargs) -> 'FrequencyTable'
      :classmethod:

      Factory method to construct a :class:`.FrequencyTable` from :mod:`biom` file.

      :param filepath: Path to :mod:`biom` file.
      :type filepath: str
      :param \*\*kwargs: Compatibility

      :returns: Instance of :class:`.FrequencyTable`


   .. method:: from_csv(cls, filepath: str, **kwargs) -> 'FrequencyTable'
      :classmethod:

      Factory method to construct a :class:`.FrequencyTable` from CSV file.

      :param filepath: Path to .csv file.
      :type filepath: str
      :param \*\*kwargs: Compatibility

      :returns: Instance of :class:`.FrequencyTable`


   .. method:: get_subset(self, rids: Optional[GenericIdentifier] = None, sids: Optional[GenericIdentifier] = None, *args, **kwargs) -> 'FrequencyTable'

      Get subset of the :class:`.FrequencyTable`.

      :param rids: Feature Identifiers
      :param sids: Sample Identifiers
      :param \*args: Compatibility
      :param \*\*kwargs: Compatibility

      :returns: Instance of :class:`.FrequencyTable`.


   .. method:: merge_features_by_map(self, mapping: Mapper, aggfunc: Union[str, Callable] = 'sum', **kwargs) -> Optional[Mapper]

      Merge features by `mapping`.

      :param mapping: Map with values as feature identifiers to be aggregated.
      :param aggfunc: Aggregation function to apply
      :param \*\*kwargs: Compatibility


   .. method:: merge_samples_by_map(self, mapping: Mapper, aggfunc: Union[str, Callable] = 'mean', **kwargs) -> Optional[Mapper]

      Merge samples by `mapping`

      :param mapping: Map with values as sample identifiers to be aggregated.
      :param aggfunc: Aggregation function to apply
      :param \*\*kwargs: Compatibility


   .. method:: rename_samples(self, mapper: Mapper) -> None

      Rename sample names

      :param mapper: Rename samples by map


   .. method:: replace_nan_with(self, value: Any) -> None

      Replace NaN values with `value`.

      :param value: Value to replace NaN's.


   .. method:: transform_to_relative_abundance(self)

      Transform absolute counts to relative.


   .. method:: xrid(self) -> pd.Index
      :property:

      Feature axis.


   .. method:: xsid(self) -> pd.Index
      :property:

      Sample axis.



