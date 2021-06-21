:orphan:

:mod:`pmaf.biome._base`
=======================

.. py:module:: pmaf.biome._base


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome._base.BiomeBackboneBase



.. py:class:: BiomeBackboneBase(metadata: Optional[dict] = None, name: Optional[str] = None, **kwargs: Any)

   Bases: :class:`pmaf.biome._metakit.BiomeBackboneMetabase`

   Base class for all biome classes.

   Constructor for `essentials` base

   :param metadata: Metadata of `essential` instance.
   :param name: Name/Label of `essential` instance
   :param \*\*kwargs: Compatibility.

   .. method:: metadata(self)
      :property:

      The `essential` instance metadata.


   .. method:: name(self)
      :property:

      The `essential` instance name.


   .. method:: shape(self) -> Shape
      :property:

      Return the shape/size of the `essential` instance.

      :returns: Tuple with shape



