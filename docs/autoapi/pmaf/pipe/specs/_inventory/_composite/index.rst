:orphan:

:mod:`pmaf.pipe.specs._inventory._composite`
============================================

.. py:module:: pmaf.pipe.specs._inventory._composite


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.specs._inventory._composite.SpecTP
   pmaf.pipe.specs._inventory._composite.SpecTS
   pmaf.pipe.specs._inventory._composite.SpecTSBP
   pmaf.pipe.specs._inventory._composite.SpecTSPBP



Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.pipe.specs._inventory._composite.ForgeSpec


.. py:class:: SpecTP(*args, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._composite._base.SpecificationCompositeBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.specs._inventory._composite.SpecTP
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.


.. py:class:: SpecTS(*args, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._composite._base.SpecificationCompositeBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.specs._inventory._composite.SpecTS
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.


.. py:class:: SpecTSBP(*args, tree_builder, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._composite._base.SpecificationCompositeBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.specs._inventory._composite.SpecTSBP
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: outlet(self)
      :property:



.. py:class:: SpecTSPBP(*args, branch_estimator, **kwargs)

   Bases: :class:`pmaf.pipe.specs._inventory._composite._base.SpecificationCompositeBase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.specs._inventory._composite.SpecTSPBP
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: outlet(self)
      :property:



.. function:: ForgeSpec(name, *inters)

   :param name:
   :param \*inters:

   Returns:


