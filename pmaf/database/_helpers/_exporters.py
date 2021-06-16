from pmaf.database._core._base import DatabaseBase
from pmaf.database._core._tax_base import DatabaseTaxonomyMixin
from pmaf.database._core._seq_base import DatabaseSequenceMixin
from pmaf.database._core._phy_base import DatabasePhylogenyMixin
from pmaf.database._core._acs_base import DatabaseAccessionMixin
import numpy as np

def export_database_by_rid(database, output_fasta_fp, output_tax_fp, ids=None, chunksize=100):
    '''

    Args:
      database: 
      output_fasta_fp: 
      output_tax_fp: 
      ids: (Default value = None)
      chunksize: (Default value = 100)

    Returns:

    '''
    if isinstance(database,DatabaseBase):
        if isinstance(database,DatabaseTaxonomyMixin) and isinstance(database,DatabaseSequenceMixin):
            if database.storage_manager.state == 1:
                if ids is None:
                    target_ids = np.asarray(database.xrid)
                else:
                    target_ids = np.asarray(ids)
                multiseq_gen = database.get_sequence_by_rid(target_ids, iterator=True, chunksize=chunksize)
                _, first_multiseq = next(multiseq_gen)
                first_multiseq.write(output_fasta_fp, mode='w')
                for _, multiseq in multiseq_gen:
                    multiseq.write(output_fasta_fp, mode='a')
                taxonomy_df = database.get_lineage_by_rid(target_ids,missing_rank=True,desired_ranks=database.avail_ranks)
                taxonomy_df.to_csv(output_tax_fp, header=False, sep='\t')
            else:
                raise RuntimeError('Storage is closed.')
        else:
            raise ValueError('`database` does not have taxonomy and sequences.')
    else:
        raise TypeError('`database` is invalid.')
