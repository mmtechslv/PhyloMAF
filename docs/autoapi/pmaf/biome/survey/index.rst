:mod:`pmaf.biome.survey`
========================

.. py:module:: pmaf.biome.survey


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.survey.BiomeSurvey



.. py:class:: BiomeSurvey(assembiles: Optional[Sequence[BiomeAssembly]] = None, *args: Any, aggfunc: Union[AggFunc, Tuple[AggFunc, AggFunc], Dict[Union[str, int], Union[AggFunc, Dict[Union[EssentialBackboneMetabase, None], AggFunc]]]] = 'mean', groupby: Union[str, Tuple[str, str], Dict[Union[int, str], str]] = 'label', **kwargs: Any)

   Bases: :class:`pmaf.biome._base.BiomeBackboneBase`, :class:`pmaf.biome.survey._metakit.BiomeSurveyBackboneMetabase`

   Assembly-like Survey class for merging instances of :class:`~pmaf.biome.assembly._assembly.BiomeAssembly`

   This class performs merging/pooling of _multiple independent studies
   or instances of :class:`~pmaf.biome.essentials.EssentialBackboneBase` (essentials) into single
   instance of :class:`~pmaf.biome.survey._assembly.BiomeAssembly` -like class :class:`~pmaf.biome.survey._survey.BiomeSurvey`.

   :param assembiles: *essentials* to pool.
   :param \*args: Unpacked *essentials* to pool. (Convenience)
   :param aggfunc: Aggregation method. Parameter take _multiple variations of
                   aggregation approach. If `str` or `Callable` then `aggfunc` will be
                   applied to both axes(feature and sample) and any *essentials*
                   regardless of its type. To apply aggregation for each axis separately
                   use `tuple` (for example,  *aggfunc=('sum', 'mean'))* where first
                   aggregation method refers to feature axis and second to sample axis.
                   To apply more complex aggregation use Dict type, where keys refer to axis
                   like *0/feature* for feature axis or *1/sample* for sample axis. Values
                   of the dictionary can refer to two approaches. First is when values are
                   simply `str` or `Callable`, which is similar to using `tuple`. Second,
                   is when using values with type `Dict` where dictionary values are
                   `str` or `Callable` refer to aggregating function and keys are types or
                   class of *essentials* (must have base abstract class :class:`~pmaf.biome.essentials._metakit.EssentialBackboneMetabase` ).
                   Using this method each type of *essential* will be processed differently
                   among instances of *assemblies*. Lastly, when using approach like
                   Dict[axis, Dict[*essential-type*,*agg-func*]] using `None` for one of
                   *essential-type* keys will assume that it refers to all *remaining-types*.
   :param groupby: Grouping method. Parameters take _multiple variations
                   similar to `aggfunc`. Variations are same as `aggfunc` with exception
                   that values can be either `label` for both feature-axis or sample-axis
                   like *groupby='label'* or *groupby=(`label`, `label`)* , or *taxonomy*
                   for feature-axis only. Grouping by *taxonomy* will merge features with
                   same consensus lineage.
   :param \*\*kwargs: Compatibility

   .. method:: _repr_appendage__(self)

      Helper for `__repr__` method of class :class:`~pmaf.biome.BiomeBackboneBase`


   .. method:: assemblies(self) -> Tuple[BiomeAssembly]
      :property:

      Tuple of surveyed assemblies


   .. method:: controller(self) -> EssentialsController
      :property:

      :class:`~pmaf.biome.essentials._controller.EssentialsController` of *essentials*


   .. method:: copy(self) -> 'BiomeSurvey'

      Copy of the instance.


   .. method:: essentials(self) -> List[EssentialBackboneMetabase]
      :property:

      List of *essentials*


   .. method:: to_assembly(self) -> BiomeAssembly

      Converts to the :class:`~pmaf.biome.assembly._assembly.BiomeAssembly` instance.


   .. method:: xrid(self) -> GenericIdentifier
      :property:

      Feature identifiers


   .. method:: xsid(self) -> GenericIdentifier
      :property:

      Sample identifiers



