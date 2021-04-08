from pmaf.biome.essentials import SampleMetadata,FrequencyTable,RepTaxonomy
import pandas as pd
import numpy as np
from functools import reduce
from pprint import pprint

def mergeRepTaxonmy(feature_groupby,features_map,essentials_map,aggfunc_dict):
    if feature_groupby == 'taxonomy':
        new_tax_lineages = features_map.loc[:, 'index'].reset_index().set_index('index')
        return RepTaxonomy(new_tax_lineages, name='Taxonomy')
    elif feature_groupby in ['index','label']:
        feature_groups = features_map.reset_index(drop=True).set_index('index')
        new_tax_lineages = pd.Series(index=feature_groups.index, data=None, dtype=str)
        shared_ranks = set([rank for essential in essentials_map[RepTaxonomy].values() for rank in essential.avail_ranks])
        for label, essential in essentials_map[RepTaxonomy].items():
            new_ids = feature_groups.index[feature_groups.loc[:, label].map(len).astype(bool)]
            target_ids = [rids[0] for rids in feature_groups.loc[new_ids, label].values]
            new_tax_lineages.loc[new_ids] = essential.get_lineage_by_id(ids=target_ids, desired_ranks=shared_ranks, missing_rank=True, drop_ranks=False).values
        return RepTaxonomy(new_tax_lineages, name='RepTaxonomy')
    else:
        raise ValueError('`feature_groupby` is invalid.')

def mergeFrequencyTable(feature_groupby,sample_groupby, features_map, samples_map, essentials_map,aggfunc_dict):
    if feature_groupby == 'taxonomy' and sample_groupby in ['index','label']:
        feature_groups = features_map.reset_index(drop=True).set_index('index')
        sample_groups = samples_map.reset_index(drop=True).set_index('index')

        freq_dfs = []
        label_dfs = []
        for label, essential in essentials_map[FrequencyTable].items():
            tmp_essential = essential.copy()
            tmp_feature_groups_map = feature_groups.loc[feature_groups.loc[:,label].map(len).astype(bool),label].to_dict()
            tmp_sample_groups_map = sample_groups.loc[sample_groups.loc[:,label].map(len).astype(bool),label].to_dict()
            tmp_essential._merge_features_by_map(tmp_feature_groups_map, aggfunc=aggfunc_dict[FrequencyTable][0])
            tmp_essential._merge_samples_by_map(tmp_sample_groups_map, aggfunc=aggfunc_dict[FrequencyTable][1])
            freq_dfs.append(tmp_essential.data)
            label_dfs.append(label)

        new_frequency_table =pd.concat(freq_dfs,axis=1,join='outer',keys=label_dfs).groupby(level=1,axis=1).agg(aggfunc_dict[FrequencyTable][1])
        return FrequencyTable(new_frequency_table, name='FrequencyTable')
    else:
        feature_groups = features_map.reset_index(drop=True).set_index('index')
        sample_groups = samples_map.reset_index(drop=True).set_index('index')
        new_freq_table_parts = {nsid: {nfid: list() for nfid in feature_groups.index} for nsid in sample_groups.index}
        for label, essential in essentials_map[FrequencyTable].items():
            tmp_freq_table = essential.data
            for new_sid, sids in sample_groups.loc[:, label].iteritems():
                if len(sids) > 0:
                    for new_rid, rids in feature_groups.loc[:, label].iteritems():
                        if len(rids) > 0:
                            new_freq_table_parts[new_sid][new_rid].append(tmp_freq_table.loc[rids, sids])

        new_freq_table_dict = {nsid: {nfid: list() for nfid in feature_groups.index} for nsid in sample_groups.index}
        for sid in sample_groups.index:
            for rid in feature_groups.index:
                if len(new_freq_table_parts[sid][rid]) > 0:
                    new_freq_table_dict[sid][rid] = pd.concat(new_freq_table_parts[sid][rid], join='outer', verify_integrity=False, ignore_index=True).agg(aggfunc_dict[FrequencyTable][0], axis=0).agg(aggfunc_dict[FrequencyTable][1])
                else:
                    new_freq_table_dict[sid][rid] = None
        new_frequency_table = pd.DataFrame.from_dict(new_freq_table_dict)
        return FrequencyTable(new_frequency_table, name='FrequencyTable')

def mergeSampleMetadata(sample_groupby,samples_map,essentials_map,aggfunc_dict):
    if sample_groupby in ['index','label']:
        sample_groups = samples_map.reset_index(drop=True).set_index('index')
        new_sample_parts = {nsid: list() for nsid in sample_groups.index}
        for label, essential in essentials_map[SampleMetadata].items():
            tmp_sample_table = essential.data
            for new_sid, sids in sample_groups.loc[:, label].iteritems():
                if len(sids) > 0:
                    new_sample_parts[new_sid].append(tmp_sample_table.loc[sids, :])
        new_sample_dict = {nsid: list() for nsid in sample_groups.index}
        for sid in sample_groups.index:
            if len(new_sample_parts[sid]) > 0:
                new_sample_dict[sid] = pd.concat(new_sample_parts[sid], join='outer', verify_integrity=False, ignore_index=True).agg(lambda meta:  '|'.join(set(meta)) if len(set(meta)) > 1 else meta[0]).to_dict()
            else:
                new_sample_dict[sid] = {}
        new_sample_table = pd.DataFrame.from_dict(new_sample_dict, orient='index')
        missing_index = sample_groups.index[~sample_groups.index.isin(new_sample_table.index)]
        if len(missing_index)>0:
            tmp_next_samle_table = pd.DataFrame(index=missing_index, columns=new_sample_table.columns).astype(new_sample_table.dtypes)
            new_sample_table = new_sample_table.append(tmp_next_samle_table)
        return SampleMetadata(new_sample_table, name='SampleMetadata', axis=0)
    else:
        raise ValueError('`sample_groupby` is invalid.')

def parse_assembly_maps(feature_groupby,sample_groupby,assembly_map):
    if feature_groupby in ['index','label']:
        features_set = set()
        for label, asmbly in assembly_map.items():
            assembly_map[label] = asmbly
            features_set.update(asmbly.xrid)
        features_map = pd.DataFrame(index=list(features_set), columns=list(assembly_map.keys()), dtype='object')
        for label, asmbly in assembly_map.items():
            features_map.loc[:, label] = features_map.index.where(features_map.index.isin(asmbly.xrid, None))
        features_map = features_map.applymap(lambda x: [] if pd.isna(x) else [x]).reset_index(col_level=0).rename(columns={'index': 'groups'}).reset_index().set_index('groups')
        if feature_groupby == 'label':
            if pd.api.types.is_object_dtype(features_map.index):
                features_map['index'] = features_map.index.astype(str)
            else:
                features_map['index'] = features_map.index
    elif feature_groupby == 'taxonomy':
        reptax_rank_list = []
        for label, asmbly in assembly_map.items():
            reptax_rank_list.append(asmbly.RepTaxonomy.avail_ranks)
            assembly_map[label] = asmbly
        shared_ranks = list(reduce(np.intersect1d, reptax_rank_list))
        features_map_dict = dict.fromkeys(assembly_map.keys())
        for label, asmbly in assembly_map.items():
            tmp_asm_tax = asmbly.RepTaxonomy.get_lineage_by_id(desired_ranks=shared_ranks, missing_rank=True, drop_ranks=False).map(lambda lin:lin.lower())
            features_map_dict[label] = {k: list(v) for k, v in tmp_asm_tax.groupby(tmp_asm_tax).groups.items()}
        features_map = pd.DataFrame.from_dict(features_map_dict, dtype=object)
        features_map = features_map.applymap(lambda x: x if isinstance(x, list) else []).reset_index(col_level=0).rename(columns={'index': 'groups'}).reset_index().set_index('groups')
    else:
        raise ValueError('`feature_groupby` is invalid.')

    if sample_groupby in ['index','label']:
        samples_set = set()
        for label, asmbly in assembly_map.items():
            assembly_map[label] = asmbly
            samples_set.update(asmbly.xsid)
        samples_map = pd.DataFrame(index=list(samples_set), columns=list(assembly_map.keys()), dtype='object')

        for label, asmbly in assembly_map.items():
            samples_map.loc[:, label] = samples_map.index.where(samples_map.index.isin(asmbly.xsid, None))
        samples_map = samples_map.applymap(lambda x: [] if pd.isna(x) else [x]).reset_index(col_level=0).rename(columns={'index': 'groups'}).reset_index().set_index('groups')
        if sample_groupby == 'label':
            if pd.api.types.is_object_dtype(features_map.index):
                samples_map['index'] = samples_map.index.astype(str)
            else:
                samples_map['index'] = samples_map.index
    else:
        raise ValueError('`sample_groupby` is invalid.')
    return features_map, samples_map