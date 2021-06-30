import pytest
from pmaf.internal._shared import generate_lineages_from_taxa


def test_generate_lineages_from_taxa(
    input_taxonomy_all_ranks, product_generate_lineages_from_taxa_default
):
    product = generate_lineages_from_taxa(input_taxonomy_all_ranks)
    should_product = product_generate_lineages_from_taxa_default
    assert product.equals(should_product)
