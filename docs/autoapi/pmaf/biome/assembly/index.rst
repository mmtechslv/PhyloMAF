:mod:`pmaf.biome.assembly`
==========================

.. py:module:: pmaf.biome.assembly


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.assembly.BiomeAssembly



.. py:class:: BiomeAssembly(essentials: Optional[Sequence[EssentialBackboneMetabase]] = None, *args: Optional[EssentialBackboneMetabase], curb: Union[str, EssentialBackboneMetabase, None] = None, copy: bool = True, **kwargs: Any)

   Bases: :class:`pmaf.biome._base.BiomeBackboneBase`, :class:`pmaf.biome.assembly._metakit.BiomeAssemblyBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.assembly.BiomeAssembly
      :parts: 1

   Assembly class for interconnecting and containing `essentials`

   Constructor for :class:`.BiomeAssembly`

   :param essentials: Single or _multiple instances of `essentials`
   :param \*args: Instances of `essentials`
   :param curb: Set limiting instance of `essentials` that will be used to
                subset remaining essentials to identical axes.
                If set tp 'intersect' intersection will be used as limiter.
   :param copy: Whether to copy `essentials` or not.
   :param \*\*kwargs: Compatibility.

   .. method:: _repr_appendage__(self)

      Helper for `__repr__` method of class :class:`~pmaf.biome.BiomeBackboneBase`


   .. method:: add_essentials(self, *args: EssentialBackboneMetabase, curb: Optional[str] = None, copy: bool = True) -> None

      Add instance of `essentials` to the current instance of :class:`.BiomeAssembly`

      :param \*args: Instances of `essentials` to add.
      :param curb: Can be either `intersect` or None.
      :param copy: Whether to copy essentials or not.


   .. method:: controller(self) -> EssentialsController
      :property:

      :class:`~pmaf.biome.essentials._controller.EssentialsController` of `essentials`


   .. method:: copy(self) -> 'BiomeAssembly'

      Copy of the instance.


   .. method:: essentials(self) -> List[EssentialBackboneMetabase]
      :property:

      List of `essentials`


   .. method:: export(self, output_dir: str, prefix: Optional[str] = None, as_otu_table: bool = False, sep: str = ',', **kwargs: Any) -> None

      Export data from assembly to the directory.

      :param output_dir: Export directory path.
      :param prefix: Prefix for output files.
      :param as_otu_table: Create OTU-table from :class:`~pmaf.biome.essentials._frequency.FrequncyTable` and  :class:`~pmaf.biome.essentials._taxonomy.RepTaxonomy`
      :param sep: Delimiter
      :param \*\*kwargs: Compatibility.


   .. method:: get_subset(self, rids: Optional[GenericIdentifier] = None, sids: Optional[GenericIdentifier] = None, **kwargs) -> 'BiomeAssembly'

      Get subset of the :class:`.BiomeAssembly`.

      :param rids: Feature Identifiers
      :param sids: Sample Identifiers
      :param \*\*kwargs: Compatibility

      :returns: Instance of :class:`.BiomeAssembly`.


   .. method:: to_otu_table(self, *args: Any, **kwargs: Any) -> pd.DataFrame

      Crate an OTU-table :class:`~pandas.DataFrame`

      :param \*args: Compatibility.
      :param \*\*kwargs: Compatibility

      :returns: :class:`~pandas.DataFrame` of OTU-table


   .. method:: write_otu_table(self, output_fp: str, *args: Any, sep: str = ',', **kwargs: Any) -> None

      Write OTU-table to the file.

      :param output_fp: Output filepath
      :param \*args: Compatibility
      :param sep: Delimiter
      :param \*\*kwargs: Compatibility


   .. method:: xrid(self) -> GenericIdentifier
      :property:

      Feature identifiers


   .. method:: xsid(self) -> GenericIdentifier
      :property:

      Sample identifiers



