:orphan:

:mod:`pmaf.biome.assembly._metakit`
===================================

.. py:module:: pmaf.biome.assembly._metakit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.biome.assembly._metakit.BiomeAssemblyBackboneMetabase



.. py:class:: BiomeAssemblyBackboneMetabase

   Bases: :class:`pmaf.biome._metakit.BiomeFeatureMetabase`, :class:`pmaf.biome._metakit.BiomeSampleMetabase`

   .. autoapi-inheritance-diagram:: pmaf.biome.assembly._metakit.BiomeAssemblyBackboneMetabase
      :parts: 1

   .. method:: add_essentials(self, *args)
      :abstractmethod:

      :param \*args:

      Returns:


   .. method:: controller(self)
      :property:


   .. method:: essentials(self)
      :property:


   .. method:: export(self, output_dir, *args, **kwargs)
      :abstractmethod:

      :param output_dir:
      :param \*args:
      :param \*\*kwargs:

      Returns:


   .. method:: get_subset(self, *args, **kwargs)
      :abstractmethod:

      :param \*args:
      :param \*\*kwargs:

      Returns:


   .. method:: to_otu_table(self, *args, **kwargs)
      :abstractmethod:

      :param \*args:
      :param \*\*kwargs:

      Returns:


   .. method:: write_otu_table(self, output_fp, *args, **kwargs)
      :abstractmethod:

      :param output_fp:
      :param \*args:
      :param \*\*kwargs:

      Returns:



