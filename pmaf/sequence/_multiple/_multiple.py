import warnings
warnings.simplefilter('ignore', category=FutureWarning)
from skbio import TabularMSA
from skbio.sequence import GrammaredSequence
from io import StringIO,IOBase
from shutil import copyfileobj
import copy
import numpy as np
from pmaf.internal.io._seq import SequenceIO
from pmaf.sequence._sequence._nucleotide import Nucleotide
from pmaf.sequence._metakit import MultiSequenceMetabase,NucleotideMetabase
from pmaf.sequence._shared import validate_seq_mode

class MultiSequence(MultiSequenceMetabase):
    ''' '''
    def __init__(self,sequences,name=None,mode=None,metadata=None,aligned=False,**kwargs):
        if name is None or np.isscalar(name):
            tmp_name = name
        else:
            raise TypeError('`name` can be any scalar')
        if isinstance(metadata, dict):
            tmp_metadata = metadata
        elif metadata is None:
            tmp_metadata = {}
        else:
            raise TypeError('`metadata` can be dict or None')
        if mode is not None:
            if validate_seq_mode(mode):
                tmp_mode = mode.lower()
            else:
                raise ValueError('`mode` is invalid.')
        else:
            tmp_mode = mode
        tmp_sequences = []
        if isinstance(sequences,list):
            if all([isinstance(sequence, NucleotideMetabase) for sequence in sequences]):
                tmp_sequences = sequences
            elif all([isinstance(sequence,GrammaredSequence) for sequence in sequences]):
                tmp_sequences = [Nucleotide(skbio_seq, mode=None, **kwargs) for skbio_seq in sequences]
            else:
                raise ValueError('`sequences` must have same type when provided as list.')
        else:
            if tmp_mode is not None:
                seq_gen = SequenceIO(sequences,upper=True).pull_parser(parser='simple',id=True,description=True,sequence=True)
                for sid, desc, seq_str in seq_gen:
                    tmp_sequences.append(Nucleotide(seq_str, name=sid, mode=tmp_mode, metadata={'description': desc}, **kwargs))
            else:
                raise ValueError('`mode` cannot be None if raw read is performed.')
        if aligned:
            if len(set([sequence.length for sequence in tmp_sequences])) != 1:
                raise ValueError('`sequences` must be all of the length if aligned.')
        tmp_indices = [sequence.name for sequence in tmp_sequences]
        if len(tmp_indices) != len(set(tmp_indices)):
            raise ValueError('`sequences` must have unique names.')
        tmp_modes = set([sequence.mode for sequence in tmp_sequences])
        if len(tmp_modes)>1:
            raise ValueError('`sequences` cannot have different modes.')
        if tmp_mode is not None:
            if tmp_mode not in tmp_modes:
                raise ValueError('`mode` must match modes of sequences.')
        else:
            tmp_mode = tmp_modes.pop()
        tmp_internal_id = kwargs.get('internal_id',None)
        if tmp_internal_id is not None:
            for sequence in tmp_sequences:
                if tmp_internal_id not in sequence.metadata.keys():
                    raise ValueError('Metadata of all sequences must contain same internal_id.')
        self.__indices = np.asarray([seq.name for seq in tmp_sequences])
        self.__sequences = tmp_sequences
        self.__metadata = tmp_metadata
        self.__aligned = bool(aligned)
        self.__internal_id = tmp_internal_id
        self.__skbio_mode = tmp_sequences[0].skbio_mode
        self.__mode = tmp_mode
        self.__name = tmp_name
        self.__buckled = bool(kwargs.get('buckled',None))

    def __repr__(self):
        class_name = self.__class__.__name__
        name = self.__name if self.__name is not None else 'N/A'
        count = len(self.__sequences)
        metadata_state = 'Present' if len(self.__metadata)>0 else 'N/A'
        aligned = 'Yes' if self.__aligned else 'No'
        mode = self.__mode.upper() if self.__mode is not None else 'N/A'
        repr_str = "<{}:[{}], Name:[{}], Mode:[{}], Aligned: [{}], Metadata:[{}]>".format(class_name, count, name, mode, aligned, metadata_state)
        return repr_str

    def to_skbio_msa(self, indices=None):
        '''

        Args:
          indices: (Default value = None)

        Returns:

        '''
        if self.__aligned:
            tmp_sequences = self.__get_seqs_by_index(indices)
            return TabularMSA([sequence.skbio for sequence in tmp_sequences])
        else:
            raise RuntimeError('TabularMSA can only be retrieved for alignment.')

    def __get_seqs_by_index(self,ids):
        if ids is not None:
            target_ids = np.asarray(ids)
        else:
            target_ids = self.__indices
        if np.isin(self.__indices,target_ids).sum() == len(target_ids):
            return [seq for seq in self.__sequences if seq.name in target_ids]
        else:
            raise ValueError('Invalid indices are provided.')

    def get_consensus(self,indices=None):
        '''

        Args:
          indices: (Default value = None)

        Returns:

        '''
        if self.__aligned:
            tmp_msa = self.to_skbio_msa(indices)
            return Nucleotide(tmp_msa.consensus(),name=self.__name,metadata=self.__metadata,mode=self.__mode)
        else:
            raise RuntimeError('Consensus can be retrieved only from alignment.')

    def get_subset(self,indices=None):
        '''

        Args:
          indices: (Default value = None)

        Returns:

        '''
        return type(self)(self.__get_seqs_by_index(indices),name=self.__name,metadata=self.__metadata,mode=self.__mode, aligned=self.__aligned)

    def buckle_for_alignment(self):
        ''' '''
        if not self.__buckled:
            from collections import defaultdict
            from random import random

            if self.__internal_id is None:
                self.__internal_id = round(random() * 100000, None)
            packed_metadata = {'master-metadata': self.__metadata, '__name': self.__name, '__internal_id': self.__internal_id}
            children_metadata = defaultdict(dict)
            for tmp_uid, sequence in enumerate(self.__sequences):
                tmp_uid_str = 'TMP_ID_{}'.format(str(tmp_uid))
                children_metadata[tmp_uid_str] = sequence.buckle_by_uid(tmp_uid_str)
            packed_metadata.update({'children-metadata': dict(children_metadata)})
            self.__buckled = True
            return packed_metadata
        else:
            raise RuntimeError('MultiSequence instance is already buckled.')

    def restore_buckle(self,buckled_pack):
        '''

        Args:
          buckled_pack: 

        Returns:

        '''
        if self.__buckled:
            self.__metadata = buckled_pack['master-metadata']
            self.__name = buckled_pack['__name']
            self.__internal_id = buckled_pack['__internal_id']
            for sequence in self.__sequences:
                tmp_uid = sequence.unbuckle_uid()
                child_packed_metadata = buckled_pack['children-metadata'][tmp_uid]
                sequence.restore_buckle(child_packed_metadata)
            self.__indices = np.asarray([seq.name for seq in self.__sequences])
        else:
            raise RuntimeError('MultiSequence instance is not buckled.')

    def get_iter(self, method='asis'):
        '''

        Args:
          method: (Default value = 'asis')

        Returns:

        '''
        def make_generator():
            ''' '''
            for sequence in self.__sequences:
                if method == 'asis':
                    yield sequence.name, sequence
                elif method == 'string':
                    yield sequence.name, sequence.text
                elif method == 'skbio':
                    yield sequence.name, sequence.skbio
                else:
                    raise ValueError('`method` is invalid.')
        return make_generator()

    def copy(self):
        ''' '''
        return copy.deepcopy(self)

    def write(self, file, mode='w', **kwargs):
        '''

        Args:
          file: 
          mode: (Default value = 'w')
          **kwargs: 

        Returns:

        '''
        buffer_io = self.__make_fasta_io(**kwargs)
        if isinstance(file,IOBase):
            file_handle = file
        elif isinstance(file,str):
            file_handle = open(file, mode=mode)
        else:
            raise TypeError('`file` has invalid type.')
        copyfileobj(buffer_io, file_handle)
        buffer_io.close()

    def get_string_as(self,**kwargs):
        '''

        Args:
          **kwargs: 

        Returns:

        '''
        buffer_io = self.__make_fasta_io(**kwargs)
        ret = buffer_io.getvalue()
        buffer_io.close()
        return ret

    def __make_fasta_io(self, **kwargs):
        buffer_io = StringIO()
        for sequence in self.__sequences:
            sequence.write(buffer_io, mode='a',**kwargs)
        buffer_io.seek(0)
        return buffer_io

    @classmethod
    def from_buckled(cls, sequences, buckled_pack, **kwargs):
        '''

        Args:
          sequences: 
          buckled_pack: 
          **kwargs: 

        Returns:

        '''
        if not isinstance(buckled_pack,dict):
            raise TypeError('`buckled_pack` must have dict type.')
        tmp_multiseq = cls(sequences,buckled=True,**kwargs)
        tmp_multiseq.restore_buckle(buckled_pack)
        return tmp_multiseq

    @property
    def count(self):
        ''' '''
        return len(self.__sequences)

    @property
    def metadata(self):
        ''' '''
        return self.__metadata

    @property
    def mode(self):
        ''' '''
        return self.__mode

    @property
    def skbio_mode(self):
        ''' '''
        return self.__skbio_mode

    @property
    def sequences(self):
        ''' '''
        return  self.__sequences

    @property
    def name(self):
        ''' '''
        return self.__name

    @property
    def is_alignment(self):
        ''' '''
        return self.__aligned

    @property
    def is_buckled(self):
        ''' '''
        return self.__buckled

    @property
    def index(self):
        ''' '''
        return self.__indices




