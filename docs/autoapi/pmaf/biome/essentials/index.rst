:mod:`pmaf.biome.essentials`
============================

.. py:module:: pmaf.biome.essentials

.. autoapi-nested-parse::

   Essentials (:mod:`pmaf.biome.essentials`)
   =========================================
   .. currentmodule:: pmaf.biome.essentials

   This is primary module that contain `essentials` that work with biome data such as OTU-tables, :mod:`biom` files, representative OTU phylogeny, sequence, taxonomy etc.



Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.essentials.FrequencyTable
   pmaf.biome.essentials.RepPhylogeny
   pmaf.biome.essentials.RepSequence
   pmaf.biome.essentials.RepTaxonomy
   pmaf.biome.essentials.SampleMetadata



.. py:class:: FrequencyTable(frequency: Union[pd.DataFrame, str], skipcols: Union[Sequence[Union[str, int]], str, int] = None, allow_nan: bool = False, **kwargs)

   Bases: :class:`pmaf.biome.essentials._base.EssentialBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialFeatureMetabase`, :class:`pmaf.biome.essentials._metakit.EssentialSampleMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.essentials.FrequencyTable
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



.. py:class:: RepPhylogeny(tree: Union[PhyloTree, TreeEte3Base, StringIO, str], feature_ids: Optional[GenericIdentifier] = None, prune: bool = False, annotation: Union[dict, pd.Series, None] = None, copy: bool = True, ignore_polytomy: bool = False, **kwargs: Any)

   Bases: :class:`pmaf.biome.essentials._base.EssentialBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialFeatureMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.essentials.RepPhylogeny
      :parts: 1

   An `essential` class for handling phylogeny data.

   Constructor for :class:`.RepPhylogeny`

   :param tree: Phylogeny data
   :param feature_ids: Target feature identifiers
   :param prune: Whether to prune for `feature_ids`
   :param annotation: Annotations for tips
   :param copy: Whether to copy the original tree.
                May require long time if tree is large.
   :param ignore_polytomy: Whether to resolve tree polytomy or not.
   :param \*\*kwargs: Compatibility

   .. method:: annotations(self) -> dict
      :property:

      Tip Annotations


   .. method:: copy(self) -> 'RepPhylogeny'

      Copy of the instance.


   .. method:: data(self) -> PhyloTree
      :property:

      Phylogenetic Tree


   .. method:: export(self, output_fp: str, _add_ext: bool = False, **kwargs: Any) -> None

      Exports the Newick formatted phylogenetic tree into specified file.

      :param output_fp: Export filepath
      :param _add_ext: Add file extension or not.
      :param \*\*kwargs: Compatibility


   .. method:: get_annotated_tree(self) -> PhyloTree

      Retrieves annotated tree

      :returns: Annotated tree of class :class:`~pmaf.phylo.tree.PhyloTree`


   .. method:: get_ascii_art(self, annotated: bool = False) -> str

      Creates ASCII art of the tree.

      :param annotated: Whether to create tree with annotated tips or not.

      :returns: String with ASCII art


   .. method:: get_subset(self, rids: Optional[GenericIdentifier] = None, *args, **kwargs: Any) -> 'RepPhylogeny'

      Get subset of the :class:`.RepPhylogeny`.

      :param rids: Feature Identifiers
      :param \*args: Compatibility
      :param \*\*kwargs: Compatibility

      :returns: Instance of :class:`.RepPhylogeny`.


   .. method:: render_art(self, output_fp: str, annotated: bool = False) -> Any

      Renders tree into file.

      :param output_fp: File to render into. File format depends on the extension.
                        For example, .pdf will produce PDF file and
                        while .png will produce PNG file.
      :param annotated: Whether to create tree with annotated tips or not.


   .. method:: resolve_polytomy(self) -> None

      Resolve tree polytomy.


   .. method:: write(self, output_fp: str, mode: str = 'w', **kwargs: Any) -> None

      Writes the Newick tree into specified file.

      :param output_fp: Output filepath
      :param mode: File write mode.
      :param \*\*kwargs: Compatibility


   .. method:: xrid(self) -> GenericIdentifier
      :property:

      Feature identifiers



.. py:class:: RepSequence(sequences: Union[str, MultiSequence, pd.DataFrame, pd.Series], **kwargs: Any)

   Bases: :class:`pmaf.biome.essentials._base.EssentialBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialFeatureMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.essentials.RepSequence
      :parts: 1

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


   .. method:: get_subset(self, rids: Optional[GenericIdentifier] = None, *args: Any, **kwargs: Any) -> 'RepSequence'

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



.. py:class:: RepTaxonomy(taxonomy: Union[pd.DataFrame, pd.Series, str], taxonomy_columns: Union[str, int, Sequence[Union[int, str]]] = None, **kwargs: Any)

   Bases: :class:`pmaf.biome.essentials._base.EssentialBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialFeatureMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.essentials.RepTaxonomy
      :parts: 1

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



.. py:class:: SampleMetadata(samples: Union[pd.DataFrame, str], axis: Union[int, str] = 1, index_col: Union[str, int] = 0, **kwargs: Any)

   Bases: :class:`pmaf.biome.essentials._base.EssentialBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialSampleMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.essentials.SampleMetadata
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



