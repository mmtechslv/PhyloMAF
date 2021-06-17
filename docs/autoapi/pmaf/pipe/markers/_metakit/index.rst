:orphan:

:mod:`pmaf.pipe.markers._metakit`
=================================

.. py:module:: pmaf.pipe.markers._metakit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.markers._metakit.MarkerBackboneMetabase



.. py:class:: MarkerBackboneMetabase

   Bases: :class:`abc.ABC`

   .. autoapi-inheritance-diagram:: pmaf.pipe.markers._metakit.MarkerBackboneMetabase
      :parts: 1

   .. method:: compute(self)
      :abstractmethod:


   .. method:: embed_specs(self, method, input, outlet, name, description)
      :abstractmethod:

      :param method:
      :param input:
      :param outlet:
      :param name:
      :param description:

      Returns:


   .. method:: inlet(self)
      :property:


   .. method:: input(self)
      :property:


   .. method:: metadata(self)
      :property:


   .. method:: name(self)
      :property:


   .. method:: next(self)
      :abstractmethod:


   .. method:: outlet(self)
      :property:


   .. method:: output(self)
      :property:


   .. method:: tasks(self)
      :property:


   .. method:: upcoming(self)
      :property:



