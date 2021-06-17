:orphan:

:mod:`pmaf.pipe.agents.mediators.local._components._seq_mixin`
==============================================================

.. py:module:: pmaf.pipe.agents.mediators.local._components._seq_mixin


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.pipe.agents.mediators.local._components._seq_mixin.MediatorLocalSequenceMixin



.. py:class:: MediatorLocalSequenceMixin(database, seq_method='refseq', seq_subs=False, seq_aligner=None, seq_force_align=False, seq_refrep='tid', seq_filter_method=None, seq_filter_value=None, **kwargs)

   Bases: :class:`pmaf.pipe.agents.mediators.local._base.MediatorLocalBase`, :class:`pmaf.pipe.agents.mediators._metakit.MediatorSequenceMetabase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. attribute:: SEQ_EXTRACT_METHODS
      :annotation: = ['refseq', 'consensus']

      

   .. attribute:: SEQ_FILTER_METHODS
      :annotation: = ['random', 'tab']

      

   .. method:: get_identifier_by_sequence(self, docker, factor, **kwargs)
      :abstractmethod:

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:


   .. method:: get_sequence_by_identifier(self, docker, factor, **kwargs)

      :param docker:
      :param factor:
      :param \*\*kwargs:

      Returns:



