from pmaf.database._metakit import  DatabaseTaxonomyMetabase
from pmaf.internal._shared import generate_lineages_from_taxa
from pmaf.database._shared._common import explode_element_columns, verify_tax_format
import numpy as np
import pandas as pd
from pmaf.internal._shared import sort_ranks

class DatabaseTaxonomyMixin(DatabaseTaxonomyMetabase):
    ''' '''
    def get_lineage_by_tid(self, ids = None, missing_rank=False, desired_ranks=False, drop_ranks=False):
        '''Generates lineages for taxon ids

        Args:
          ids: (Default value = None)
          missing_rank: (Default value = False)
          desired_ranks: (Default value = False)
          drop_ranks: (Default value = False)

        Returns:

        '''
        if ids is None:
            return generate_lineages_from_taxa(self.storage_manager.retrieve_data_by_element('taxonomy-sheet'), missing_rank, desired_ranks, drop_ranks)
        else:
            target_ids = np.asarray(ids)
            target_unique_ids = np.unique(target_ids)
            if self.xtid.isin(target_unique_ids).sum() == len(target_unique_ids):
                tmp_tax_sheet = self.storage_manager.get_element_data_by_ids('taxonomy-sheet', target_unique_ids)
                tmp_tax_lin = generate_lineages_from_taxa(tmp_tax_sheet, missing_rank, desired_ranks, drop_ranks)
                return tmp_tax_lin.loc[target_ids]
            else:
                raise ValueError('Invalid taxon ids provided.')

    def get_lineage_by_rid(self, ids = None, missing_rank=False, desired_ranks=False, drop_ranks=False):
        '''Generates lineages for taxon ids

        Args:
          ids: (Default value = None)
          missing_rank: (Default value = False)
          desired_ranks: (Default value = False)
          drop_ranks: (Default value = False)

        Returns:

        '''
        tmp_unver_map2tid = self.find_tid_by_rid(ids, levels='tid', method='asis', mode='frame')
        tmp_focus_map2tid = tmp_unver_map2tid[~tmp_unver_map2tid.index.duplicated()]
        tmp_rid_tax_sheet = pd.DataFrame(index=tmp_focus_map2tid.index, columns=explode_element_columns(self.storage_manager.summary, 'taxonomy-sheet'))
        tmp_tid_tax_sheet = self.storage_manager.retrieve_data_by_element('taxonomy-sheet')
        tmp_tid_groupby = tmp_focus_map2tid.groupby(tmp_focus_map2tid)
        for tid, rids in tmp_tid_groupby.groups.items():
            if tid == 0:
                tmp_rid_tax_sheet.loc[rids, :] = None
            else:
                tmp_rid_tax_sheet.loc[rids, :] = tmp_tid_tax_sheet.loc[tid, :].values
        tmp_rid_tax_lin = generate_lineages_from_taxa(tmp_rid_tax_sheet, missing_rank, desired_ranks, drop_ranks)
        return  tmp_rid_tax_lin.loc[tmp_unver_map2tid.index]

    def get_taxonomy_by_tid(self, ids = None, levels = None):
        '''Return taxonomy dataframe for given TaxonIDs or all if id=None

        Args:
          ids: List of TaxonIDs or None (Default value = None)
          levels: Default value

        Returns:
          

        '''
        if levels is None:
            target_ranks = np.asarray(self.avail_ranks)
        elif isinstance(levels, str):
            target_ranks = np.asarray([levels])
        else:
            target_ranks = np.asarray(levels)

        if np.isin(self.avail_ranks,target_ranks).sum() != len(target_ranks):
            raise ValueError('Invalid `levels` are provided.')

        if ids is None:
            product = self.storage_manager.retrieve_data_by_element('taxonomy-sheet')
        else:
            target_ids = np.asarray(ids)
            target_unique_ids = np.unique(target_ids)
            if self.xtid.isin(target_unique_ids).sum() == len(target_unique_ids):
                tmp_tax_sheet = self.storage_manager.get_element_data_by_ids('taxonomy-sheet', target_unique_ids)
                product = tmp_tax_sheet.loc[target_ids]
            else:
                raise ValueError('Invalid taxon ids provided.')
        if len(target_ranks)>1:
            return product.loc[:,target_ranks]
        else:
            return product.loc[:, target_ranks[0]]

    def get_taxonomy_by_rid(self, ids = None, levels = None, tax_format=None):
        '''Return taxonomy dataframe for given TaxonIDs or all if id=None

        Args:
          ids: List of TaxonIDs or None (Default value = None)
          levels: Default value
          tax_format: Default value

        Returns:
          

        '''
        if isinstance(tax_format, str):
            if not verify_tax_format(tax_format):
                raise ValueError('`tax_format` has invalid format.')
        elif tax_format is None:
            pass
        else:
            raise TypeError('`tax_format` has invalid type.')

        if levels is None:
            target_ranks = np.asarray(self.avail_ranks)
        elif isinstance(levels, str):
            target_ranks = np.asarray([levels])
        else:
            target_ranks = np.asarray(levels)

        if ids is None:
            target_ids = self.xrid.values
        else:
            target_ids = np.asarray(ids)

        target_unique_ids = np.unique(target_ids)
        target_unique_ranks = np.unique(target_ranks)
        unique_tids_flat = self.find_tid_by_rid(target_unique_ids, levels=target_unique_ranks, flatten=True, method='legal', mode='array')
        tmp_master_map2tid = self.find_tid_by_rid(target_unique_ids, levels=target_unique_ranks,flatten=False, method='asis', mode='frame')

        tmp_tid_tax_sheet = self.storage_manager.get_element_data_by_ids('taxonomy-sheet',unique_tids_flat).loc[:,target_unique_ranks]
        if tax_format is None:
            tmp_tax_map = tmp_tid_tax_sheet.reindex(columns=sort_ranks(tmp_tid_tax_sheet.columns))
        else:
            tmp_tax_map = tmp_tid_tax_sheet.reindex(columns=sort_ranks(tmp_tid_tax_sheet.columns))
            tmp_tid_tax_sheet = tmp_tid_tax_sheet.reset_index(drop=False).set_index('index',drop=False)
            for rank in sort_ranks(target_unique_ranks):
                tmp_tax_map.loc[:,rank] = tmp_tid_tax_sheet.loc[:,['index',rank]].\
                    apply(func=lambda row: None if row[rank] is None else tax_format.format(tid=str(row['index']), tax=str(row[rank])), axis=1)

        tmp_tax_map.loc[0,:] = None
        if len(target_ranks)>1:
            product = tmp_master_map2tid.replace(tmp_tax_map.to_dict(),value=None,method=None)
            return product.loc[target_ids,target_ranks]
        else:
            product = tmp_master_map2tid.replace(tmp_tax_map.iloc[:,0].to_dict(),value=None,method=None)
            return product.loc[target_ids]

    def get_taxonomy_by_rank(self, levels):
        '''

        Args:
          level: 
          ids: 
          levels: 

        Returns:

        '''
        if levels is None:
            target_ranks = np.asarray(self.avail_ranks)
        elif isinstance(levels, str):
            target_ranks = np.asarray([levels])
        else:
            target_ranks = np.asarray(levels)

        tids_for_ranks_flat = self.take_tids_by_rank(target_ranks,flatten=True)
        product = self.storage_manager.retrieve_data_by_element('taxonomy-sheet').loc[tids_for_ranks_flat,:]
        if isinstance(levels,str) and len(target_ranks)==1:
            return product.loc[:,target_ranks[0]]
        else:
            return product.loc[:, target_ranks]