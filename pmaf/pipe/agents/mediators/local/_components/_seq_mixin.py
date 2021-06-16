from pmaf.pipe.agents.mediators._metakit import MediatorSequenceMetabase
from pmaf.pipe.agents.mediators.local._base import MediatorLocalBase
from pmaf.pipe.agents.dockers._metakit import DockerIdentifierMetabase
from pmaf.pipe.agents.dockers._mediums._seq_medium import DockerSequenceMedium
from pmaf.database._metakit import DatabaseSequenceMetabase
from pmaf.alignment._multiple._metakit import MultiSequenceAlignerBackboneMetabase
import numpy as np
from collections import defaultdict

class MediatorLocalSequenceMixin(MediatorLocalBase,MediatorSequenceMetabase):
    ''' '''
    SEQ_EXTRACT_METHODS = ['refseq', 'consensus']
    SEQ_FILTER_METHODS = ['random','tab']
    def __init__(self, database,
                 seq_method='refseq',
                 seq_subs=False,
                 seq_aligner=None,
                 seq_force_align=False,
                 seq_refrep='tid',
                 seq_filter_method=None,
                 seq_filter_value=None,
                 **kwargs):

        if isinstance(database, DatabaseSequenceMetabase):
            if not database.storage_manager.has_repseq:
                raise TypeError('`database` does not have valid sequences present.')
        else:
            raise TypeError('`database` must be instance of DatabasePhylogenyMetabase')
        if isinstance(seq_method, str):
            if seq_method not in self.SEQ_EXTRACT_METHODS:
                raise ValueError('`seq_method` is unknown.')
        else:
            raise TypeError('`seq_method` has invalid type.')
        if seq_aligner is not None:
            if not isinstance(seq_aligner, MultiSequenceAlignerBackboneMetabase):
                raise TypeError('`seq_aligner` has invalid type.')

        if seq_refrep not in ['tid','rid']:
            raise ValueError('`seq_refrep` is invalid.')

        if seq_method == 'consensus' and not (seq_aligner is not None or database.storage_manager.has_align):
            raise ValueError('`seq_method` in consensus mode require valid `seq_aligner` or database alignment.')
        if seq_filter_method is not None:
            if isinstance(seq_filter_method, str):
                if not seq_filter_method in self.SEQ_FILTER_METHODS:
                    raise ValueError('`seq_filter_method` is unknown.')
            elif callable(seq_filter_method):
                pass
            else:
                raise TypeError('`seq_filter_method` has invalid type.')
        if seq_filter_value is not None:
            if not isinstance(seq_filter_value, int):
                raise TypeError('`seq_filter_value` has invalid type.')


        super().__init__(database=database,
                         seq_method=seq_method,
                         seq_aligner=seq_aligner,
                         seq_subs=bool(seq_subs),
                         seq_force_align=bool(seq_force_align),
                         seq_refrep=seq_refrep,
                         seq_filter_method=seq_filter_method,
                         seq_filter_value=seq_filter_value,**kwargs)

    def get_sequence_by_identifier(self, docker, factor, **kwargs):
        '''

        Args:
          docker: 
          factor: 
          **kwargs: 

        Returns:

        '''
        if not self.verify_factor(factor):
            raise ValueError('`factor` is invalid.')
        if isinstance(docker, DockerIdentifierMetabase):
            if docker.singleton:
                return self.__retrieve_sequences_by_identifier(docker, **kwargs)
            else:
                raise ValueError('`docker` must be singleton.')
        else:
            raise TypeError('`docker` must be instance of DockerIdentifierMetabase.')

    def get_identifier_by_sequence(self, docker, factor, **kwargs):
        '''

        Args:
          docker: 
          factor: 
          **kwargs: 

        Returns:

        '''
        raise NotImplementedError

    def __retrieve_sequences_by_identifier(self, docker, **kwargs):

        id_array = docker.to_array(exclude_missing=True)
        new_metadata = {'configs':self.configs, 'master': docker.wrap_meta()}
        is_alignment, tmp_multiseq_request = self.__request_multiseq_by_method(id_array)
        if self.configs['seq_method'] == 'refseq':
            tmp_results = dict.fromkeys(tmp_multiseq_request.keys(), None)
            for mseq_id, multiseq in tmp_multiseq_request.items():
                if multiseq is not None:
                    tmp_results[mseq_id] = self.__parse_multiseq_for_refseq(multiseq)
        elif self.configs['seq_method'] == 'consensus' and isinstance(tmp_multiseq_request,dict):
            tmp_results = dict.fromkeys(tmp_multiseq_request.keys(), None)
            for mseq_id, multiseq in tmp_multiseq_request.items():
                if multiseq is not None:
                    tmp_results[mseq_id] = self.__parse_multiseq_for_consensus(multiseq, not is_alignment)
        else:
            raise RuntimeError('`seq_method` is unknown.')
        id_rev_map = {v: k for k, v in docker.get_subset(exclude_missing=True).data.items()}
        tmp_results_adj = {id_rev_map[k]:v for k,v in tmp_results.items()}
        tmp_results_adj.update({tid:None for tid in docker.missing})
        return DockerSequenceMedium(tmp_results_adj,name=docker.name,metadata=new_metadata,aligned=is_alignment)

    def __request_multiseq_by_method(self,id_array):
        if self.configs['seq_method'] == 'refseq':
            if self.configs['seq_force_align']:
                if isinstance(self.configs['seq_aligner'], MultiSequenceAlignerBackboneMetabase):
                    retrieve_alignment = False
                else:
                    raise RuntimeError('`seq_aligner` is required and an has invalid type.')
            else:
                retrieve_alignment = False
        elif self.configs['seq_method'] == 'consensus':
            if (not self.client.storage_manager.has_align) or self.configs['seq_force_align']:
                retrieve_alignment = False
            elif self.client.storage_manager.has_align:
                retrieve_alignment = True
            else:
                raise NotImplementedError
        else:
            raise RuntimeError('`seq_method` is invalid.')

        if self.configs['seq_refrep'] == 'tid' and retrieve_alignment:
            if self.configs['seq_filter_method'] == 'random' and isinstance(self.configs['seq_filter_value'], int):
                repseq_map_gen = self.client.find_rid_by_tid(id_array, subs=self.configs['seq_subs'], iterator=True)
                tmp_ret = defaultdict(None)
                for tid, rid_list in repseq_map_gen:
                    if len(rid_list) > self.configs['seq_filter_value']:
                        tmp_target_rids = np.random.choice(rid_list, self.configs['seq_filter_value'], False)
                        tmp_ret[tid] = self.client.get_alignment_by_rid(tmp_target_rids, like='multiseq', iterator=False)
                    else:
                        tmp_ret[tid] = self.client.get_alignment_by_rid(rid_list, like='multiseq', iterator=False)
                ret = dict(tmp_ret)
            elif self.configs['seq_filter_method'] is None:
                ret = self.client.get_alignment_by_tid(id_array, subs=self.configs['seq_subs'], like='multiseq', iterator=False)
            else:
                raise NotImplementedError
        elif self.configs['seq_refrep'] == 'tid' and not retrieve_alignment:
            if self.configs['seq_filter_method'] == 'random' and isinstance(self.configs['seq_filter_value'], int):
                repseq_map_gen = self.client.find_rid_by_tid(id_array, self.configs['seq_subs'], iterator=True)
                tmp_ret = defaultdict(None)
                for tid, rid_list in repseq_map_gen:
                    if len(rid_list) > self.configs['seq_filter_value']:
                        tmp_target_rids = np.random.choice(rid_list, self.configs['seq_filter_value'], False)
                        tmp_ret[tid] = self.client.get_sequence_by_tid(tmp_target_rids, like='multiseq', iterator=False)
                    else:
                        tmp_ret[tid] = self.client.get_sequence_by_tid(id_array, like='multiseq', iterator=False)
                ret = dict(tmp_ret)
            elif self.configs['seq_filter_method'] is None:
                ret = self.client.get_sequence_by_tid(id_array, subs=self.configs['seq_subs'], like='multiseq', iterator=False)
            else:
                raise NotImplementedError
        elif self.configs['seq_refrep'] == 'rid' and retrieve_alignment:
            ret = self.client.get_alignment_by_rid(id_array, like='multiseq', iterator=False)
        elif self.configs['seq_refrep'] == 'rid' and not retrieve_alignment:
            ret = self.client.get_sequence_by_tid(id_array, like='multiseq', iterator=False)
        else:
            raise RuntimeError('`seq_refrep` is invalid.')
        return retrieve_alignment, ret

    def __parse_multiseq_for_consensus(self, multiseq, align):
        if self.configs['seq_method'] == 'consensus' and align:
                seq_aligner = self.configs['seq_aligner']
                if isinstance(seq_aligner, MultiSequenceAlignerBackboneMetabase):
                    return seq_aligner.align(multiseq).get_consensus()
                else:
                    raise RuntimeError('`seq_aligner` has invalid type.')
        elif self.configs['seq_method'] == 'consensus' and not align:
            return multiseq.get_consensus()
        else:
            raise NotImplementedError

    def __parse_multiseq_for_refseq(self,multiseq):
        if self.configs['seq_filter_method'] == 'random' and isinstance(self.configs['seq_filter_value'],int):
            if multiseq.count > self.configs['seq_filter_value']:
                tmp_target_ids = np.random.choice(multiseq.index, self.configs['seq_filter_value'], False)
                return multiseq.get_subset(tmp_target_ids)
            else:
                return multiseq
        elif self.configs['seq_filter_method'] is None:
            return multiseq
        else:
            raise NotImplementedError
