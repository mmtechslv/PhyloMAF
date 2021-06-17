:orphan:

:mod:`pmaf.biome.essentials._samplemeta`
========================================

.. py:module:: pmaf.biome.essentials._samplemeta


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.essentials._samplemeta.SampleMetadata



.. py:class:: SampleMetadata(samples: Union[pd.DataFrame, str], axis: Union[int, str] = 1, index_col: Union[str, int] = 0, **kwargs: Any)

   Bases: :class:`pmaf.biome.essentials._base.EssentialBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialSampleMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.essentials._samplemeta.SampleMetadata
      :parts: 1

   An `essential` class for handling sample metadata.

   Constructor for :class:`.SampleMetadata`

   :param samples: Data containing sample metadata
   :param axis: Sample index axis. Using 0/`index` sets rows as sample indices while 1/`columns` sets columns as indices.
   :param index_col: Which row/column to use as index.
   :param \*\*kwargs: Passed to :func:`~pandas.read_csv` or :mod:`biom` loader.

   .. method:: copy(self) -> 'SampleMetadata'

      Copy of the instance.


   .. method:: data(self) -> pd.DataFrame
      :property:

      Sample metadata


   .. method:: drop_sample_by_id(self, ids: GenericIdentifier, **kwargs) -> Optional[GenericIdentifier]

      Drop samples by sample identifiers.

      :param ids: Identifiers to remove
      :param \*\*kwargs: Compatibility


   .. method:: export(self, output_fp: str, *args, _add_ext: bool = False, sep: str = ',', **kwargs) -> None

      Exports the sample metadata content into the specified file.

      :param output_fp: Export filepath
      :param \*args: Compatibility
      :param _add_ext: Add file extension or not.
      :param sep: Delimiter
      :param \*\*kwargs: Compatibility


   .. method:: from_biom(cls, filepath: str, **kwargs) -> 'SampleMetadata'
      :classmethod:

      Factory method to construct a :class:`.SampleMetadata` from :mod:`biom` file.

      :param filepath: (str): Path to :mod:`biom` file.
      :param \*\*kwargs: Passed to the constructor.

      :returns: Instance of :class:`.SampleMetadata`


   .. method:: from_csv(cls, filepath: str, **kwargs: Any) -> 'SampleMetadata'
      :classmethod:

      Factory method to construct a :class:`.SampleMetadata` from CSV file.

      :param filepath: Path to .csv file.
      :type filepath: str
      :param \*\*kwargs: Passed to the constructor.

      :returns: Instance of :class:`.SampleMetadata`


   .. method:: get_subset(self, sids: GenericIdentifier = None, *args, **kwargs) -> 'SampleMetadata'

      Get subset of the :class:`.SampleMetadata`.

      :param sids: Sample Identifiers
      :param \*args: Compatibility
      :param \*\*kwargs: Compatibility

      :returns: Instance of :class:`.SampleMetadata`.


   .. method:: get_variables_by_id(self, ids: Optional[GenericIdentifier] = None, variables: Optional[GenericIdentifier] = None) -> Union[pd.Series, pd.DataFrame, str, int]

      Get sample metadata by sample identifiers and variables.

      :param ids: Sample identifiers
      :param variables: Metadata varibles

      :returns: :class:`~pandas.DataFrame`


   .. method:: merge_samples_by_variable(self, variable: Union[str, int], aggfunc: Union[str, Callable] = 'mean', **kwargs) -> Optional[Mapper]

      Merge samples by `variable`.

      :param variable: Sample metadata variable.
      :param aggfunc: Aggregation function that will be applied to both :class:`.SampleMetadata` instance and ratified to other `essentials` if contained in :class:`~pmaf.biome.assembly.BiomeAssembly` instance.
      :param \*\*kwargs: Compatibility


   .. method:: rename_samples(self, mapper: Mapper) -> None

      Rename sample names by `mapper`

      :param mapper: Dict-like mapper use for renaming.


   .. method:: variables(self) -> np.ndarray
      :property:

      Sample metadata variables


   .. method:: xsid(self) -> pd.Index
      :property:

      Sample identifiers



