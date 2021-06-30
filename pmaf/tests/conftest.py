import pytest
from pmaf.database import DatabaseGreengenes
import pandas as pd
from os import path
from ._testing_shared import fix_nan_in_frame

TEST_DATA_ROOT = "pmaf/tests/data/"


@pytest.fixture(scope="module")
def tdb_greengenes():
    db = DatabaseGreengenes(
        path.join(TEST_DATA_ROOT, "tdbs/greengenes/gg_13_8_demo.hdf5")
    )
    yield db
    db.close()


@pytest.fixture
def product_tids_tax_greengenes():
    return fix_nan_in_frame(
        pd.read_csv(
            path.join(TEST_DATA_ROOT, "tdbs/greengenes/products/product_tids_tax.csv"),
            index_col=0,
            header=0,
        )
    )


@pytest.fixture
def input_taxonomy_all_ranks():
    return fix_nan_in_frame(
        pd.read_json(
            path.join(TEST_DATA_ROOT, "taxonomy/input_taxonomy_all_ranks_1.json")
        )
    )


@pytest.fixture
def product_generate_lineages_from_taxa_default():
    return pd.read_json(
        path.join(
            TEST_DATA_ROOT, "taxonomy/product_taxonomy_all_ranks_1_GLFT_default.json"
        ),
        typ="series",
    )
