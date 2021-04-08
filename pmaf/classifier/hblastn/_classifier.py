import warnings
warnings.simplefilter('ignore', category=UserWarning)
from pmaf.classifier._metakit import ClassifierBackboneMetabase
from pmaf.database._metakit import DatabaseBackboneMetabase
import numpy as np
import pandas as pd
from os import path,mkdir
from tempfile import TemporaryDirectory
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast.Applications import NcbimakeblastdbCommandline
from pmaf.internal._shared import sort_ranks,get_rank_upto
from datetime import datetime
from pmaf.sequence._metakit import MultiSequenceMetabase

class HBLASTNClassifier(ClassifierBackboneMetabase):
    _CACHE_PREFIX = 'dhnb_'
    DATETIME_FORMAT = "%d%m%Y_%H%M%S"
    def __init__(self, database_instance, cache_dir_fp=None, **kwargs):
        if not isinstance(database_instance, DatabaseBackboneMetabase):
            raise TypeError('`database_instance` has invalid type.')
        tmp_cache_root_dir = None
        if cache_dir_fp is not None:
            if not path.isdir(cache_dir_fp):
                raise NotADirectoryError('`cache_dir_fp` is invalid.')
            else:
                tmp_cache_root_dir = path.abspath(cache_dir_fp)
                tmp_cache_dir = TemporaryDirectory(prefix=self._CACHE_PREFIX,dir=tmp_cache_root_dir)
        else:
            tmp_cache_dir = TemporaryDirectory(prefix=self._CACHE_PREFIX)
        self._cache_root_dir = tmp_cache_root_dir
        self._cache_dir_tmp = tmp_cache_dir
        self._database = database_instance

    def classify_by_rank(self, multiseq, rank, min_subs=10, max_subs=500):
        if not isinstance(multiseq,MultiSequenceMetabase):
            raise TypeError('`multiseq` is invalid.')
        if rank not in self._database.avail_ranks:
            raise ValueError('Invalid rank given.')
        else:
            target_rank = rank
        allowed_ranks_sorted = sort_ranks(self._database.avail_ranks)
        last_allowed_ranks_ix = allowed_ranks_sorted.index(allowed_ranks_sorted[-2])
        if not (allowed_ranks_sorted.index(target_rank) <= last_allowed_ranks_ix):
            raise ValueError('Terminal or Pre-Terminal rank is given.')

        target_filename = path.join(self._cache_dir_tmp.name,"{}_{}_ref.fa".format(rank,datetime.now().strftime(self.DATETIME_FORMAT)))
        next_rank = target_rank

        def get_tid_rids(target_tids):
            tmp_tid2rid_map = self._database.find_rid_by_tid(target_tids, subs=False)
            return tmp_tid2rid_map.map(lambda tids: np.random.choice(tids, max_subs, False) if len(tids) > max_subs else tids)

        target_tids = self._database.take_tids_by_rank(target_rank)
        target_tid2rid_map = get_tid_rids(target_tids)

        while (allowed_ranks_sorted.index(next_rank) <= last_allowed_ranks_ix) and ((target_tid2rid_map.map(len) < min_subs).any()):
            next_rank = allowed_ranks_sorted[allowed_ranks_sorted.index(next_rank) + 1]

            norep_tids = target_tid2rid_map.index[(target_tid2rid_map.map(len) < min_subs)]

            norep_tids_subs = self._database.find_sub_tids_by_tid(norep_tids, ter_rank=next_rank)
            norep_tids_subs_adj = norep_tids_subs.map(lambda tids: np.random.choice(tids, 1, False)[0] if len(tids) > 0 else None)
            norep_valid_tids = norep_tids_subs_adj[norep_tids_subs_adj.notna()].index
            norep_new_tids = norep_tids_subs_adj[norep_valid_tids].values

            norep_tid2rid_tmp_map = get_tid_rids(norep_new_tids)
            norep_tid2rid_map = target_tid2rid_map.loc[norep_tids].to_dict()
            for norep_tid in norep_valid_tids:
                norep_tid2rid_map[norep_tid] = norep_tid2rid_map[norep_tid].tolist() if not isinstance(norep_tid2rid_map[norep_tid], list) else norep_tid2rid_map[norep_tid]
                norep_tid2rid_map[norep_tid].extend(norep_tid2rid_tmp_map[norep_tids_subs_adj[norep_tid]])

            norep_tid2rid_map = pd.Series(norep_tid2rid_map)

            target_tid2rid_map.loc[norep_tids] = norep_tid2rid_map.loc[norep_tids]

        target_tid2rid_map_adj = target_tid2rid_map[target_tid2rid_map.map(len) >= min_subs]

        all_unique_rids = list({rid for rids in target_tid2rid_map_adj.values for rid in rids})
        rank_repseqs = self._database.get_sequence_by_rid(all_unique_rids, iterator=False, like='multiseq')
        rank_repseqs.write(target_filename)
        tmp_makeblastdb_cline = NcbimakeblastdbCommandline(dbtype="nucl", input_file=target_filename)
        tmp_makeblastdb_cline_out = tmp_makeblastdb_cline()

        query_seq_filename = path.join(self._cache_dir_tmp.name,"{}_{}_query.fa".format(rank,datetime.now().strftime(self.DATETIME_FORMAT)))
        query_result_filename = path.join(self._cache_dir_tmp.name,"{}_{}_out.csv".format(rank,datetime.now().strftime(self.DATETIME_FORMAT)))
        multiseq.write(query_seq_filename)

        tmp_blastn_cline = NcbiblastnCommandline(query=query_seq_filename, db=target_filename,
                                      out=query_result_filename, outfmt=6, evalue=0.001, word_size=7,
                                      max_target_seqs=1, num_threads=5)
        tmp_blastn_cline_out = tmp_blastn_cline()

        # blastn -db gg_phylum.fasta -num_threads 5 -outfmt 6 -max_target_seqs 1 -query datasets/rdp_sample_500.fa -out datasets/rdp_sample_500.out.tsv

        rank_repseq_result = pd.read_csv(query_result_filename, sep='\t', header=None)
        result_map = rank_repseq_result.iloc[:, 0:2]
        result_map = result_map[~result_map.iloc[:, 0].duplicated()]

        classified_taxonomy = pd.Series(index=result_map.iloc[:, 0].values, data=result_map.iloc[:, 1].values)

        verbose = dict(makeblastn_out=tmp_makeblastdb_cline,
                       blastn_out=tmp_blastn_cline,
                       query_result_df=rank_repseq_result,
                       target_rank=target_rank,
                       sorted_ref_ranks=allowed_ranks_sorted)

        return classified_taxonomy, verbose

    def classify(self, *args, **kwargs):
        pass

    @property
    def state(self):
        return self._database.state

    @property
    def database(self):
        return self._database
