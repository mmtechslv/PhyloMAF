from collections import Counter, defaultdict
from pmaf.database._shared._common import filter_interx_elements, get_element_index_type, get_element_type
import pandas as pd
import numpy as np
from pmaf.internal._constants import MAIN_RANKS,VALID_RANKS
from pmaf.internal._shared import get_stats_for_sequence_record_df
from tempfile import NamedTemporaryFile
from pmaf.database._shared._summarizers import merge_recaps


def finalize_storage_construction(storage_manager, stamp_data, prior_recap, **kwargs):
    def produce_metadata_db_summary(final_recap):
        yield None, None
        yield final_recap.sort_index()

    final_recap = merge_recaps(prior_recap, make_column_details(storage_manager))
    storage_manager.commit_to_storage('metadata-db-summary', produce_metadata_db_summary(final_recap))
    storage_manager.imprint_database(stamp_data)

    compress = False
    overwrite = True
    complevel = 9
    complib = 'blosc'
    if len(kwargs):
        for key, value in kwargs.items():
            if key == 'compress' and isinstance(value, bool):
                compress = value
            elif key == 'overwrite' and isinstance(value, bool):
                overwrite = value
            elif key == 'complevel' and isinstance(value, int):
                complevel = value
            elif key == 'complib' and isinstance(value, str):
                complib = value
            else:
                raise KeyError('Invalid parameters were provided.')
    if compress:
        print('Compressing storage file.')
        if not storage_manager.compress_storage(complevel=complevel, complib=complib, overwrite=overwrite):
            raise RuntimeError('Could not compress storage file.')
    print('Storage is Ready.')
    return

def make_interxmaps(storage_manager):
    if storage_manager.state == -1:
        active_elements = filter_interx_elements(storage_manager.active_elements)
        if len(active_elements) > 0:
            repseq_elements = [element for element in active_elements if get_element_index_type(element) == 'map-interx-repseq']
            taxon_elements = [element for element in active_elements if get_element_index_type(element) == 'map-interx-taxon']
            def make_interxmap(target_elements,storage_manager):
                first_element = target_elements[0]
                internal_index_map = storage_manager.get_index_by_element(first_element)
                internal_index_map = internal_index_map.reset_index(name='target').set_index('target').rename({'index': first_element}, axis=1)
                if len(target_elements) > 1:
                    for element in target_elements[1:]:
                        next_elemenet_index_map = storage_manager.get_index_by_element(element)
                        next_elemenet_index_map = next_elemenet_index_map.reset_index(name='target').set_index('target').rename({'index': element}, axis=1)
                        internal_index_map = internal_index_map.join(next_elemenet_index_map, how='left')
                internal_index_map.sort_index(inplace=True)
                internal_index_map.index.rename('index', inplace=True)
                return internal_index_map
            return {'map-interx-repseq':make_interxmap(repseq_elements,storage_manager),'map-interx-taxon':make_interxmap(taxon_elements,storage_manager)}
        else:
            raise ValueError('Storage manager have not active elements.')
    else:
        raise RuntimeError('Storage Manager must be in construction state.')

def reparse_tree(tree_object, index_mapper):
    nodes_with_names = [node for node in tree_object.iter_leaves() if node.name != '']
    for node in nodes_with_names:
        if node.name in index_mapper.index:
            node.name = str(index_mapper[node.name])
        else:
            node.name = "-{}".format(str(node.name))
    with NamedTemporaryFile(mode='w+') as tmp_newick_io:
        tree_object.write(format=2, outfile=tmp_newick_io.name, format_root_node=True,quoted_node_names=True)
        tmp_newick_io.file.seek(0)
        return tmp_newick_io.file.read()

def rebuild_phylo(tree_object):
    nodes_with_no_names = tree_object.iter_search_nodes(name='')
    nn_counter = 1
    for node in nodes_with_no_names:
        node.name = '+{}'.format(str(nn_counter))
        nn_counter += 1
    all_names = [node.name for node in tree_object.iter_descendants()]

    duplicated_names = [name for name, count in Counter(all_names).items() if count > 1]
    duplicated_nodes = [tree_object.iter_search_nodes(name=node_name) for node_name in duplicated_names]
    for nodes in duplicated_nodes:
        counter = 1
        for node in nodes:
            new_name = '{}+{}'.format(str(counter), node.name)
            node.name = new_name
            counter = counter + 1
    return tree_object

def make_tree_map(tree_object):
    uid_map_list = []
    for node in tree_object.traverse('postorder'):
        if not node.is_root():
            uid_map_list.append([node.name, node.up.name])
        else:
            uid_map_list.append([node.name, ''])
    tree_map = pd.DataFrame.from_records(uid_map_list, columns=['uid', 'pid'], index=['uid'])
    tree_map.index = tree_map.index.map(str)
    return tree_map.applymap(str)

def reconstruct_taxonomy(master_taxonomy_sheet_df,index_mapper,reject_taxa=None):
    if reject_taxa is None:
        taxa_to_reject = []
    else:
        if isinstance(reject_taxa,str):
            taxa_to_reject = [reject_taxa]
        elif isinstance(reject_taxa,(tuple,list)):
            taxa_to_reject = list(reject_taxa)
        else:
            raise ValueError('`reject_taxa` is invalid.')

    tmp_master_tax_sheet_loose = master_taxonomy_sheet_df.dropna(axis=0, how='all')
    tmp_dropped_taxa = master_taxonomy_sheet_df.index[~master_taxonomy_sheet_df.index.isin(tmp_master_tax_sheet_loose.index)]
    removed_rids = index_mapper[index_mapper.isin(tmp_dropped_taxa)].index

    def correct_taxa(taxon):
        if taxon is not None:
            tmp_taxon_trimmed = taxon.lower().strip()
            if not any([taxon in tmp_taxon_trimmed for taxon in taxa_to_reject]):
                if tmp_taxon_trimmed[0] == '[':
                    tmp_taxon_trimmed = tmp_taxon_trimmed[1:]
                if tmp_taxon_trimmed[-1] == ']':
                    tmp_taxon_trimmed = tmp_taxon_trimmed[:-1]
                return tmp_taxon_trimmed.capitalize()
            else:
                return None
        else:
            return None

    tmp_master_tax_sheet = tmp_master_tax_sheet_loose.applymap(correct_taxa)

    avail_ranks = [rank for rank in VALID_RANKS if rank in tmp_master_tax_sheet.columns]

    groupby = tmp_master_tax_sheet.groupby(tmp_master_tax_sheet.columns.values.tolist())

    tmp_taxa_series_list = []
    group2prior = defaultdict(list)
    prior2group = defaultdict(int)
    group_i = 1
    for taxa_series, repseq_ids in groupby.groups.items():
        tmp_taxa_series_list.append(taxa_series)
        group2prior[group_i] = repseq_ids.values.tolist()
        for repseq_id in repseq_ids:
            prior2group[repseq_id] = group_i
        group_i = group_i + 1

    taxdf_dd = pd.DataFrame(data=tmp_taxa_series_list, index=range(1, group_i), columns=tmp_master_tax_sheet.columns)

    tmp_rep2gid = pd.DataFrame.from_dict(prior2group, orient='index', columns=['deduplication'])

    if avail_ranks[-1] == 's':
        avail_ranks = avail_ranks[:-1]
        groupby = taxdf_dd.groupby(avail_ranks)
        tmp_taxa_series_list = []
        group2prior_s = defaultdict(list)
        prior2group_s = defaultdict(int)
        group_i = 1
        for taxa_series, repseq_ids in groupby.groups.items():
            tmp_taxa_series_list.append(taxa_series)
            group2prior_s[group_i] = repseq_ids.values.tolist()
            for repseq_id in repseq_ids:
                prior2group_s[repseq_id] = group_i
            group_i = group_i + 1
        taxdf_dd_ds = pd.DataFrame(data=tmp_taxa_series_list, index=range(1, group_i), columns=avail_ranks)
        taxdf_dd_ds = taxdf_dd_ds.applymap(lambda x: None if pd.isna(x) else x)
        tmp_rep2gid['despecies'] = tmp_rep2gid['deduplication'].apply(prior2group_s.get)
        rep2tid_map = tmp_rep2gid['despecies'].to_frame('tid')
    else:
        rep2tid_map = tmp_rep2gid['deduplication'].to_frame('tid')
        taxdf_dd_ds = taxdf_dd.applymap(lambda x: None if pd.isna(x) else x)

    novel_tids_dict = defaultdict(dict)

    for rank in avail_ranks:
        target_rank_i = avail_ranks.index(rank)
        group_ranks = avail_ranks[:target_rank_i + 1]
        none_ranks = avail_ranks[target_rank_i + 1:]
        rank_tids = taxdf_dd_ds[taxdf_dd_ds[none_ranks].isna().all(axis=1)].dropna(subset=[rank])[group_ranks]
        groupby = taxdf_dd_ds.groupby(group_ranks)
        for taxa, tids in groupby.groups.items():
            taxa_tuple = tuple([taxa]) if rank == avail_ranks[0] else taxa
            if pd.notna(taxa_tuple[-1]):
                taxa_dict = {avail_ranks[ki]: [taxa_tuple[ki]] for ki in range(target_rank_i + 1)}
                target_rank_id = rank_tids[rank_tids.isin(taxa_dict).all(axis=1)].index.values.tolist()
                if len(target_rank_id) == 0:
                    target_rank_id = [taxdf_dd_ds.index.max() + len(novel_tids_dict) + 1]
                    nove_taxa_dict = {r: taxon[0] for r, taxon in taxa_dict.items()}
                    nove_taxa_dict.update({r: None for r in none_ranks})
                    novel_tids_dict[target_rank_id[0]] = nove_taxa_dict
                elif len(target_rank_id) > 1:
                    raise RuntimeError('Impossible scenario. Taxa at given rank cannot have more than one repseq. Invalid unduplication step.')
                repseq_ix = rep2tid_map[rep2tid_map['tid'].isin(tids)].index
                rep2tid_map.loc[repseq_ix, rank] = target_rank_id[0]

    rep2tid_map = rep2tid_map.fillna(0).astype(int)

    tmp_novel_taxdf = pd.DataFrame.from_dict(novel_tids_dict, orient='index')
    tmp_taxonomy_sheet = pd.concat([taxdf_dd_ds, tmp_novel_taxdf])
    missing_ranks = [r for r in MAIN_RANKS if r not in avail_ranks]

    for rank in missing_ranks:
        tmp_taxonomy_sheet.loc[:, rank] = None
        rep2tid_map.loc[:, rank] = 0

    rep2tid_map = rep2tid_map.reindex(columns=MAIN_RANKS + ['tid'])
    final_taxonomy_sheet = tmp_taxonomy_sheet.reindex(columns=MAIN_RANKS)
    transformation_details = {'map-rep2tid': rep2tid_map, 'removed-rids': removed_rids, 'changes': tmp_rep2gid, 'novel-tids': list(novel_tids_dict.keys()), 'avail-ranks': avail_ranks}
    return final_taxonomy_sheet.applymap(lambda x: '' if pd.isna(x) else x), transformation_details

def make_rid_index_mapper(rids_index):
    return rids_index.to_series(index=range(1,rids_index.shape[0]+1),name='rids').reset_index().set_index('rids').iloc[:,0]

def reindex_frame(target_df, index_mapper):
    return target_df.rename(index=index_mapper)

def make_column_details(storage_manager):
    tmp_column_summary = pd.Series()
    for element_key in storage_manager.active_elements:
        tmp_df = None
        if get_element_type(element_key) == 'fixed':
            tmp_df = storage_manager.retrieve_data_by_element(element_key)
        elif get_element_type(element_key) == 'table':
            tmp_df = next(storage_manager.retrieve_data_by_element(element_key,chunksize=2))
        if isinstance(tmp_df,pd.DataFrame):
            tmp_column_summary["columns-{}".format(element_key)] = '|'.join(list(tmp_df.columns))
    return tmp_column_summary

def produce_rep_stats(storage_manager, chunksize):
    total_repseqs = storage_manager.get_index_by_element('sequence-representative').shape[0]
    repseq_generator = storage_manager.retrieve_data_by_element('sequence-representative', chunksize=chunksize)

    yield {'index_columns':['index'],'max_rows':total_repseqs}, get_stats_for_sequence_record_df(next(repseq_generator))
    for repseq_df in repseq_generator:
        yield get_stats_for_sequence_record_df(repseq_df)

def produce_tax_stats(storage_manager, novel_tids):
    map2tid = storage_manager.retrieve_data_by_element('map-rep2tid')
    tid_subseqs_stat = defaultdict(tuple)
    for rank in map2tid.columns[map2tid.columns != 'tid']:
        groupby = map2tid.groupby(rank)
        for tid, rids in groupby.groups.items():
            if tid != 0:
                is_novel = tid in novel_tids
                total_subseqs = len(rids)
                is_singleton = total_subseqs == 1
                tid_subseqs_stat[tid] = (is_novel,total_subseqs,is_singleton,rank)
    tax_stats = pd.DataFrame.from_dict(tid_subseqs_stat, orient='index', columns=['novel','subseqs','singleton','rank'])
    yield None, None
    yield tax_stats

# Following function is experimental and is not integrated. It is here just in case if I changed my mind but I doubt it.
def make_repseq_map_generator(transformation_details,chunksize=500):
    tid_index = transformation_details['map-rep2tid']['tid'].unique().tolist() + transformation_details['novel-tids']
    rid_index = transformation_details['map-rep2tid'].index.values.tolist()

    repseq_map_dict = {tid: np.asarray([0] * len(rid_index), dtype='int8') for tid in tid_index}

    for rank in transformation_details['avail-ranks']:
        groupby = transformation_details['map-rep2tid'].groupby(rank)
        for tid, rids in groupby.groups.items():
            tmp_rid_dict = dict.fromkeys(rid_index, 0)
            if tid != '':
                for rid in rids:
                    tmp_rid_dict[rid] = 0b100  # 0b100 corresponds to any related sequence
                repseq_map_dict[tid] = np.bitwise_or(repseq_map_dict[tid], np.asarray([tmp_rid_dict[rid] for rid in rid_index], dtype='int8'))

    groupby = transformation_details['map-rep2tid'].groupby('tid')
    for tid, rids in groupby.groups.items():
        tmp_rid_dict = dict.fromkeys(rid_index, 0)
        for rid in rids:
            tmp_rid_dict[rid] = 0b010
        repseq_map_dict[tid] = np.bitwise_or(repseq_map_dict[tid], np.asarray([tmp_rid_dict[rid] for rid in rid_index], dtype='int8'))

    repseq_map_array = np.array([repseq_map_dict[tid] for tid in tid_index])

    pre_state_dict = {'index': max(list(map(len,tid_index))), 'max_rows': len(tid_index)}

    yield pre_state_dict, pd.DataFrame.from_records(repseq_map_array[:chunksize],index=tid_index[:chunksize],columns=rid_index).astype(np.dtype('int8'))

    for chunk_i in range(chunksize, len(tid_index)):
        yield pd.DataFrame.from_records(repseq_map_array[chunk_i:chunk_i + chunksize],index=tid_index[chunk_i:chunk_i + chunksize],columns=rid_index).astype(np.dtype('int8'))




