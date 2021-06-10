import warnings
warnings.simplefilter('ignore', category=FutureWarning)
from pmaf.biome.essentials._metakit import EssentialFeatureMetabase
from pmaf.biome.essentials._base import EssentialBackboneBase
from pmaf.internal._constants import AVAIL_TAXONOMY_NOTATIONS,jRegexGG,jRegexQIIME,BIOM_TAXONOMY_NAMES,VALID_RANKS
from pmaf.internal._shared import generate_lineages_from_taxa, get_rank_upto, \
    indentify_taxon_notation, validate_ranks, extract_valid_ranks, cols2ranks
from collections import defaultdict
from os import path
import pandas as pd
import numpy as np
import biom
from typing import Union, Sequence

class RepTaxonomy(EssentialBackboneBase, EssentialFeatureMetabase):
    ''' '''
    def __init__(self, taxonomy: Union[pd.DataFrame, pd.Series, str],
                 taxonomy_columns:Union[str,int,Sequence[Union[int,str]]] = None, **kwargs):
        tmp_metadata = kwargs.pop('metadata',{})
        self.__avail_ranks = []
        self.__internal_taxonomy = None
        if isinstance(taxonomy,pd.DataFrame):
            if taxonomy.shape[0] > 0:
                if taxonomy.shape[1]>1:
                    if validate_ranks(list(taxonomy.columns.values),VALID_RANKS):
                        tmp_taxonomy = taxonomy
                    else:
                        raise ValueError('Provided `taxonomy` Datafame has invalid ranks.')
                else:
                    tmp_taxonomy = taxonomy.iloc[:,0]
            else:
                raise ValueError('Provided `taxonomy` Datafame is invalid.')
        elif isinstance(taxonomy,pd.Series):
            if taxonomy.shape[0]>0:
                tmp_taxonomy = taxonomy
            else:
                raise ValueError('Provided `taxonomy` Series is invalid.')
        elif isinstance(taxonomy,str):
            if path.isfile(taxonomy):
                file_extension = path.splitext(taxonomy)[-1].lower()
                if file_extension in ['.csv','.tsv']:
                    if taxonomy_columns is None:
                        tmp_taxonomy = pd.read_csv(taxonomy, sep = kwargs.pop('sep',','), header = kwargs.pop('header','infer'), index_col = kwargs.pop('index_col',None))
                    else:
                        if isinstance(taxonomy_columns,int):
                            tmp_taxonomy = pd.read_csv(taxonomy, sep = kwargs.pop('sep',','), header = kwargs.pop('header','infer'), index_col = kwargs.pop('index_col',None)).iloc[:, taxonomy_columns]
                        else:
                            tmp_taxonomy = pd.read_csv(taxonomy, sep = kwargs.pop('sep',','), header = kwargs.pop('header','infer'), index_col = kwargs.pop('index_col',None)).loc[:, taxonomy_columns]
                elif file_extension in ['.biom','.biome']:
                    tmp_taxonomy, new_metadata = self.__load_biom(taxonomy, **kwargs)
                    tmp_metadata.update({'biom': new_metadata})
                else:
                    raise NotImplementedError('File type is not supported.')
            else:
                raise FileNotFoundError('Provided `taxonomy` file path is invalid.')
        else:
            raise TypeError('Provided `taxonomy` has invalid type.')
        self.__init_internal_taxonomy(tmp_taxonomy,**kwargs)
        super().__init__(metadata=tmp_metadata,**kwargs)

    @classmethod
    def from_csv(cls,filepath,taxonomy_columns=None,**kwargs):
        '''

        Args:
          filepath: 
          taxonomy_columns: (Default value = None)
          **kwargs: 

        Returns:

        '''
        if taxonomy_columns is None:
            tmp_taxonomy = pd.read_csv(filepath, **kwargs)
        else:
            if isinstance(taxonomy_columns, int):
                tmp_taxonomy = pd.read_csv(filepath, **kwargs).iloc[:, taxonomy_columns]
            else:
                tmp_taxonomy = pd.read_csv(filepath, **kwargs).loc[:, taxonomy_columns]
        tmp_metadata = kwargs.pop('metadata', {})
        tmp_metadata.update({'filepath': path.abspath(filepath)})
        return cls(taxonomy=tmp_taxonomy, metadata=tmp_metadata, **kwargs)

    @classmethod
    def from_biom(cls,filepath,**kwargs):
        '''

        Args:
          filepath: 
          **kwargs: 

        Returns:

        '''
        taxonomy_frame, new_metadata = cls.__load_biom(filepath, **kwargs)
        tmp_metadata = kwargs.pop('metadata', {})
        tmp_metadata.update({'biom':new_metadata})
        return cls(taxonomy=taxonomy_frame, metadata=tmp_metadata, **kwargs)

    @classmethod
    def __load_biom(cls, filepath, **kwargs):
        biom_file = biom.load_table(filepath)
        if biom_file.metadata(axis='observation') is not None:
            obs_data = biom_file.metadata_to_dataframe('observation')
            col_names = obs_data.columns.values.tolist()
            col_names_low = [col.lower() for col in col_names]
            avail_col_names = [colname for tax_name in BIOM_TAXONOMY_NAMES for colname in col_names_low if colname[::-1].find(tax_name[::-1]) < 3 and colname[::-1].find(tax_name[::-1]) > -1]
            metadata_cols = [col for col in col_names if col.lower() not in avail_col_names]
            if len(avail_col_names) == 1:
                tmp_col_index = col_names_low.index(avail_col_names[0])
                taxonomy_frame = obs_data[col_names[tmp_col_index]]
            else:
                taxonomy_frame = obs_data
            tmp_metadata = obs_data.loc[:,metadata_cols].to_dict()
            return taxonomy_frame, tmp_metadata
        else:
            raise ValueError('Biom file does not contain observation metadata.')

    def _remove_features_by_id(self, ids, **kwargs):
        '''

        Args:
          ids: 
          **kwargs: 

        Returns:

        '''
        tmp_ids = np.asarray(ids,dtype=self.__internal_taxonomy.index.dtype)
        if len(tmp_ids)>0:
            self.__internal_taxonomy.drop(tmp_ids, inplace=True)
        return self._ratify_action('_remove_features_by_id', ids, **kwargs)

    def _merge_features_by_map(self, map_dict, done=False, **kwargs):
        '''

        Args:
          map_dict: 
          done: (Default value = False)
          **kwargs: 

        Returns:

        '''
        if done:
            if len(map_dict)>0:
                return self._ratify_action('_merge_features_by_map', map_dict, _annotations=self.__internal_taxonomy.loc[:,'lineage'].to_dict(), **kwargs)
        else:
            raise NotImplementedError

    def drop_feature_by_id(self, ids: Union[Sequence[Union[str,int]]], **kwargs):
        '''Removeo features by feature indices.

        Args:
          ids: Feature indices
          **kwargs: 
          ids: Union[Sequence[Union[str: 
          int]]]: 

        Returns:

        '''
        target_ids = np.asarray(ids)
        if self.xrid.isin(target_ids).sum() == len(target_ids):
            return self._remove_features_by_id(target_ids, **kwargs)
        else:
            raise ValueError('Invalid feature ids are provided.')

    def get_taxonomy_by_id(self, ids=None):
        '''Get taxonomy DataFrame by feature indices.

        Args:
          ids: Either feature indices or None for all. (Default value = None)

        Returns:
          : pd.DataFrame with taxonomy data

        '''
        if ids is None:
            target_ids = self.xrid
        else:
            target_ids = np.asarray(ids)
        if self.xrid.isin(target_ids).sum() <= len(target_ids):
            return self.__internal_taxonomy.loc[target_ids,self.__avail_ranks]
        else:
            raise ValueError('Invalid feature ids are provided.')

    def get_lineage_by_id(self, ids=None, missing_rank=False, desired_ranks=False, drop_ranks=False, **kwargs):
        '''Get taxonomy lineages by feature indices.

        Args:
          ids: Either feature indices or None for all. (Default value = None)
          missing_rank: If True will generate prefix like s__ or d__  (Default value = False)
          desired_ranks: List of desired ranks to generate. If False then will generate all main ranks (Default value = False)
          drop_ranks: List of ranks to drop from desired ranks. This parameter only useful if `missing_rank` is True (Default value = False)
          **kwargs: 

        Returns:
          : Series with generated consensus lineages and corresponding IDs as Series index

        '''
        if ids is None:
            target_ids = self.xrid
        else:
            target_ids = np.asarray(ids)
        tmp_desired_ranks = VALID_RANKS if desired_ranks is False else desired_ranks
        total_valid_rids = self.xrid.isin(target_ids).sum()
        if total_valid_rids == len(target_ids):
            return generate_lineages_from_taxa(self.__internal_taxonomy.loc[target_ids],missing_rank, tmp_desired_ranks, drop_ranks)
        elif total_valid_rids < len(target_ids):
            return generate_lineages_from_taxa(self.__internal_taxonomy.loc[np.unique(target_ids)], missing_rank, tmp_desired_ranks, drop_ranks)
        else:
            raise ValueError('Invalid feature ids are provided.')

    def find_features_by_pattern(self, pattern_str, case_sensitive=False, regex=False):
        '''Searches for features with taxa that matches `pattern_str`

        Args:
          pattern_str: Pattern to search for
          case_sensitive: Case sensitive mode (Default value = False)
          regex: Use regular expressions (Default value = False)

        Returns:

        '''
        return self.__internal_taxonomy[self.__internal_taxonomy.loc[:, 'lineage'].str.contains(pattern_str, case=case_sensitive, regex=regex)].index.values

    def drop_features_without_taxa(self, **kwargs):
        '''Remove features that do not contain taxonomy.

        Args:
          **kwargs: 

        Returns:

        '''
        ids_to_drop = self.find_features_without_taxa()
        return self._remove_features_by_id(ids_to_drop, **kwargs)

    def drop_features_without_ranks(self, ranks, any=False, **kwargs):  # Done
        '''Remove features that do not contain `ranks`

        Args:
          ranks: Ranks to look for
          any: If True removes feature with single occurrence of missing rank. If False all `ranks` must be missing. (Default value = False)
          **kwargs: 

        Returns:

        '''
        target_ranks = np.asarray(ranks)
        if self.__internal_taxonomy.columns.isin(target_ranks).sum() == len(target_ranks):
            no_rank_mask = self.__internal_taxonomy.loc[:, ranks].isna()
            no_rank_mask_adjusted = no_rank_mask.any(axis=1) if any else no_rank_mask.all(axis=1)
            ids_to_drop = self.__internal_taxonomy.loc[no_rank_mask_adjusted].index
            return self._remove_features_by_id(ids_to_drop, **kwargs)
        else:
            raise ValueError('Invalid ranks are provided.')

    def merge_duplicated_features(self, **kwargs):
        '''Merge duplicated features

        Args:
          **kwargs: Passed to methods with similar task when in assembly.

        Returns:

        '''
        ret = {}
        groupby = self.__internal_taxonomy.groupby('lineage')
        if any([len(group) > 1 for group in groupby.groups.values()]):
            tmp_feature_lineage = []
            tmp_groups = []
            group_indices = list(range(len(groupby.groups)))
            for lineage, feature_ids in groupby.groups.items():
                tmp_feature_lineage.append(lineage)
                tmp_groups.append(list(feature_ids))
            self.__init_internal_taxonomy(pd.Series(data=tmp_feature_lineage, index=group_indices))
            ret = dict(zip(group_indices, tmp_groups))
        return self._merge_features_by_map(ret,True, **kwargs)

    def merge_features_by_rank(self, level: str, **kwargs):
        '''Merge features by taxonomic rank/level

        Args:
          level: Taxonomic rank based on which merging will be applied.
          **kwargs: Passed to methods with similar task when in assembly.
          level: str: 

        Returns:

        '''
        ret = {}
        if not isinstance(level,str):
            raise TypeError('`rank` must have str type.')
        if level in self.__avail_ranks:
            target_ranks = get_rank_upto(self.avail_ranks, level, True)
            if target_ranks:
                tmp_lineages = generate_lineages_from_taxa(self.__internal_taxonomy,False, target_ranks, False)
                groups = tmp_lineages.groupby(tmp_lineages)
                if len(groups.groups) > 1:
                    tmp_feature_lineage = []
                    tmp_groups = []
                    group_indices = list(range(len(groups.groups)))
                    for lineage, feature_ids in groups.groups.items():
                        tmp_feature_lineage.append(lineage)
                        tmp_groups.append(list(feature_ids))
                    self.__init_internal_taxonomy(pd.Series(data=tmp_feature_lineage, index=group_indices))
                    ret = dict(zip(group_indices, tmp_groups))
        else:
            raise ValueError('Invalid rank are provided.')
        return self._merge_features_by_map(ret,True, **kwargs)

    def find_features_without_taxa(self):
        '''Find features without taxa.'''
        return self.__internal_taxonomy.loc[self.__internal_taxonomy.loc[:, VALID_RANKS].
                                               agg(lambda rank: len(''.join(map(lambda x: (str(x or '')), rank))), axis=1) < 1].index.values

    def get_subset(self, rids:Union[Sequence,None] =None,
                   *args, **kwargs):
        '''Retrieves a subset of the RepTaxonomy

        Args:
          rids: (Default value = None) Feature indices to subset for.
          rids:Union[Sequence: 
          None]:  (Default value = None)
          *args: 
          **kwargs: 

        Returns:
          : New `RepTaxonomy`

        '''
        if rids is None:
            target_rids = self.xrid
        else:
            target_rids = np.asarray(rids).astype(self.__internal_taxonomy.index.dtype)
        if not self.xrid.isin(target_rids).sum() == len(target_rids):
            raise ValueError('Invalid feature ids are provided.')
        return type(self)(taxonomy=self.__internal_taxonomy.loc[target_rids, 'lineage'], metadata=self.metadata, name=self.name)

    def _export(self, taxlike: str ='lineage',
                ascending: bool = True, **kwargs):
        '''

        Args:
          taxlike: (Default value = 'lineage')
          ascending: (Default value = True)
          taxlike: str:  (Default value = 'lineage')
          ascending: bool:  (Default value = True)
          **kwargs: 

        Returns:

        '''
        if taxlike == 'lineage':
            return self.get_lineage_by_id(**kwargs).sort_values(ascending=ascending), kwargs
        else:
            raise NotImplemented

    def export(self, output_fp: str, *args,
               _add_ext:bool = False,
               sep:str = ',', **kwargs):
        '''

        Args:
          output_fp: 
          *args: 
          _add_ext: (Default value = False)
          sep: (Default value = ')
          ': 
          **kwargs: 
          output_fp: str: 
          _add_ext:bool:  (Default value = False)
          sep:str:  (Default value = ')

        Returns:

        '''
        tmp_export, rkwarg = self._export(*args, **kwargs)
        if _add_ext:
            tmp_export.to_csv("{}.csv".format(output_fp), sep=sep)
        else:
            tmp_export.to_csv(output_fp, sep=sep)

    def copy(self):
        '''Make a hard copy of current instance.'''
        return type(self)(taxonomy = self.__internal_taxonomy.loc[:,'lineage'], metadata = self.metadata,name=self.name)

    def __fix_taxon_names(self):
        def taxon_fixer(taxon):
            '''

            Args:
              taxon: 

            Returns:

            '''
            if taxon is not None and pd.notna(taxon):
                tmp_taxon_trimmed = taxon.lower().strip()
                if len(tmp_taxon_trimmed)>0:
                    if tmp_taxon_trimmed[0] == '[':
                        tmp_taxon_trimmed = tmp_taxon_trimmed[1:]
                    if tmp_taxon_trimmed[-1] == ']':
                        tmp_taxon_trimmed = tmp_taxon_trimmed[:-1]
                    return tmp_taxon_trimmed.capitalize()
                else:
                    return None
            else:
                return None
        self.__internal_taxonomy.loc[:, VALID_RANKS] = self.__internal_taxonomy.loc[:, VALID_RANKS].applymap(taxon_fixer)

    def __reconstruct_internal_lineages(self):
        """Reconstruct the internal lineages, `self.__internal_taxonomy.loc[:, 'lineage']`.

        """
        self.__internal_taxonomy.loc[:, 'lineage'] = generate_lineages_from_taxa(self.__internal_taxonomy,True, self.__avail_ranks, False)

    def __init_internal_taxonomy(self, taxonomy_data, taxonomy_notation='greengenes', order_ranks=None, **kwargs):
        """

        :param taxonomy_data: Incoming parsed taxonomy data
        :type taxonomy_data: pd.DataFrame or pd.Series
        :param taxonomy_notation: Taxonomy lineage notation style. Can be one of AVAIL_TAXONOMY_NOTATIONS
        :type taxonomy_notation: str
        :param order_ranks: List with the target rank order. Default is set to None. The 'silva' notation require `order_ranks`.
        :type order_ranks: list or None
        :param kwargs: None
        :type kwargs: None
        """
        if isinstance(taxonomy_data, pd.Series):
            new_taxonomy = self.__init_taxonomy_from_lineages(taxonomy_data, taxonomy_notation, order_ranks)
        elif isinstance(taxonomy_data, pd.DataFrame):
            if taxonomy_data.shape[1] == 1:
                taxonomy_data_series = pd.Series(data=taxonomy_data.iloc[:, 0], index=taxonomy_data.index)
                new_taxonomy = self.__init_taxonomy_from_lineages(taxonomy_data_series, taxonomy_notation, order_ranks)
            else:
                new_taxonomy = self.__init_taxonomy_from_frame(taxonomy_data, taxonomy_notation, order_ranks)
        else:
            raise RuntimeError('`taxonomy_data` must be either pd.Series or pd.Dataframe')
        if new_taxonomy is not None:
            self.__internal_taxonomy = new_taxonomy  # Assign newly constructed taxonomy to the self.__internal_taxonomy
            self.__fix_taxon_names()  # Fix incorrect taxa
            tmp_avail_ranks = [rank for rank in VALID_RANKS if rank in new_taxonomy.columns]
            self.__avail_ranks = [rank for rank in tmp_avail_ranks  if new_taxonomy.loc[:, rank].notna().any()]
            self.__reconstruct_internal_lineages()  # Reconstruct internal lineages for default greengenes notation
            self._init_state = True
        else:
            raise ValueError('Provided taxonomy is invalid.')

    def __init_taxonomy_from_lineages(self, taxonomy_series, taxonomy_notation, order_ranks):  # Done
        """Main method that produces taxonomy dataframe from lineages

        :param taxonomy_series: Map for rid - taxonomy lineage str
        :type taxonomy_series: pd.Series
        :param taxonomy_notation: Taxonomy lineage notation style. Can be one of AVAIL_TAXONOMY_NOTATIONS
        :type taxonomy_notation: str
        :param order_ranks: List with the target rank order. Default is set to None. The 'silva' notation require `order_ranks`.
        :type order_ranks: list or None
        :return: Dataframe with taxonomy
        :rtype: pd.DataFrame
        """
        if taxonomy_notation in AVAIL_TAXONOMY_NOTATIONS:  # Check if taxonomy is known and is available for parsing. Otherwise indentify_taxon_notation() will try to identify notation
            notation = taxonomy_notation
        else:
            sample_taxon = taxonomy_series.iloc[0]  # Get first lineage _sample for notation testing assuming the rest have the the same notations
            notation = indentify_taxon_notation(sample_taxon)  # Identify notation of the lineage string
        if order_ranks is not None:
            if not all([rank in VALID_RANKS for rank in order_ranks]):
                raise NotImplementedError
            else:
                target_order_ranks = order_ranks
        else:
            target_order_ranks = VALID_RANKS
        if notation == 'greengenes':
            lineages = taxonomy_series.reset_index().values.tolist()
            ordered_taxa_list = []
            ordered_indices_list = [elem[0] for elem in lineages]
            for lineage in lineages:
                tmp_lineage = jRegexGG.findall(lineage[1])
                tmp_taxa_dict = {elem[0]: elem[1] for elem in tmp_lineage if elem[0] in VALID_RANKS}
                for rank in VALID_RANKS:
                    if rank not in tmp_taxa_dict.keys():
                        tmp_taxa_dict.update({rank: None})
                tmp_taxa_ordered = [tmp_taxa_dict[rank] for rank in VALID_RANKS]
                ordered_taxa_list.append([None] + tmp_taxa_ordered)
            taxonomy = pd.DataFrame(index=ordered_indices_list, data=ordered_taxa_list, columns=['lineage'] + VALID_RANKS)
            return taxonomy
        elif notation=='qiime':
            lineages = taxonomy_series.reset_index().values.tolist()
            tmp_taxa_dict_list = []
            tmp_ranks = set()
            for lineage in lineages:
                tmp_lineage = jRegexQIIME.findall(lineage[1])
                tmp_lineage.sort(key=lambda x: x[0])
                tmp_taxa_dict = defaultdict(None)
                tmp_taxa_dict[None] = lineage[0]
                for rank, taxon in tmp_lineage:
                    tmp_taxa_dict[rank] = taxon
                    tmp_ranks.add(rank)
                tmp_taxa_dict_list.append(dict(tmp_taxa_dict))
            tmp_taxonomy_df = pd.DataFrame.from_records(tmp_taxa_dict_list)
            tmp_taxonomy_df.set_index(None, inplace=True)
            tmp_taxonomy_df = tmp_taxonomy_df.loc[:, sorted(list(tmp_ranks))]
            tmp_taxonomy_df.columns = [rank for rank in target_order_ranks[::-1][:len(tmp_ranks)]][::-1]
            for rank in [rank for rank in VALID_RANKS if rank not in tmp_taxonomy_df.columns]:
                tmp_taxonomy_df.loc[:,rank] = None
            return tmp_taxonomy_df 
        elif notation=='silva':
            lineages = taxonomy_series.reset_index().values.tolist()
            tmp_taxa_dict_list = []
            tmp_ranks = set()
            for lineage in lineages:
                tmp_lineage = lineage[1].split(';')
                tmp_taxa_dict = defaultdict(None)
                tmp_taxa_dict[None] = lineage[0]            
                for rank_i, taxon in enumerate(tmp_lineage):
                    rank = target_order_ranks[rank_i]
                    tmp_taxa_dict[rank] = taxon
                    tmp_ranks.add(rank)
                tmp_taxa_dict_list.append(dict(tmp_taxa_dict))
            tmp_taxonomy_df = pd.DataFrame.from_records(tmp_taxa_dict_list)
            tmp_taxonomy_df.set_index(None, inplace=True)
            tmp_rank_ordered = [rank for rank in target_order_ranks if rank in VALID_RANKS]
            tmp_taxonomy_df = tmp_taxonomy_df.loc[:, tmp_rank_ordered]
            tmp_taxonomy_df.columns = [rank for rank in target_order_ranks[::-1][:len(tmp_ranks)]][::-1]
            for rank in [rank for rank in VALID_RANKS if rank not in tmp_taxonomy_df.columns]:
                tmp_taxonomy_df.loc[:,rank] = None
            return tmp_taxonomy_df 
            
        else:
            raise NotImplementedError

    def __init_taxonomy_from_frame(self, taxonomy_dataframe, taxonomy_notation, order_ranks):  # Done # For now only pass to _init_taxonomy_from_series
        """Main method that produces taxonomy dataframe from dataframe

        :param taxonomy_dataframe: Map for rid - taxa with columns as levels/ranks
        :type taxonomy_dataframe: pd.DataFrame
        :param taxonomy_notation: Taxonomy lineage notation style. Can be one of AVAIL_TAXONOMY_NOTATIONS
        :type taxonomy_notation: str
        :param order_ranks: List with the target rank order. Default is set to None. The 'silva' notation require `order_ranks`.
        :type order_ranks: list or None
        :return: Dataframe with taxonomy
        :rtype: pd.DataFrame
        """
        valid_ranks = extract_valid_ranks(taxonomy_dataframe.columns,VALID_RANKS)
        if valid_ranks is not None:
            if len(valid_ranks)>0:
                return pd.concat([taxonomy_dataframe,pd.DataFrame(data='',index=taxonomy_dataframe.index,columns=[rank for rank in VALID_RANKS if rank not in valid_ranks])],axis=1)
            else:
                taxonomy_series = taxonomy_dataframe.apply(lambda taxa: ';'.join(taxa.values.tolist()), axis=1)
                return self.__init_taxonomy_from_lineages(taxonomy_series, taxonomy_notation,order_ranks)
        else:
            valid_ranks = cols2ranks(taxonomy_dataframe.columns)
            taxonomy_dataframe.columns = valid_ranks
            taxonomy_series = taxonomy_dataframe.apply(lambda taxa: ';'.join(taxa.values.tolist()), axis=1)
            return self.__init_taxonomy_from_lineages(taxonomy_series, taxonomy_notation, order_ranks)


    @property
    def avail_ranks(self):
        '''List of available taxonomic ranks.'''
        return self.__avail_ranks

    @property
    def duplicated(self):
        '''List of duplicated feature indices.'''
        return self.__internal_taxonomy.index[self.__internal_taxonomy['lineage'].duplicated(keep=False)]

    @property
    def data(self):
        '''Actual data representation as pd.DataFrame'''
        return self.__internal_taxonomy

    @property
    def xrid(self):
        '''Feature indices as pd.Index'''
        return self.__internal_taxonomy.index

