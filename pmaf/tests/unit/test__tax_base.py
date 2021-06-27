import pytest


def test_get_lineage_by_tid(tdb_greengenes,product_tids_tax_greengenes):
    tids_tax = tdb_greengenes.get_taxonomy_by_tid()
    assert tids_tax.equals(product_tids_tax_greengenes)
