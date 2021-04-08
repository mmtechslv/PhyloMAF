import pandas as pd
import numpy as np
from string import Formatter

DATABASE_HDF5_STRUCT = {    'root-tree':'/tre', # Path
                            'root-taxonomy':'/tax',  # Path
                            'root-sequence':'/seq', # Path
                            'root-metadata':'/meta', # Path
                            'root-map':'/map', # Path
                            'root-stats':'/stat', # Path,
                            'stat-reps':'/stat/reps',
                            'stat-taxs':'/stat/taxs',
                            'tree-prior':'/tre/master/value', # Newick string UTF-8 encoded bytes. /value is explicitly refered in order to ease acess with simple .read()
                            'tree-parsed':'/tre/parsed/value', # Newick string UTF-8 encoded bytes. /value is explicitly refered in order to ease acess with simple .read()
                            'tree-object':'/tre/pickled/value', # Pickled bytes
                            'taxonomy-prior':'/tax/master',
                            'taxonomy-sheet':'/tax/parsed',
                            'sequence-representative':'/seq/reps',
                            'sequence-aligned':'/seq/algn',
                            'sequence-accession':'/seq/accs',
                            'metadata-db-summary':'/meta/summary', # pandas Series that contain all of the statistics and summary of the local such as taxonomy summary, representative sequence summary.
                            'metadata-db-info':'/meta/info', # pandas Series that will contain all of the information about which structure elements are full and which are inactive
                            'metadata-db-stamp':'/meta/stamp', # pandas Series that contain all of the information about the local creation such as author, creation time, etc.
                            'metadata-db-history':'/meta/history', # pandas Series that contain all of the information about the local processing. Data must be sufficient to reconstruct local to the prior state.
                            'map-interx-taxon':'/map/interxtax',
                            'map-interx-repseq':'/map/interxreps',
                            'map-rep2tid':'/map/reptid', # DataFrame of size len(# Valid RepSeqs) x (7 ranks + 1 TaxonID)
                            'map-repseq':'/map/repseq',  # DataFrame of size len(# TaxonIDs) x (1 Selected RepSeqID + 1 All Related RepSeqIDs separated by `|`
                            'map-tree':'/map/tree'
}

def get_element_mode(element_key):
    if element_key in ['tree-prior', 'tree-parsed', 'tree-object']:
        return 1
    else:
        return 2

def get_element_type(element_key):
    if get_element_mode(element_key) == 2:
        if element_key in ['map-interx-taxon','map-interx-repseq','map-tree']:
            return 'fixed'
        else:
            return 'table'
    else:
        return False

def get_element_index_type(element_key):
    if element_key in ['taxonomy-prior','sequence-representative','sequence-aligned','sequence-accession','map-rep2tid', 'stat-reps']:
        return 'map-interx-repseq'
    elif element_key in ['taxonomy-sheet','map-repseq','stat-taxs']:
        return 'map-interx-taxon'
    else:
        return None

def filter_interx_elements(element_key_list):
    tmp_element_list = []
    for element in element_key_list:
        if element in ['taxonomy-prior','sequence-representative','sequence-aligned','sequence-accession','map-rep2tid','taxonomy-sheet','stat-reps','stat-reps']:
            tmp_element_list.append(element)
    return tmp_element_list


def filter_elements_by(startswith, exclude=[]):
    tmp_element_list = []
    for key in DATABASE_HDF5_STRUCT.keys():
        if key.startswith(startswith) and key not in exclude:
            tmp_element_list.append(key)
    return tmp_element_list

def missing_to_none(target_pd_data):
    if isinstance(target_pd_data,pd.DataFrame):
        return target_pd_data.applymap(lambda x: None if (x == '' or pd.isna(x)) else x)
    else:
        return target_pd_data.map(lambda x: None if (x == '' or pd.isna(x)) else x)

def explode_element_columns(db_summary,element_key):
    tmp_element_col_label = "columns-{}".format(element_key)
    if tmp_element_col_label in db_summary.index:
        return db_summary.loc[tmp_element_col_label].split('|')
    else:
        return []

def to_mode(result_obj,mode='array',order=None):
    if mode == 'array':
        if isinstance(result_obj, (pd.DataFrame, pd.Series)):
            if order is None:
                if isinstance(result_obj, pd.DataFrame):
                    if result_obj.shape[1]>1:
                        return result_obj.apply(tuple,axis=1).values
                    else:
                        return result_obj.values
                else:
                    return result_obj.values
            else:
                if result_obj.index.isin(order).all():
                    if isinstance(result_obj, pd.DataFrame):
                        if result_obj.shape[1]>1:
                            if result_obj.index.has_duplicates:
                                result_obj_unq = result_obj[result_obj.index.duplicated()]
                                return result_obj_unq.loc[order].apply(tuple,axis=1).values
                            else:
                                return result_obj.reindex(index=order,fill_value=tuple([])).apply(tuple,axis=1).values
                        else:
                            if result_obj.index.has_duplicates:
                                result_obj_unq = result_obj[result_obj.index.duplicated()]
                                return result_obj_unq.loc[order].values
                            else:
                                return result_obj.reindex(index=order,fill_value=pd.NA).values
                        
                    else:
                        if result_obj.index.has_duplicates:
                            result_obj_unq = result_obj[result_obj.index.duplicated()]
                            return result_obj_unq.loc[order].values
                        else:
                            return result_obj.reindex(index=order,fill_value=pd.NA).values
                else:
                    raise ValueError('`order` index does not match `result_obj`.')
        elif isinstance(result_obj, (list, tuple)):
            return np.asarray(result_obj)
        elif isinstance(result_obj, dict):
            if order is None:
                if len(list(result_obj.values())[0])>1:
                    return np.asarray(list(map(tuple,result_obj.values())))
                else:
                    return np.asarray(list(result_obj.values()))
            else:
                tmp_result_list = []
                if len(list(result_obj.values())[0])>1:
                    for oid in order:
                        tmp_result_list.append(tuple(result_obj[oid]))
                else:
                    for oid in order:
                        tmp_result_list.append(result_obj[oid]) 
                return np.asarray(tmp_result_list)
        else:
            if isinstance(result_obj,np.ndarray) or np.isscalar(result_obj):
                return result_obj
            else:
                raise TypeError('Invalid data type was passed.')
    elif mode == 'frame':
        if isinstance(result_obj, (pd.DataFrame, pd.Series)):
            if order is None:
                return result_obj
            else:
                if result_obj.index.isin(order).all():
                    if result_obj.index.has_duplicates:
                        result_obj_unq = result_obj[result_obj.index.duplicated()]
                        return result_obj_unq.loc[order]
                    else:
                        return result_obj.reindex(index=order,fill_value=np.asarray([]))
                else:
                    raise ValueError('`order` index does not match `result_obj`.')
        elif isinstance(result_obj, (list, tuple)):
            return pd.Series(result_obj)
        elif isinstance(result_obj, dict):
            if len(result_obj)>0:
                result_obj_unq = pd.Series(result_obj)
                if order is None:
                    return result_obj_unq
                else:
                    if result_obj_unq.index.isin(order).all():
                        return result_obj_unq.reindex(index=order,fill_value=np.asarray([]))
                    else:
                        raise ValueError('`order` index does not match `result_obj`.')
            else:
                return pd.Series([],dtype=object)
        else:
            if isinstance(result_obj,np.ndarray):
                return pd.Series(result_obj)
            elif np.isscalar(result_obj):
                return result_obj
            else:
                raise TypeError('Invalid data type was passed.')
    elif mode == 'dict':
        if isinstance(result_obj, pd.DataFrame):
            return result_obj.to_dict(orient='index')
        elif isinstance(result_obj, pd.Series):
            return result_obj.to_dict()
        elif isinstance(result_obj, (list, tuple)):# Fallback
            return np.asarray(result_obj)
        elif isinstance(result_obj, dict):
            return dict(result_obj)
        else:
            if isinstance(result_obj,np.ndarray) or np.isscalar(result_obj): # Fallback
                return result_obj
            else:
                raise TypeError('Invalid data type was passed.')
    else:
        raise ValueError('Invalid `mode` is requested.')

def verify_tax_format(tax_format):
    valid_placeholders = ['tid', 'tax']
    target_placeholders = [fmt[1] for fmt in Formatter().parse(tax_format) if fmt[1] is not None]
    return all([ph in valid_placeholders for ph in target_placeholders])