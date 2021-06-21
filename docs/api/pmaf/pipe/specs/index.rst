:mod:`pmaf.pipe.specs`
======================

.. py:module:: pmaf.pipe.specs


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.specs.SpecIA
   pmaf.pipe.specs.SpecIP
   pmaf.pipe.specs.SpecIS
   pmaf.pipe.specs.SpecIT
   pmaf.pipe.specs.SpecTI
   pmaf.pipe.specs.SpecTP
   pmaf.pipe.specs.SpecTS
   pmaf.pipe.specs.SpecTSBP
   pmaf.pipe.specs.SpecTSPBP



Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.pipe.specs.ForgeSpec


.. py:class:: SpecIA(mediator, factor, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._primitive._base.SpecificationPrimitiveBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: inlet(self)
      :property:


   .. method:: outlet(self)
      :property:


   .. method:: verify_docker(self, docker)

      :param docker:

      Returns:



.. py:class:: SpecIP(mediator, factor, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._primitive._base.SpecificationPrimitiveBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: inlet(self)
      :property:


   .. method:: outlet(self)
      :property:


   .. method:: verify_docker(self, docker)

      :param docker:

      Returns:



.. py:class:: SpecIS(mediator, factor, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._primitive._base.SpecificationPrimitiveBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: inlet(self)
      :property:


   .. method:: outlet(self)
      :property:


   .. method:: verify_docker(self, docker)

      :param docker:

      Returns:



.. py:class:: SpecIT(mediator, factor, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._primitive._base.SpecificationPrimitiveBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: inlet(self)
      :property:


   .. method:: outlet(self)
      :property:


   .. method:: verify_docker(self, docker)

      :param docker:

      Returns:



.. py:class:: SpecTI(mediator, factor, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._primitive._base.SpecificationPrimitiveBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: inlet(self)
      :property:


   .. method:: outlet(self)
      :property:


   .. method:: verify_docker(self, docker)

      :param docker:

      Returns:



.. py:class:: SpecTP(*args, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._composite._base.SpecificationCompositeBase`

   Initialize self.  See help(type(self)) for accurate signature.


.. py:class:: SpecTS(*args, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._composite._base.SpecificationCompositeBase`

   Initialize self.  See help(type(self)) for accurate signature.


.. py:class:: SpecTSBP(*args, tree_builder, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._composite._base.SpecificationCompositeBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: outlet(self)
      :property:



.. py:class:: SpecTSPBP(*args, branch_estimator, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._composite._base.SpecificationCompositeBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: outlet(self)
      :property:



.. function:: ForgeSpec(name, *inters)

   :param name:
   :param \*inters:

   Returns:


