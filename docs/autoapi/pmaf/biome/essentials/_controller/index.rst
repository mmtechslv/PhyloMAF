:orphan:

:mod:`pmaf.biome.essentials._controller`
========================================

.. py:module:: pmaf.biome.essentials._controller


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.essentials._controller.EssentialsController



.. py:class:: EssentialsController(remount: bool = False, **kwargs)

   Bases: :class:`pmaf.biome.essentials._metakit.EssentialControllerBackboneMetabse`

   Controller for `essentials` working in hand with :class:`~pmaf.biome.assembly.BiomeAssembly`.

   Controller constructor

   :param remount: Force remount
   :param \*\*kwargs: Compatibility

   .. method:: count(self) -> int
      :property:

      Total controlled essentials.


   .. method:: essentials(self) -> List
      :property:

      Get controlled essentials.


   .. method:: has_essential_by_types(self, *args) -> bool

      Helper function that checks if `essentials` in `*args` are controlled via current :class:`.EssentialsController` instance.

      :param \*args: Unpacked elements of :class:`~pmaf.biome.essentials._base.EssentialBackboneBase`

      :returns: Check result.


   .. method:: insert_essential(self, essential: EssentialBackboneMetabase) -> None

      Add instance of `essentials` to the controller.

      :param essential: Instance of :class:`~pmaf.biome.essentials._metakit.EssentialBackboneMetabase`


   .. method:: reflect_action(self, source: EssentialBackboneMetabase, method: str, value: Any, **kwargs) -> dict

      Reflect or mirror the action to controlled instances of `essentials`.

      :param source: Instance of :class:`~pmaf.biome.essentials._base.EssentialBackboneBase` where the action is coming from.
      :param method: Name of the method to be reflected.
      :param value: Value to be passed to mirroring functions. Eg. ids to be removed.
      :param \*\*kwargs: Remaining parameters passed to mirroring function.

      :returns: Dictionary with results for each `essential`


   .. method:: state(self) -> bool
      :property:

      Is controller active.


   .. method:: take_essential_by_type(self, type: Any) -> Optional[EssentialBackboneMetabase]

      Get controlled essential by type.

      :param type: Class of `essential` to retrieve.

      :returns: Instance of `essential`


   .. method:: verify_essential(self, essential: EssentialBackboneMetabase, check_axis: bool = True, check_mount: bool = True) -> bool

      Validates the essentials instance.

      :param essential: Instance of :class:`~pmaf.biome.essentials._metakit.EssentialBackboneMetabase` to validate.
      :param check_axis: Whether to check if axes are compatible with active essential instances.
      :param check_mount: Whether to check if the instance is already mounted

      :returns: Result of validation.
      :rtype: bool


   .. method:: xrid(self) -> GenericIdentifier
      :property:

      Feature axis of controlled essentials.


   .. method:: xsid(self) -> GenericIdentifier
      :property:

      Sample axis of controlled essentials.



