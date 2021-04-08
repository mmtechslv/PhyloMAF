from abc import ABC, abstractmethod

class MediatorBackboneMetabase(ABC):

    @abstractmethod
    def verify_factor(self,factor):
        pass

    @abstractmethod
    def reconfig(self,name,value):
        pass

    @property
    @abstractmethod
    def state(self):
        pass

    @property
    @abstractmethod
    def client(self):
        pass

    @property
    @abstractmethod
    def configs(self):
        pass

class MediatorAccessionMetabase(MediatorBackboneMetabase):

    @abstractmethod
    def get_accession_by_identifier(self, docker, factor, **kwargs):
        pass

    @abstractmethod
    def get_identifier_by_accession(self, docker, factor, **kwargs):
        pass


class MediatorSequenceMetabase(MediatorBackboneMetabase):
    @abstractmethod
    def get_sequence_by_identifier(self, docker, factor, **kwargs):
        pass

    @abstractmethod
    def get_identifier_by_sequence(self, docker, factor, **kwargs):
        pass

class MediatorPhylogenyMetabase(MediatorBackboneMetabase):
    @abstractmethod
    def get_phylogeny_by_identifier(self, docker, factor, **kwargs):
        pass

    @abstractmethod
    def get_identifier_by_phylogeny(self, docker, factor, **kwargs):
        pass

class MediatorTaxonomyMetabase(MediatorBackboneMetabase):
    @abstractmethod
    def get_taxonomy_by_identifier(self, docker, factor, **kwargs):
        pass

    @abstractmethod
    def get_identifier_by_taxonomy(self, docker, factor, **kwargs):
        pass
