:orphan:

:mod:`pmaf.pipe.agents.dockers._base`
=====================================

.. py:module:: pmaf.pipe.agents.dockers._base


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.dockers._base.DockerBase



.. py:class:: DockerBase(_data_dict, _valid_types, name=None, metadata=None, _transit=None, **kwargs)

   Bases: :class:`pmaf.pipe.agents.dockers._metakit.DockerBackboneMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: count(self)
      :property:


   .. method:: data(self)
      :property:


   .. method:: empty(self)
      :property:


   .. method:: get_iterator(self, indices=None, exclude_missing=False)

      :param indices: (Default value = None)
      :param exclude_missing: (Default value = False)

      Returns:


   .. method:: get_subset(self, indices=None, exclude_missing=False)

      :param indices: (Default value = None)
      :param exclude_missing: (Default value = False)

      Returns:


   .. method:: index(self)
      :property:


   .. method:: metadata(self)
      :property:


   .. method:: missing(self)
      :property:


   .. method:: name(self)
      :property:


   .. method:: singleton(self)
      :property:


   .. method:: valid(self)
      :property:


   .. method:: wrap_meta(self)



