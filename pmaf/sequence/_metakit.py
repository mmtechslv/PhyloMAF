from abc import ABC,abstractmethod

class SequenceBackboneMetabase(ABC):
    """ """

    @property
    @abstractmethod
    def metadata(self):
        """ """
        pass

    @property
    @abstractmethod
    def mode(self):
        """ """
        pass

    @property
    @abstractmethod
    def skbio_mode(self):
        """ """
        pass

    @property
    @abstractmethod
    def name(self):
        """ """
        pass

    @property
    @abstractmethod
    def is_buckled(self):
        """ """
        pass

    @abstractmethod
    def write(self,file,**kwargs):
        """

        Parameters
        ----------
        file :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_string_as(self,**kwargs):
        """

        Parameters
        ----------
        **kwargs :
            

        Returns
        -------

        """
        pass


class NucleotideMetabase(SequenceBackboneMetabase):
    """ """

    @abstractmethod
    def buckle_by_uid(self,tmp_uid):
        """

        Parameters
        ----------
        tmp_uid :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def unbuckle_uid(self):
        """ """
        pass

    @abstractmethod
    def restore_buckle(self,packed_metadata):
        """

        Parameters
        ----------
        packed_metadata :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def complement(self):
        """ """
        pass

    @abstractmethod
    def copy(self):
        """ """
        pass

    @classmethod
    @abstractmethod
    def read(cls, file, name=None, metadata=None, mode='DNA', **kwargs):
        """

        Parameters
        ----------
        file :
            
        name :
            (Default value = None)
        metadata :
            (Default value = None)
        mode :
            (Default value = 'DNA')
        **kwargs :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def skbio(self):
        """ """
        pass

    @property
    @abstractmethod
    def text(self):
        """ """
        pass

    @property
    @abstractmethod
    def length(self):
        """ """
        pass


class MultiSequenceMetabase(SequenceBackboneMetabase):
    """ """
    @abstractmethod
    def to_skbio_msa(self, indices):
        """

        Parameters
        ----------
        indices :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def buckle_for_alignment(self):
        """ """
        pass

    @abstractmethod
    def restore_buckle(self,packed_metadata):
        """

        Parameters
        ----------
        packed_metadata :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_iter(self, method):
        """

        Parameters
        ----------
        method :
            

        Returns
        -------

        """
        pass

    @classmethod
    @abstractmethod
    def from_buckled(cls, sequences, buckled_pack, **kwargs):
        """

        Parameters
        ----------
        sequences :
            
        buckled_pack :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def count(self):
        """ """
        pass

    @property
    @abstractmethod
    def sequences(self):
        """ """
        pass

    @abstractmethod
    def get_consensus(self,indices):
        """

        Parameters
        ----------
        indices :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_subset(self,indices):
        """

        Parameters
        ----------
        indices :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def index(self):
        """ """
        pass

    @property
    @abstractmethod
    def is_alignment(self):
        """ """
        pass


class MultiSequenceStreamBackboneMetabase(ABC):
    """ """

    @abstractmethod
    def __init__(self,filepath, mode, aligned, name,compressor):
        pass

    @abstractmethod
    def append_sequence(self,sequence):
        """

        Parameters
        ----------
        sequence :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def extend_multiseq(self,multiseq):
        """

        Parameters
        ----------
        multiseq :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def append_string(self,name,mode,sequence_str,metadata_dict):
        """

        Parameters
        ----------
        name :
            
        mode :
            
        sequence_str :
            
        metadata_dict :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_sequence_by_acc(self,acc_number):
        """

        Parameters
        ----------
        acc_number :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_multiseq_by_accs(self, acc_numbers):
        """

        Parameters
        ----------
        acc_numbers :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def name(self):
        """ """
        pass

    @property
    @abstractmethod
    def mode(self):
        """ """
        pass

    @property
    @abstractmethod
    def count(self):
        """ """
        pass

    @property
    @abstractmethod
    def summarize(self):
        """ """
        pass

    @property
    @abstractmethod
    def accession_numbers(self):
        """ """
        pass


