import pytest
from pmaf.database import DatabaseGreengenes
import pandas as pd


@pytest.fixture(scope="module")
def tdb_greengenes():
    db = DatabaseGreengenes("pmaf/tests/data/tdbs/greengenes/gg_13_8_demo.hdf5")
    yield db
    db.close()


@pytest.fixture
def product_tids_tax_greengenes():
    return pd.read_csv(
        "pmaf/tests/data/tdbs/greengenes/products/product_tids_tax.csv", index_col=0, header=0
    ).replace({pd.NA: None})
