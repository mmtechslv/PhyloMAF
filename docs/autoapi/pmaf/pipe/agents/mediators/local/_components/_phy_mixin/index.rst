:orphan:

:mod:`pmaf.pipe.agents.mediators.local._components._phy_mixin`
==============================================================

.. py:module:: pmaf.pipe.agents.mediators.local._components._phy_mixin


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.mediators.local._components._phy_mixin.MediatorLocalPhylogenyMixin



.. py:class:: MediatorLocalPhylogenyMixin(database, phy_method='infer', phy_sub_nodes=True, phy_ignore_tips=False, phy_refrep='tid', **kwargs)

   Bases: :class:`pmaf.pipe.agents.mediators.local._base.MediatorLocalBase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorPhylogenyMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: PHYLO_EXTRACT_METHODS
      :annotation: = ['infer', 'prune']

      

   .. method:: get_identifier_by_phylogeny(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_phylogeny_by_identifier(self, docker, factor, **kwargs)

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:



