:orphan:

:mod:`pmaf.internal._shared`
============================

.. py:module:: pmaf.internal._shared


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.internal._shared.chunk_generator
   pmaf.internal._shared.cols2ranks
   pmaf.internal._shared.cut_lineages
   pmaf.internal._shared.ensure_list
   pmaf.internal._shared.ensure_new_dir
   pmaf.internal._shared.extract_valid_ranks
   pmaf.internal._shared.generate_lineages_from_taxa
   pmaf.internal._shared.get_datetime
   pmaf.internal._shared.get_package_root
   pmaf.internal._shared.get_rank_upto
   pmaf.internal._shared.get_stats_for_sequence_record_df
   pmaf.internal._shared.indentify_taxon_notation
   pmaf.internal._shared.is_table_taxa_alike
   pmaf.internal._shared.read_csv
   pmaf.internal._shared.sort_ranks
   pmaf.internal._shared.to_array
   pmaf.internal._shared.validate_ranks
   pmaf.internal._shared.write_csv


.. function:: chunk_generator(iterable, chunksize)

   :param iterable:
   :param chunksize:

   Returns:


.. function:: cols2ranks(cols: Sequence[Union[str, int]], ref_ranks: Optional[Sequence[str]] = None) -> Sequence[str]

   Transform columns to ranks based on order.

   :param cols: Original column values.
   :type cols: list or tuple
   :param ref_ranks: Reference ranks to use. Default to None or VALID_RANKS
   :type ref_ranks: None or list or tuple, optional

   :returns: Transformed ranks
   :rtype: list


.. function:: cut_lineages(in_lineages, levels)

   Supplementary function for cutting ranks both ends of lineages with
   Greengenes convention

   :param in_lineages: pandas Series of lineages and IDs as index
   :type in_lineages: pandas.Series
   :param levels: Level to cut. 1 will cut from the beginning of the string.
   :type levels: int

   Negative sign will reverse algorithm and will cut from the end.

   :returns: New lineages
   :rtype: pandas.Series


.. function:: ensure_list(var)

   Makes sure that `var` is a list

   :param var: List like object
   :type var: list like

   :returns: `var` as list
   :rtype: list


.. function:: ensure_new_dir(dir_name)

   Creates new directory if it does not exist. If it does exist then it
   checks if existing directory was generated via this function if it does it
   reads counter prefix in directory name and creates new directory with
   increment

   :param dir_name: Directory name to check
   :type dir_name: str

   :returns: Path to new directory or False.
   :rtype: str|bool


.. function:: extract_valid_ranks(ranks: Sequence[str], ref_ranks: Optional[Sequence[str]] = None)

   Extract real rank values from list-like ranks

   :param ranks: Target ranks to extract from.
   :type ranks: list or tuple
   :param ref_ranks: Ref ranks to use. Default to None or MAIN_RANKS
   :type ref_ranks: None or list or tuple, optional

   :returns: Extracted ranks
   :rtype: None or bool


.. function:: generate_lineages_from_taxa(in_taxa: pd.DataFrame, missing_rank: bool = False, desired_ranks: Union[Sequence[str], bool] = False, drop_ranks: Union[Sequence[str], bool] = False)

   Generate consensus lineages in QIIME convention format from taxonomy
   dataframe like `FeatureTable._internal_taxonomy`

     in_taxa: pandas DataFrame like `FeatureTable._internal_taxonomy`
     missing_rank: If True will generate prefix like `s__` or `d__`  (Default value = False)
     desired_ranks: List of desired ranks to generate. If False then will generate all main ranks (Default value = False)
     drop_ranks: List of ranks to drop from desired ranks. This parameter only useful if `missing_rank` is True (Default value = False):

   :returns: Series with generated consensus lineages and corresponding IDs as Series index


.. function:: get_datetime(datetime_str, format=None)

   :param datetime_str:
   :param format: (Default value = None)

   Returns:


.. function:: get_package_root()


.. function:: get_rank_upto(ranks: Sequence[str], ter_rank: str, include_terminal: bool = False) -> Sequence[str]

   Generates list of ranks from `ranks` terminated at `ter_rank`

   :param ranks: List of ranks
   :type ranks: list
   :param ter_rank: Terminal rank
   :type ter_rank: str
   :param include_terminal: (Default value = False)

   :returns: List of ranks
   :rtype: list


.. function:: get_stats_for_sequence_record_df(sequence_record_df)

   :param sequence_record_df:

   Returns:


.. function:: indentify_taxon_notation(taxon_string)

   Identifies taxonomic notation from `taxon_string` . Currently available
   conventions are Greengenens, sintax and SILVA

   Examples:

   :param taxon_string: String with taxonomy/lineage to test
   :type taxon_string: str

   :returns: 'greengenes' or 'sintax' or 'silva'
   :rtype: str

   >>> test_taxon_string = 'c__Bacilli; o__Lactobacillales; f__Lactobacillaceae; g__Lactobacillus; s__Lactobacillusbrevis'
       >>> print(indentify_taxon_notation(test_taxon_string))
       'greengenes'


.. function:: is_table_taxa_alike(feature_table1, feature_table2)

   This method checks if `feature_table2` instance contains same taxonomy as
   `feature_table1`

   :param feature_table1: First FeatureTable
   :type feature_table1: pmaf._feature.FeatureTable
   :param feature_table2: Second FeatureTable
   :type feature_table2: pmaf._feature.FeatureTable

   :returns: True if taxonomies are same. False otherwise
   :rtype: bool


.. function:: read_csv(file_path, sep=',', quote='"')

   Reads CSV/TSV file and returns content as list

   :param file_path: Path to CSV/TSV the file
   :type file_path: str
   :param sep: Delimiter of CSV/TSV file (Default value = ')
   :type sep: str, optional
   :param quote: Quoting of CSV/TSV file (Default value = '"')
   :type quote: str, optional
   :param ':

   :returns: Content of the CSV/TSV file
   :rtype: list


.. function:: sort_ranks(ranks)

   :param ranks:

   Returns:


.. function:: to_array(data)

   :param data:

   Returns:


.. function:: validate_ranks(ranks: Sequence[str], ref_ranks: Optional[Sequence[str]] = None)

   Validate the ranks based on ref_ranks.

   :param ranks: Target ranks to validate
   :type ranks: list or tuple
   :param ref_ranks: Reference ranks to use. Default to None or MAIN_RANKS
   :type ref_ranks: None or list or tuple
   :param ranks: Sequence[str]:
   :param ref_ranks: Sequence[str]:  (Default value = None)

   :returns: Validation result.
   :rtype: None or bool


.. function:: write_csv(iContent, file_path, sep=',', quote='"')

   Writes content to CSV/TSV file

   :param iContent: Content to write
   :type iContent: list
   :param file_path: Path to CSV/TSV the file
   :type file_path: str
   :param sep: Delimiter of CSV/TSV file (Default value = ')
   :type sep: str, optional
   :param quote: Quoting of CSV/TSV file (Default value = '"')
   :type quote: str, optional
   :param ':

   :returns: True if write was successful. False otherwise
   :rtype: bool


