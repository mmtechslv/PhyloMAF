import warnings
warnings.simplefilter('ignore', category=FutureWarning)
from pmaf.biome.essentials._metakit import EssentialFeatureMetabase,EssentialSampleMetabase
from pmaf.biome.essentials._base import EssentialBackboneBase
from collections import defaultdict
from os import path
import pandas as pd
import numpy as np
import biom

class FrequencyTable(EssentialBackboneBase, EssentialFeatureMetabase, EssentialSampleMetabase):
    '''The `Essential` class for handling frequency data.'''
    def __init__(self, frequency, skipcols=None, allow_nan=False, **kwargs):
        '''

        Args:
            frequency (Union[DataFrame, str]): Frequency data can be DataFrame or filepath
            skipcols (Union[str, int, list-like]): Columns to skip.
            allow_nan (bool): Allow NA/NaN values or raise an error.
            **kwargs (): Remaining parameters passed to `pandas.read_csv` or `__load_biom` method
        '''
        tmp_skipcols = np.asarray([])
        tmp_metadata = kwargs.pop('metadata',{})
        if skipcols is not None:
            if isinstance(skipcols,(str,int)):
                tmp_skipcols = np.asarray([skipcols])
            elif isinstance(skipcols,(list,tuple)):
                if isinstance(skipcols[0],(str,int)):
                    tmp_skipcols = np.asarray(skipcols)
                else:
                    raise TypeError('`skipcols` can be int/str or list-like of int/str.')
            else:
                raise TypeError('`skipcols` can be int/str or list-like of int/str.')
        if isinstance(frequency, pd.DataFrame):
            if all(frequency.shape):
                tmp_frequency = frequency
            else:
                raise ValueError('Provided `frequency` Datafame is invalid.')
        elif isinstance(frequency, str):
            if path.isfile(frequency):
                file_extension = path.splitext(frequency)[-1].lower()
                if file_extension in ['.csv', '.tsv']:
                    tmp_frequency = pd.read_csv(frequency,**kwargs)
                elif file_extension in ['.biom','.biome']:
                    tmp_frequency, new_metadata = self.__load_biom(frequency, **kwargs)
                    tmp_metadata.update({'biom': new_metadata})
                else:
                    raise NotImplementedError('File type is not supported.')
            else:
                raise FileNotFoundError('Provided `frequency` file path is invalid.')
        else:
            raise TypeError('Provided `frequency` has invalid type.')
        if skipcols is not None:
            if np.issubdtype(tmp_skipcols.dtype,np.number):
                if tmp_frequency.columns.isin(tmp_skipcols).any():
                    tmp_frequency.drop(columns=tmp_skipcols,inplace=True)
                else:
                    tmp_frequency.drop(columns=tmp_frequency.columns[tmp_skipcols], inplace=True)
            else:
                tmp_frequency.drop(columns=tmp_skipcols, inplace=True)
        tmp_dtypes = list(set(tmp_frequency.dtypes.values.tolist()))
        if len(tmp_dtypes) == 1 and pd.api.types.is_numeric_dtype(tmp_dtypes[0]):
            self.__init_frequency_table(tmp_frequency)
        else:
            if allow_nan:
                if len(tmp_dtypes)==1 and pd.api.types.is_numeric_dtype(tmp_dtypes[0]):
                    self.__init_frequency_table(tmp_frequency)
                elif len(tmp_dtypes)==2:
                    if all([(dt == object) or (pd.api.types.is_numeric_dtype(dt))  for dt in tmp_dtypes]) and tmp_frequency.isnull().values.any():
                        self.__init_frequency_table(tmp_frequency)
                    else:
                        raise ValueError('Provided `frequency` may contain numeric values or NAs.')
                else:
                    raise ValueError('Provided `frequency` has zero or too many dtypes.')
            else:
                raise ValueError('Provided `frequency` must have numeric dtypes. `allow_nan` to allow missing values.')
        super().__init__(metadata=tmp_metadata,**kwargs)

    @classmethod
    def from_biom(cls, filepath, **kwargs):
        '''Construct a FrequencyTable from BIOM file.

        Args:
          filepath(str): Path to .biom file.
          kwargs: type kwargs:
          **kwargs: 

        Returns:
          FrequencyTable: Instance of FrequencyTable

        '''
        frequency_frame, new_metadata = cls.__load_biom(filepath, **kwargs)
        tmp_metadata = kwargs.pop('metadata', {})
        tmp_metadata.update({'biom': new_metadata})
        return cls(frequency=frequency_frame, metadata=tmp_metadata, **kwargs)

    @classmethod
    def from_csv(cls, filepath, **kwargs):
        '''Construct a FrequencyTable from CSV file.

        Args:
          filepath(str): Path to .csv file.
          kwargs: type kwargs:
          **kwargs: 

        Returns:
          FrequencyTable: Instance of FrequencyTable

        '''
        tmp_frequency = pd.read_csv(filepath,**kwargs)
        tmp_metadata = kwargs.pop('metadata', {})
        tmp_metadata.update({'filepath': path.abspath(filepath)})
        return cls(frequency=tmp_frequency, metadata=tmp_metadata, **kwargs)

    @classmethod
    def __load_biom(cls, filepath, **kwargs):
        biom_file = biom.load_table(filepath)
        return biom_file.to_dataframe(dense=True), {}

    def _rename_samples_by_map(self, map_like, **kwargs):
        '''Rename sample names by map and ratify action.

        Args:
          map_like: 
          **kwargs: 

        Returns:

        '''
        self.__internal_frequency.rename(mapper=map_like, axis=1, inplace=True)
        return self._ratify_action('_rename_samples_by_map', map_like, **kwargs)

    def _remove_features_by_id(self, ids, **kwargs):
        '''Remove feature by id and ratify action.

        Args:
          ids: 
          **kwargs: 

        Returns:

        '''
        tmp_ids = np.asarray(ids,dtype=self.__internal_frequency.index.dtype)
        if len(tmp_ids)>0:
            self.__internal_frequency.drop(index=tmp_ids,inplace=True)
        return self._ratify_action('_remove_features_by_id', ids, **kwargs)

    def _merge_features_by_map(self, map_dict, aggfunc='sum', **kwargs):
        '''Merge features by map with aggfunc and ratify action.

        Args:
          map_dict: 
          aggfunc: (Default value = 'sum')
          **kwargs: 

        Returns:

        '''
        tmp_agg_dict = defaultdict(list)
        for new_id, group in map_dict.items():
            tmp_agg_dict[new_id] = self.__internal_frequency.loc[group, :].agg(func=aggfunc, axis=0).values
        tmp_freq_table = pd.DataFrame.from_dict(tmp_agg_dict, orient='index', columns=self.__internal_frequency.columns)
        self.__init_frequency_table(tmp_freq_table)
        return self._ratify_action('_merge_features_by_map', map_dict, aggfunc=aggfunc, **kwargs)

    def _remove_samples_by_id(self, ids, **kwargs):
        '''Remove samples by id and ratify action.

        Args:
          ids: 
          **kwargs: 

        Returns:

        '''
        tmp_ids = np.asarray(ids, dtype=self.__internal_frequency.columns.dtype)
        if len(tmp_ids) > 0:
            self.__internal_frequency.drop(columns=tmp_ids, inplace=True)
        return self._ratify_action('_remove_samples_by_id', ids, **kwargs)

    def _merge_samples_by_map(self, map_dict, aggfunc='mean', **kwargs):
        '''Merge samples by map with aggfunc and ratify action.

        Args:
          map_dict: 
          aggfunc: (Default value = 'mean')
          **kwargs: 

        Returns:

        '''
        tmp_agg_dict = defaultdict(list)
        for new_id, group in map_dict.items():
            tmp_agg_dict[new_id] = self.__internal_frequency.loc[:, group].agg(func=aggfunc, axis=1).to_dict()
        tmp_freq_table = pd.DataFrame.from_dict(tmp_agg_dict, orient='columns')
        self.__init_frequency_table(tmp_freq_table)
        return self._ratify_action('_merge_samples_by_map', map_dict, aggfunc=aggfunc, **kwargs)

    def transform_to_relative_abundance(self):
        '''Transform absolute counts to relative.'''
        self.__internal_frequency = self.__internal_frequency.div(self.__internal_frequency.sum(axis=0),axis=1)

    def replace_nan_with(self, value):
        '''Replace NaN values with `value`.

        Args:
          value(Any): Value to replace with.

        Returns:

        '''
        self.__internal_frequency.fillna(value,inplace=True)

    def drop_features_by_id(self, ids):
        '''Drop features by `ids`

        Args:
          ids(list-like): Feature identifiers

        Returns:
          rtype: 

        '''
        target_ids = np.asarray(ids)
        if self.__internal_frequency.index.isin(target_ids).sum() == len(target_ids):
            self._remove_features_by_id(target_ids)
            if self.is_buckled:
                return target_ids
        else:
            raise ValueError('Invalid _feature ids are provided.')

    def rename_samples(self, mapper):
        '''Rename sample names

        Args:
          mapper(Union[dict): dict or callable

        Returns:
          rtype: 

        '''
        if isinstance(mapper,dict) or callable(mapper):
            if isinstance(mapper, dict):
                if self.__internal_frequency.columns.isin(list(mapper.keys())).sum() == len(mapper):
                    self._rename_samples_by_map(mapper)
                else:
                    raise ValueError('Invalid sample ids are provided.')
            else:
                self._rename_samples_by_map(mapper)
        else:
            raise TypeError('Invalid `mapper` type.')

    def drop_features_without_counts(self):
        '''Drop features that has no counts. Typically required after dropping samples.'''
        target_ids = self.__internal_frequency.index[self.__internal_frequency.sum(axis=1) == 0].values
        self._remove_features_by_id(target_ids)
        if self.is_buckled:
            return target_ids

    def drop_samples_by_id(self, ids):
        '''Drop samples by `ids`.

        Args:
          ids(list-like): Sample identifiers

        Returns:
          rtype: 

        '''
        target_ids = np.asarray(ids)
        if self.__internal_frequency.columns.isin(target_ids).sum() == len(target_ids):
            self._remove_samples_by_id(target_ids)
            if self.is_buckled:
                return target_ids
        else:
            raise ValueError('Invalid _sample ids are provided.')

    def __init_frequency_table(self, freq_table):
        """Initiate the frequency table."""
        self.__internal_frequency = freq_table

    def merge_features_by_map(self, mapping, aggfunc='sum', **kwargs):
        '''Merge features by `mapping`.

        Args:
          mapping(dict-like): Map where values are feature identifiers to be aggregated.
          aggfunc(str, optional): Aggregation function. (Default value = 'sum')
          kwargs: type kwargs:
          **kwargs: 

        Returns:
          rtype: 

        '''
        if isinstance(mapping, (dict, pd.Series)):
            tmp_ids = sorted({x for _,v in mapping.items() for x in v}) # FIXME: Uncool behavior make it better and follow the usage.
            if self.__internal_frequency.index.isin(tmp_ids).sum() == len(tmp_ids):
                return self._merge_features_by_map(mapping, aggfunc, **kwargs)
            else:
                raise ValueError('Invalid feature ids were found.')
        else:
            raise TypeError('`mapping` can be `dict` or `pd.Series`')

    def merge_samples_by_map(self, mapping, aggfunc='mean', **kwargs):
        '''Merge samples by `mapping`

        Args:
          mapping(dict-like): Map where values are feature identifiers to be aggreagated.
          aggfunc(str, optional): Aggregation function. (Default value = 'mean')
          kwargs: type kwargs:
          **kwargs: 

        Returns:
          rtype: 

        '''
        if isinstance(mapping, (dict, pd.Series)):
            tmp_ids = sorted({x for _,v in mapping.items() for x in v}) # FIXME: Uncool. See above.
            if self.__internal_frequency.columns.isin(tmp_ids).sum() == len(tmp_ids):
                return self._merge_samples_by_map(mapping, aggfunc, **kwargs)
            else:
                raise ValueError('Invalid sample ids were found.')
        else:
            raise TypeError('`mapping` can be `dict` or `pd.Series`')

    def copy(self):
        '''Copy of the instance.'''
        return type(self)(frequency=self.__internal_frequency, metadata=self.metadata,name=self.name)

    def get_subset(self, rids=None, sids=None, *args, **kwargs):
        '''Get subset of the `FrequencyTable`.

        Args:
          rids(list-like, optional): Subset `rids` on feature axis. (Default value = None)
          sids(list-like, optional): Subset `sids` on sample axis. (Default value = None)
          args: type args:
          kwargs: type kwargs:
          *args: 
          **kwargs: 

        Returns:
          rtype: 

        '''
        if rids is None:
            target_rids = self.xrid
        else:
            target_rids = np.asarray(rids).astype(self.__internal_frequency.index.dtype)
        if sids is None:
            target_sids = self.xsid
        else:
            target_sids = np.asarray(sids).astype(self.__internal_frequency.columns.dtype)
        if not ((self.xrid.isin(target_rids).sum() == len(target_rids)) and (self.xsid.isin(target_sids).sum() == len(target_sids))):
            raise ValueError('Invalid ids are provided.')
        return type(self)(frequency=self.__internal_frequency.loc[target_rids,target_sids], metadata=self.metadata,name=self.name)

    def _export(self, sortby='counts',ascending=True, **kwargs):
        '''

        Args:
          sortby: (Default value = 'counts')
          ascending: (Default value = True)
          **kwargs: 

        Returns:

        '''
        if sortby == 'counts':
            return self.data.sort_values(by=self.xsid.values.tolist(), axis=0, ascending=ascending), kwargs
        else:
            raise NotImplemented

    def export(self, output_fp, *args, _add_ext=False, sep=',', **kwargs): # TODO: Improve
        '''Export the `FrequncyTable`.

        Args:
          output_fp(str): Export file path.
          args: type args:
          _add_ext: type _add_ext: (Default value = False)
          sep: type sep: (Default value = ')
          kwargs: type kwargs:
          *args: 
          ': 
          **kwargs: 

        Returns:

        '''
        tmp_export, rkwarg = self._export(*args, **kwargs)
        if _add_ext:
            tmp_export.to_csv("{}.csv".format(output_fp), sep=sep)
        else:
            tmp_export.to_csv(output_fp, sep=sep)

    @property
    def data(self):
        '''Pandas dataframe of `FrequencyTable`'''
        return self.__internal_frequency

    @property
    def xrid(self):
        '''Feature axis.'''
        return self.__internal_frequency.index

    @property
    def xsid(self):
        '''Sample axis.'''
        return self.__internal_frequency.columns

    @property
    def any_nan(self):
        '''Is there nan values present?'''
        return self.__internal_frequency.isnull().any().any()