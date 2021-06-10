import warnings
warnings.simplefilter('ignore', category=FutureWarning)
from pmaf.biome.essentials._metakit import EssentialFeatureMetabase
import pandas as pd
import numpy as np
from pmaf.internal.io._seq import SequenceIO
from pmaf.internal._extensions._cpython._pmafc_extension._helper import make_sequence_record_tuple
from pmaf.internal._shared import get_stats_for_sequence_record_df
from pmaf.biome.essentials._base import EssentialBackboneBase
from pmaf.sequence import MultiSequence,Nucleotide

class RepSequence(EssentialBackboneBase, EssentialFeatureMetabase):
    ''' '''
    def __init__(self,sequences,**kwargs):
        super().__init__(**kwargs)
        tmp_sequences = []
        if isinstance(sequences,str):
            seqio = SequenceIO(sequences,upper=True)
            for rid,desc,seq in seqio.pull_parser(id=True,description=True,sequence=True):
                tmp_sequences.append(make_sequence_record_tuple(rid, seq)+(desc,))
        elif isinstance(sequences,MultiSequence):
            for seq in sequences.sequences:
                tmp_sequences.append(make_sequence_record_tuple(seq.name, str(seq.text))+('',))
        elif isinstance(sequences,pd.DataFrame):
            tmp_sequences = [make_sequence_record_tuple(rid, seq) + ('',) for rid, seq in sequences.loc[:,'sequence'].iteritems()]
        elif isinstance(sequences, pd.Series):
            tmp_sequences = [make_sequence_record_tuple(rid, seq) + ('',) for rid, seq in sequences.iteritems()]
        else:
            raise TypeError('`sequences` has unsupported type.')
        tmp_seq_record_df = pd.DataFrame.from_records(tmp_sequences,columns=['rid', 'sequence','length', 'tab','description'], index=['rid'])
        self.__sequence_df = pd.concat([tmp_seq_record_df[['sequence','description']],get_stats_for_sequence_record_df(tmp_seq_record_df)],axis=1)

    def _remove_features_by_id(self, ids, **kwargs):
        '''

        Args:
          ids: 
          **kwargs: 

        Returns:

        '''
        tmp_ids = np.asarray(ids,dtype=self.__sequence_df.index.dtype)
        if len(tmp_ids)>0:
            self.__sequence_df.drop(tmp_ids, inplace=True)
        return self._ratify_action('_remove_features_by_id', ids, **kwargs)

    def _merge_features_by_map(self, map_dict, **kwargs):
        '''

        Args:
          map_dict: 
          **kwargs: 

        Returns:

        '''
        print('ASSUME ALIGNED SEQUENCES!')
        return self._ratify_action('_merge_features_by_map', map_dict, **kwargs)

    def copy(self):
        ''' '''
        return type(self)(sequences=self.__sequence_df.loc[:,'sequence'], metadata = self.metadata,name=self.name)

    def get_subset(self, rids=None, *args, **kwargs):
        '''

        Args:
          rids: (Default value = None)
          *args: 
          **kwargs: 

        Returns:

        '''
        if rids is None:
            target_rids = self.xrid
        else:
            target_rids = np.asarray(rids).astype(self.__sequence_df.index.dtype)
        if not self.xrid.isin(target_rids).sum() == len(target_rids):
            raise ValueError('Invalid feature ids are provided.')
        return type(self)(sequences=self.__sequence_df.loc[target_rids,'sequence'], metadata = self.metadata,name=self.name)

    def to_multiseq(self):
        ''' '''
        tmp_sequences = []
        for ix, seq, desc in self.__sequence_df[:,['sequence','describtion']].itertuples():
            tmp_sequences.append(Nucleotide(seq,name=None, metadata={'description': desc}))
        return MultiSequence(tmp_sequences,name=self.name,metadata=self.metadata,internal_id='taxid')

    def _export(self, *args, **kwargs):
        '''

        Args:
          *args: 
          **kwargs: 

        Returns:

        '''
        return self.to_multiseq(), kwargs

    def export(self, output_fp, *args, _add_ext=False, **kwargs):
        '''

        Args:
          output_fp: 
          *args: 
          _add_ext: (Default value = False)
          **kwargs: 

        Returns:

        '''
        tmp_export, rkwarg = self._export(*args, **kwargs)
        if _add_ext:
            tmp_export.write("{}.fasta".format(output_fp), **rkwarg)
        else:
            tmp_export.write(output_fp, **rkwarg)

    @property
    def data(self):
        ''' '''
        return self.__sequence_df

    @property
    def xrid(self):
        ''' '''
        return self.__sequence_df.index