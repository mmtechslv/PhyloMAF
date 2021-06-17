:orphan:

:mod:`pmaf.biome.essentials._taxonomy`
======================================

.. py:module:: pmaf.biome.essentials._taxonomy


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.essentials._taxonomy.RepTaxonomy



.. py:class:: RepTaxonomy(taxonomy: Union[pd.DataFrame, pd.Series, str], taxonomy_columns: Union[str, int, Sequence[Union[int, str]]] = None, **kwargs: Any)

   Bases: :class:`pmaf.biome.essentials._base.EssentialBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialFeatureMetabase`

   An `essential` class for handling taxonomy data.

   Constructor for :class:`.RepTaxonomy`

   :param taxonomy: Data containing feature taxonomy
   :param taxonomy_columns: Column(s) containing taxonomy data
   :param \*\*kwargs: Passed to :func:`~pandas.read_csv` or :mod:`biom` loader.

   .. method:: avail_ranks(self) -> Sequence[str]
      :property:

      List of available taxonomic ranks.


   .. method:: copy(self) -> 'RepTaxonomy'

      Copy of the instance.


   .. method:: data(self) -> pd.DataFrame
      :property:

      Actual data representation as pd.DataFrame


   .. method:: drop_feature_by_id(self, ids: GenericIdentifier, **kwargs: Any) -> Optional[GenericIdentifier]

      Remove features by feature `ids`.

      :param ids: Feature identifiers
      :param \*\*kwargs: Compatibility


   .. method:: drop_features_without_ranks(self, ranks: Sequence[str], any: bool = False, **kwargs: Any) -> Optional[GenericIdentifier]

      Remove features that do not contain `ranks`

      :param ranks: Ranks to look for
      :param any: If True removes feature with single occurrence of missing rank.
                  If False all `ranks` must be missing.
      :param \*\*kwargs: Compatibility


   .. method:: drop_features_without_taxa(self, **kwargs: Any) -> Optional[GenericIdentifier]

      Remove features that do not contain taxonomy.


   .. method:: duplicated(self) -> pd.Index
      :property:

      List of duplicated feature indices.


   .. method:: export(self, output_fp: str, *args, _add_ext: bool = False, sep: str = ',', **kwargs: Any) -> None

      Exports the taxonomy into the specified file.

      :param output_fp: Export filepath
      :param \*args: Compatibility
      :param _add_ext: Add file extension or not.
      :param sep: Delimiter
      :param \*\*kwargs: Compatibility


   .. method:: find_features_by_pattern(self, pattern_str: str, case_sensitive: bool = False, regex: bool = False) -> np.ndarray

      Searches for features with taxa that matches `pattern_str`

      :param pattern_str: Pattern to search for
      :param case_sensitive: Case sensitive mode
      :param regex: Use regular expressions

      :returns: :class:`~numpy.ndarray` with indices


   .. method:: find_features_without_taxa(self) -> np.ndarray

      Find features without taxa.

      :returns: :class:`~numpy.ndarray` with feature indices.


   .. method:: from_biom(cls, filepath: str, **kwargs: Any) -> 'RepTaxonomy'
      :classmethod:

      Factory method to construct a :class:`.RepTaxonomy` from :mod:`biom` file.

      :param filepath: :mod:`biom` file path.
      :param \*\*kwargs: Passed to the constructor.

      :returns: Instance of :class:`.RepTaxonomy`


   .. method:: from_csv(cls, filepath: str, taxonomy_columns: Union[str, int, Sequence[Union[int, str]]] = None, **kwargs: Any) -> 'RepTaxonomy'
      :classmethod:

      Factory method to construct a :class:`.RepTaxonomy` from CSV file.

      :param filepath: Path to .csv File
      :param taxonomy_columns: Column(s) containing taxonomy data
      :param \*\*kwargs: Passed to the constructor.

      :returns: Instance of :class:`.RepTaxonomy`


   .. method:: get_lineage_by_id(self, ids: Optional[GenericIdentifier] = None, missing_rank: bool = False, desired_ranks: Union[bool, Sequence[str]] = False, drop_ranks: Union[bool, Sequence[str]] = False, **kwargs: Any) -> pd.Series

      Get taxonomy lineages by feature `ids`.

      :param ids: Either feature indices or None for all.
      :param missing_rank: If True will generate prefix like `s__` or `d__`
      :param desired_ranks: List of desired ranks to generate.
                            If False then will generate all main ranks
      :param drop_ranks: List of ranks to drop from desired ranks.
                         This parameter only useful if `missing_rank` is True
      :param \*\*kwargs: Compatibility.

      :returns: :class:`pandas.Series` with consensus lineages and corresponding IDs


   .. method:: get_subset(self, rids: Optional[GenericIdentifier] = None, *args, **kwargs: Any) -> 'RepTaxonomy'

      Get subset of the :class:`.RepTaxonomy`.

      :param rids: Feature identifiers.
      :param \*args: Compatibility
      :param \*\*kwargs: Compatibility

      :returns: :class:`.RepTaxonomy`


   .. method:: get_taxonomy_by_id(self, ids: Optional[GenericIdentifier] = None) -> pd.DataFrame

      Get taxonomy :class:`~pandas.DataFrame` by feature `ids`.

      :param ids: Either feature indices or None for all.

      :returns: :class:`pandas.DataFrame` with taxonomy data


   .. method:: merge_duplicated_features(self, **kwargs: Any) -> Optional[Mapper]

      Merge features with duplicated taxonomy.

      :param \*\*kwargs: Compatibility


   .. method:: merge_features_by_rank(self, level: str, **kwargs: Any) -> Optional[Mapper]

      Merge features by taxonomic rank/level

      :param level: Taxonomic rank/level to use for merging.
      :param \*\*kwargs: Compatibility


   .. method:: xrid(self) -> pd.Index
      :property:

      Feature indices as pd.Index



