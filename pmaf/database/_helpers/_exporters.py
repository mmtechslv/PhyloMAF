from pmaf.database._core._base import DatabaseBase
from pmaf.database._core._tax_base import DatabaseTaxonomyMixin
from pmaf.database._core._seq_base import DatabaseSequenceMixin
from pmaf.database._core._phy_base import DatabasePhylogenyMixin
import numpy as np
from typing import Optional
from os import path
from pmaf.internal._typing import AnyGenericIdentifier


class ExportableDatabase(DatabaseTaxonomyMixin, DatabaseSequenceMixin, DatabaseBase):
    """Dummy Class that represent two exportable mixins."""

    pass


# TODO: When and if Intersection[t1,t2] type hint that was described in `PEP 483
#  <https://www.python.org/dev/peps/pep-0483/#id10>` discussed on `GitHub typing
#  issue #213 <https://github.com/python/typing/issues/213>` then change
#  ExportableDatabase to type hintIntersection[DatabaseTaxonomyMixin,
#  DatabaseSequenceMixin,DatabaseBase]


def export_database_by_rid(
    database: ExportableDatabase,
    output_dir: str,
    ids: Optional[AnyGenericIdentifier] = None,
    chunksize: int = 100,
):
    """Export database taxonomy, sequence, alignment and phylogeny into given
    `output_dir` as QIIME formatted files.

    Parameters
    ----------
    database
        Database to extract data from
    output_dir
        Path to output directory
    ids
        Reference :term:`rids` identifiers to extract. Default is None to extract all
    chunksize
        Process data in chunks. Default is 100 records per chunk
    """
    if not isinstance(database, DatabaseBase):
        raise TypeError("`database` is invalid.")
    if not (
        isinstance(database, DatabaseTaxonomyMixin)
        and isinstance(database, DatabaseSequenceMixin)
        and isinstance(database, DatabasePhylogenyMixin)
    ):
        raise ValueError("`database` does not have taxonomy and sequences.")
    if database.storage_manager.state != 1:
        raise RuntimeError("Storage is closed.")
    if ids is None:
        target_ids = np.asarray(database.xrid)
    else:
        target_ids = np.asarray(ids)
    output_fasta_fp = path.join(output_dir, "refseq.fa")
    output_aln_fp = path.join(output_dir, "refaln.fa")
    output_tax_fp = path.join(output_dir, "reftax.txt")
    output_phy_fp = path.join(output_dir, "tree.nwk")
    # Sequences
    multiseq_gen = database.get_sequence_by_rid(
        target_ids, iterator=True, chunksize=chunksize
    )
    _, first_multiseq = next(multiseq_gen)
    first_multiseq.write(output_fasta_fp, mode="w")
    for _, multiseq in multiseq_gen:
        multiseq.write(output_fasta_fp, mode="a")
    # Alignments
    multiseq_aln_gen = database.get_alignment_by_rid(
        target_ids, iterator=True, chunksize=chunksize
    )
    _, first_multiseq_aln = next(multiseq_aln_gen)
    first_multiseq_aln.write(output_aln_fp, mode="w")
    for _, multiseq in multiseq_aln_gen:
        multiseq.write(output_aln_fp, mode="a")
    taxonomy_df = database.get_lineage_by_rid(
        target_ids, missing_rank=True, desired_ranks=database.avail_ranks
    )
    taxonomy_df.to_csv(output_tax_fp, header=False, sep="\t")
    tree = database.prune_tree_by_rid(target_ids)
    tree.write(output_phy_fp)
