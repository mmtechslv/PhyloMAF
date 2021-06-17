:orphan:

:mod:`pmaf.pipe.specs._metakit`
===============================

.. py:module:: pmaf.pipe.specs._metakit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.specs._metakit.SpecificationBackboneMetabase
   pmaf.pipe.specs._metakit.SpecificationCompositeMetabase
   pmaf.pipe.specs._metakit.SpecificationPrimitiveMetabase



.. py:class:: SpecificationBackboneMetabase(*args, **kwargs)

   Bases: :class:`abc.ABC`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: factor(self)
      :property:


   .. method:: fetch(self, data)
      :abstractmethod:

      :param data:

      Returns:


   .. method:: inlet(self)
      :property:


   .. method:: outlet(self)
      :property:


   .. method:: state(self)
      :property:


   .. method:: steps(self)
      :property:


   .. method:: verify_docker(self, docker)
      :abstractmethod:

      :param docker:

      Returns:



.. py:class:: SpecificationCompositeMetabase(*args, **kwargs)

   Bases: :class:`pmaf.pipe.specs._metakit.SpecificationBackboneMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: specs(self)
      :property:



.. py:class:: SpecificationPrimitiveMetabase(*args, **kwargs)

   Bases: :class:`pmaf.pipe.specs._metakit.SpecificationBackboneMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: miner(self)
      :property:



