:orphan:

:mod:`pmaf.database._shared._common`
====================================

.. py:module:: pmaf.database._shared._common


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   pmaf.database._shared._common.explode_element_columns
   pmaf.database._shared._common.filter_elements_by
   pmaf.database._shared._common.filter_interx_elements
   pmaf.database._shared._common.get_element_index_type
   pmaf.database._shared._common.get_element_mode
   pmaf.database._shared._common.get_element_type
   pmaf.database._shared._common.missing_to_none
   pmaf.database._shared._common.to_mode
   pmaf.database._shared._common.verify_tax_format


.. data:: DATABASE_HDF5_STRUCT
   

   

.. function:: explode_element_columns(db_summary, element_key)

   :param db_summary:
   :param element_key:

   Returns:


.. function:: filter_elements_by(startswith, exclude=[])

   :param startswith:
   :param exclude: (Default value = [])

   Returns:


.. function:: filter_interx_elements(element_key_list)

   :param element_key_list:

   Returns:


.. function:: get_element_index_type(element_key)

   :param element_key:

   Returns:


.. function:: get_element_mode(element_key)

   :param element_key:

   Returns:


.. function:: get_element_type(element_key)

   :param element_key:

   Returns:


.. function:: missing_to_none(target_pd_data)

   :param target_pd_data:

   Returns:


.. function:: to_mode(result_obj, mode='array', order=None)

   :param result_obj:
   :param mode: (Default value = 'array')
   :param order: (Default value = None)

   Returns:


.. function:: verify_tax_format(tax_format)

   :param tax_format:

   Returns:


