:orphan:

:mod:`pmaf.remote._entrez._base`
================================

.. py:module:: pmaf.remote._entrez._base


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pmaf.remote._entrez._base.EntrezBase



Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.remote._entrez._base.control_request_runtime


.. py:class:: EntrezBase(email, api_key=None, tool='PhyloMAF')

   Bases: :class:`pmaf.remote._entrez._metakit.EntrezBackboneMetabase`, :class:`pmaf.remote._entrez._base_blocks.IdiomaticBase`

   Initialize self.  See help(type(self)) for accurate signature.

   .. method:: check_init(self)


   .. method:: get_request_logs(self)


   .. method:: state(self)
      :property:



.. function:: control_request_runtime(method_pass)

   :param method_pass:

   Returns:


