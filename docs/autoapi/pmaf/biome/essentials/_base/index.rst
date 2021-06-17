:orphan:

:mod:`pmaf.biome.essentials._base`
==================================

.. py:module:: pmaf.biome.essentials._base


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.essentials._base.EssentialBackboneBase



.. py:class:: EssentialBackboneBase(_controller: Optional[EssentialControllerBackboneMetabse] = None, **kwargs: Any)

   Bases: :class:`pmaf.biome._base.BiomeBackboneBase`, :class:`pmaf.biome.essentials._metakit.EssentialBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.essentials._base.EssentialBackboneBase
      :parts: 1

   Base class for `essentials`.

   Constructor of the `essentials` base class.

   :param _controller: Instance of :class:`~pmaf.biome.essentials._controller.EssentialsController`
                       or None to create an independent `essential`.
   :param \*\*kwargs: Compatibility

   .. method:: controller(self) -> EssentialControllerBackboneMetabse
      :property:

      Return the active :class:`pmaf.biome.essentials._controller.EssentialsController` instance.


   .. method:: is_buckled(self) -> bool
      :property:

      Is current `essentials` instance is mounted or not.


   .. method:: is_mounted(self) -> bool
      :property:

      True if current `essentials` instance is mounted or not.



