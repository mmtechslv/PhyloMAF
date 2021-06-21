from pmaf.database._core._base import DatabaseBase
from pmaf.database._core._tax_base import DatabaseTaxonomyMixin
from pmaf.database._core._seq_base import DatabaseSequenceMixin
import numpy as np
from typing import Optional
from pmaf.internal._typing import AnyGenericIdentifier

class ExportableDatabase(DatabaseTaxonomyMixin,DatabaseSequenceMixin,DatabaseBase):
    """Dummy Class that represent two exportable mixins."""
    pass

# TODO: When and if Intersection[t1,t2] type hint that was described in `PEP 483
#  <https://www.python.org/dev/peps/pep-0483/#id10>` discussed on `GitHub typing
#  issue #213 <https://github.com/python/typing/issues/213>` then change
#  ExportableDatabase to type hintIntersection[DatabaseTaxonomyMixin,
#  DatabaseSequenceMixin,DatabaseBase]

def export_database_by_rid(
    database: ExportableDatabase,
    output_fasta_fp: str,
    output_tax_fp: str,
    ids: Optional[AnyGenericIdentifier] = None,
    chunksize: int = 100,
):
    """Export database into QIIME formatted files.

    Parameters
    ----------
    database :
        Database to extract data from.
    output_fasta_fp :
        Path to output FASTA file
    output_tax_fp :
        Path to output taxonomy file (QIIME/Greengenes notation)
    ids :
        Reference identifiers to extract. Default is None to extract all.
    chunksize :
        Process data in chunks. Default is 100 records per chunk.
    database: ExportableDatabase :
        
    output_fasta_fp: str :
        
    output_tax_fp: str :
        
    ids: Optional[AnyGenericIdentifier] :
         (Default value = None)
    chunksize: int :
         (Default value = 100)

    Returns
    -------

    """
    if not isinstance(database, DatabaseBase):
        raise TypeError("`database` is invalid.")
    if not isinstance(database, DatabaseTaxonomyMixin) and isinstance(
        database, DatabaseSequenceMixin
    ):
        raise ValueError("`database` does not have taxonomy and sequences.")
    if database.storage_manager.state != 1:
        raise RuntimeError("Storage is closed.")
    if ids is None:
        target_ids = np.asarray(database.xrid)
    else:
        target_ids = np.asarray(ids)
    multiseq_gen = database.get_sequence_by_rid(
        target_ids, iterator=True, chunksize=chunksize
    )
    _, first_multiseq = next(multiseq_gen)
    first_multiseq.write(output_fasta_fp, mode="w")
    for _, multiseq in multiseq_gen:
        multiseq.write(output_fasta_fp, mode="a")
    taxonomy_df = database.get_lineage_by_rid(
        target_ids, missing_rank=True, desired_ranks=database.avail_ranks
    )
    taxonomy_df.to_csv(output_tax_fp, header=False, sep="\t")




