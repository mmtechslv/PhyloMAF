:orphan:

:mod:`pmaf.biome.survey._shared`
================================

.. py:module:: pmaf.biome.survey._shared


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.biome.survey._shared.mergeFrequencyTable
   pmaf.biome.survey._shared.mergeRepTaxonmy
   pmaf.biome.survey._shared.mergeSampleMetadata
   pmaf.biome.survey._shared.parse_assembly_maps


.. function:: mergeFrequencyTable(feature_groupby: str, sample_groupby: str, features_map: pd.DataFrame, samples_map: pd.DataFrame, essentials_map: Dict[Type[AnyBiomeEssential], Dict[str, AnyBiomeEssential]], aggfunc_dict: Dict[Type[AnyBiomeEssential], int]) -> FrequencyTable

   Function that merges data of `essentials` of type :class:`~pmaf.biome.essentials._metakit.EssentialFeatureMetabase`

   :param feature_groupby: Group feature axis by: `index`, `label` or `taxonomy`
   :param sample_groupby: Group sample axis by `index`, `label`
   :param features_map: Produced `features_map` by :meth:`.parse_assembly_maps` function
   :param samples_map: Produced `samples_map` by :meth:`.parse_assembly_maps` function
   :param essentials_map: Complete map of `essentials` to be merged.
   :param aggfunc_dict: Map that provide aggregation instructions.

   :returns: Aggregated :class:`~pmaf.biome.essentials._frequency.FrequencyTable`


.. function:: mergeRepTaxonmy(feature_groupby: str, features_map: pd.DataFrame, essentials_map: Dict[Type[AnyBiomeEssential], Dict[str, AnyBiomeEssential]], aggfunc_dict: Dict[Type[AnyBiomeEssential], int]) -> RepTaxonomy

   Function that merges data of `essentials` of type :class:`~pmaf.biome.essentials._metakit.EssentialFeatureMetabase`

   :param feature_groupby: Group feature axis by: `index`, `label` or `taxonomy`
   :param features_map: Produced `features_map` by :meth:`.parse_assembly_maps` function
   :param essentials_map: Complete map of `essentials` to be merged.
   :param aggfunc_dict: Map that provide aggregation instructions.

   :returns: Aggregated :class:`~pmaf.biome.essentials._taxonomy.RepTaxonomy`


.. function:: mergeSampleMetadata(sample_groupby: str, samples_map: pd.DataFrame, essentials_map: Dict[Type[AnyBiomeEssential], Dict[str, AnyBiomeEssential]], aggfunc_dict: Dict[Type[AnyBiomeEssential], int]) -> SampleMetadata

   Function that merges data of `essentials` of type :class:`~pmaf.biome.essentials._metakit.EssentialSampleMetabase`

   :param sample_groupby: Group sample axis by `index`, `label`
   :param samples_map: Produced `samples_map` by :meth:`.parse_assembly_maps` function
   :param essentials_map: Complete map of `essentials` to be merged.
   :param aggfunc_dict: Map that provide aggregation instructions.

   :returns: Aggregated :class:`~pmaf.biome.essentials._samplemeta.SampleMetadata`


.. function:: parse_assembly_maps(feature_groupby: str, sample_groupby: str, assembly_map: Dict[str, AnyBiomeAssembly]) -> Tuple[pd.DataFrame, pd.DataFrame]

   Function that rearranges `essentials` within `assemblies` in `assembly_map`, into feature and sample axis.

   :param feature_groupby: Group feature axis by: `index`, `label` or `taxonomy`
   :param sample_groupby: Group sample axis by `index`, `label`
   :param assembly_map: Map where keys are `assembly`-labels and values are `assembly` instances.

   :returns:

             - A map where keys are `assembly`-labels and values are `essentials` of type :class:`~pmaf.biome.essentials._metakit.EssentialFeatureMetabase`
             - A map where keys are `assembly`-labels and values are `essentials` of type :class:`~pmaf.biome.essentials._metakit.EssentialSampleMetabase`


