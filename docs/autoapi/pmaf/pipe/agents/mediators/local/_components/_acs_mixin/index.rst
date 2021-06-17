:orphan:

:mod:`pmaf.pipe.agents.mediators.local._components._acs_mixin`
==============================================================

.. py:module:: pmaf.pipe.agents.mediators.local._components._acs_mixin


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.mediators.local._components._acs_mixin.MediatorLocalAccessionMixin



.. py:class:: MediatorLocalAccessionMixin(database, acs_refrep='tid', acs_sub_nodes=False, acs_filter_method=None, acs_filter_value=None, **kwargs)

   Bases: :class:`pmaf.pipe.agents.mediators.local._base.MediatorLocalBase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorAccessionMetabase`

   .. autoapi-inheritance-diagram:: pmaf.pipe.agents.mediators.local._components._acs_mixin.MediatorLocalAccessionMixin
      :parts: 1

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: ACS_FILTER_METHODS
      :annotation: = ['random', 'first']

      

   .. method:: get_accession_by_identifier(self, docker, factor, **kwargs)

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_identifier_by_accession(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:



