import os
import pandas as pd
import numpy as np
from itertools import chain
from pmaf.internal._extensions._cpython._pmafc_extension._helper import make_sequence_record_tuple
from pmaf.internal.io._seq import SequenceIO

def read_qiime_taxonomy_map(taxonomy_tsv_fp):
    '''

    Args:
      taxonomy_tsv_fp: 

    Returns:

    '''
    if os.path.exists(taxonomy_tsv_fp):
        with open(taxonomy_tsv_fp, 'r') as map_file:
            tmp_tax_map = pd.read_csv(map_file, sep='\t', index_col=0,header=None)
        if tmp_tax_map.shape[1] != 1:
            raise ValueError('Invalid taxonomy file.')
        tax_map = tmp_tax_map.rename(columns={1:'taxonomy'})
        tax_map.index = tax_map.index.astype(str)
        return tax_map
    else:
        raise FileNotFoundError('Given file does not exists.')

def parse_qiime_taxonomy_map(taxonomy_map_df):
    '''

    Args:
      taxonomy_map_df: 

    Returns:

    '''
    if isinstance(taxonomy_map_df,pd.DataFrame):
        if not (taxonomy_map_df.empty or (taxonomy_map_df.shape[1] != 1)):
            taxonomy_map = taxonomy_map_df.iloc[:, 0]
            zip_list = list(chain(*taxonomy_map.map(lambda lineage: [e.strip().split('__')[0] for e in lineage.split(';') if ('__' in e)]).ravel().tolist()))

            def get_unique(zip_list):
                '''

                Args:
                  zip_list: 

                Returns:

                '''
                seen = set()
                seen_add = seen.add
                return [x for x in zip_list if not (x in seen or seen_add(x))]

            found_levels = get_unique(zip_list)

            def allocator(lineage, levels):
                '''

                Args:
                  lineage: 
                  levels: 

                Returns:

                '''
                taxa_dict = {e[0]: e[1] for e in [e.strip().split('__') for e in lineage.split(';') if ('__' in e)]}  # Anonymous function that explodes lineage into dictionary
                taxa_dict_allowed = {rank: taxa_dict[rank] for rank in taxa_dict.keys() if rank in levels}  # Drops forbidden ranks
                # Following loop sets unavailable ranks to '', which is necessary for generating taxonomy sheet
                for key in levels:
                    if not (key in taxa_dict_allowed.keys()):
                        taxa_dict_allowed[key] = ''
                taxa_list_ordered = [taxa_dict_allowed[rank] for rank in levels]  # Sort ranks according to Consts.MAIN_RANKS rank order
                return taxa_list_ordered

            allocator_vectorized = np.vectorize(allocator, excluded=['levels'], otypes=[list])  # Vectorizes function in order gain performance
            master_taxonomy_sheet = pd.DataFrame(index=list(taxonomy_map.index), data=list(allocator_vectorized(lineage=list(taxonomy_map.values), levels=found_levels)), columns=found_levels)
            return master_taxonomy_sheet.applymap(lambda x: None if (x == '' or pd.isna(x)) else x)
        else:
            raise ValueError('DataFrame cannot be empty.')
    else:
        raise TypeError('`taxonomy_map_df` must be pandas DataFrame.')

def parse_qiime_sequence_generator(sequence_fasta_fp,chunk_size,alignment):
    '''

    Args:
      sequence_fasta_fp: 
      chunk_size: 
      alignment: 

    Returns:

    '''
    seqio = SequenceIO(sequence_fasta_fp, ftype='fasta', upper=True)
    max_seq_length = 0
    min_seq_length = 99999 # Assuming no marker sequence can be longer than this
    max_id_length = 0
    max_rows = 0
    for s_id,s_seq in seqio.pull_parser(id=True,description=False,sequence=True):
        seq_length = len(s_seq)
        id_length = len(str(s_id))
        max_seq_length = seq_length if seq_length>max_seq_length else max_seq_length
        min_seq_length = seq_length if seq_length < min_seq_length else min_seq_length
        max_id_length = id_length if id_length > max_id_length else max_id_length
        max_rows = max_rows + 1
    seq_iterator = seqio.pull_parser(id=True,description=False,sequence=True)
    chunk_counter = chunk_size
    next_chunk = True
    first_chunk = True
    df_columns = ['index', 'sequence','length', 'tab'] if not alignment else ['index', 'sequence','length']
    while next_chunk:
        sequences_list = []
        for s_id,s_seq in seq_iterator:
            if not alignment:
                record_list = make_sequence_record_tuple(str(s_id),s_seq)
            else:
                record_list = [str(s_id), s_seq, len(s_seq)]
            if chunk_counter > 1:
                sequences_list.append(record_list)
                chunk_counter = chunk_counter - 1
            else:
                chunk_counter = chunk_size
                sequences_list.append(record_list)
                break
        if len(sequences_list) > 0:
            chunk_df = pd.DataFrame.from_records(sequences_list, columns=df_columns, index=['index'])
            if not alignment:
                chunk_df = chunk_df.astype({'length':'int32','tab':'int32'})
            if first_chunk:
                first_chunk = False
                pre_state_dict = {'sequence':max_seq_length,'min_sequence':min_seq_length,'max_rows':max_rows}
                yield pre_state_dict,chunk_df
            else:
                yield chunk_df
        else:
            next_chunk = False
    return