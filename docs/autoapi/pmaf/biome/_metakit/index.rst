:orphan:

:mod:`pmaf.biome._metakit`
==========================

.. py:module:: pmaf.biome._metakit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome._metakit.BiomeBackboneMetabase
   pmaf.biome._metakit.BiomeFeatureMetabase
   pmaf.biome._metakit.BiomeSampleMetabase



.. py:class:: BiomeBackboneMetabase

   Bases: :class:`abc.ABC`

   .. autoapi-inheritance-diagram:: pmaf.biome._metakit.BiomeBackboneMetabase
      :parts: 1

   .. method:: _repr_appendage__(self)
      :abstractmethod:


   .. method:: copy(self)
      :abstractmethod:


   .. method:: metadata(self)
      :property:


   .. method:: name(self)
      :property:


   .. method:: shape(self)
      :property:



.. py:class:: BiomeFeatureMetabase

   Bases: :class:`pmaf.biome._metakit.BiomeBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome._metakit.BiomeFeatureMetabase
      :parts: 1

   .. method:: get_feature_ids(self, dtype: Optional[DTypeLike] = None)

      This function and its sample twin is a rescue method to fix RepPhylogeny index problem.

      :param dtype: Type to cast into

      :returns: :class:`~numpy.ndarray` of type `dtype`


   .. method:: xrid(self)
      :property:



.. py:class:: BiomeSampleMetabase

   Bases: :class:`pmaf.biome._metakit.BiomeBackboneMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome._metakit.BiomeSampleMetabase
      :parts: 1

   .. method:: get_sample_ids(self, dtype: Optional[DTypeLike] = None)

      This function and its sample twin is a rescue method to fix RepPhylogeny index problem.

      :param dtype: Type to cast into

      :returns: :class:`~numpy.ndarray` of type `dtype`


   .. method:: xsid(self)
      :property:



