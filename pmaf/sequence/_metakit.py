from abc import ABC,abstractmethod

class SequenceBackboneMetabase(ABC):

    @property
    @abstractmethod
    def metadata(self):
        pass

    @property
    @abstractmethod
    def mode(self):
        pass

    @property
    @abstractmethod
    def skbio_mode(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def is_buckled(self):
        pass

    @abstractmethod
    def write(self,file,**kwargs):
        pass

    @abstractmethod
    def get_string_as(self,**kwargs):
        pass


class NucleotideMetabase(SequenceBackboneMetabase):

    @abstractmethod
    def buckle_by_uid(self,tmp_uid):
        pass

    @abstractmethod
    def unbuckle_uid(self):
        pass

    @abstractmethod
    def restore_buckle(self,packed_metadata):
        pass

    @abstractmethod
    def complement(self):
        pass

    @abstractmethod
    def copy(self):
        pass

    @classmethod
    @abstractmethod
    def read(cls, file, name=None, metadata=None, mode='DNA', **kwargs):
        pass

    @property
    @abstractmethod
    def skbio(self):
        pass

    @property
    @abstractmethod
    def text(self):
        pass

    @property
    @abstractmethod
    def length(self):
        pass


class MultiSequenceMetabase(SequenceBackboneMetabase):
    @abstractmethod
    def to_skbio_msa(self, indices):
        pass

    @abstractmethod
    def buckle_for_alignment(self):
        pass

    @abstractmethod
    def restore_buckle(self,packed_metadata):
        pass

    @abstractmethod
    def get_iter(self, method):
        pass

    @classmethod
    @abstractmethod
    def from_buckled(cls, sequences, buckled_pack, **kwargs):
        pass

    @property
    @abstractmethod
    def count(self):
        pass

    @property
    @abstractmethod
    def sequences(self):
        pass

    @abstractmethod
    def get_consensus(self,indices):
        pass

    @abstractmethod
    def get_subset(self,indices):
        pass

    @property
    @abstractmethod
    def index(self):
        pass

    @property
    @abstractmethod
    def is_alignment(self):
        pass


class MultiSequenceStreamBackboneMetabase(ABC):

    @abstractmethod
    def __init__(self,filepath, mode, aligned, name,compressor):
        pass

    @abstractmethod
    def append_sequence(self,sequence):
        pass

    @abstractmethod
    def extend_multiseq(self,multiseq):
        pass

    @abstractmethod
    def append_string(self,name,mode,sequence_str,metadata_dict):
        pass

    @abstractmethod
    def get_sequence_by_acc(self,acc_number):
        pass

    @abstractmethod
    def get_multiseq_by_accs(self, acc_numbers):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def mode(self):
        pass

    @property
    @abstractmethod
    def count(self):
        pass

    @property
    @abstractmethod
    def summarize(self):
        pass

    @property
    @abstractmethod
    def accession_numbers(self):
        pass


