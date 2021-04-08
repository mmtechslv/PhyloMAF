from abc import ABC,abstractmethod

class DockerBackboneMetabase(ABC):

    @abstractmethod
    def wrap_meta(self):
        pass

    @abstractmethod
    def get_subset(self,indices,exclude_missing):
        pass

    @abstractmethod
    def get_iterator(self,indices,exclude_missing):
        pass

    @property
    @abstractmethod
    def singleton(self):
        pass

    @property
    @abstractmethod
    def empty(self):
        pass

    @property
    @abstractmethod
    def data(self):
        pass

    @property
    @abstractmethod
    def missing(self):
        pass

    @property
    @abstractmethod
    def valid(self):
        pass

    @property
    @abstractmethod
    def _transit(self):
        pass

    @property
    @abstractmethod
    def metadata(self):
        pass

    @metadata.setter
    @abstractmethod
    def metadata(self, value):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        pass

    @property
    @abstractmethod
    def index(self):
        pass

    @property
    @abstractmethod
    def count(self):
        pass

class DockerIdentifierMetabase(DockerBackboneMetabase):
    @abstractmethod
    def to_array(self, indices, exclude_missing):
        pass

class DockerTaxonomyMetabase(DockerBackboneMetabase):
    @abstractmethod
    def get_avail_ranks(self,indices):
        pass

    @abstractmethod
    def to_dataframe(self, indices, ranks):
        pass

class DockerPhylogenyMetabase(DockerBackboneMetabase):

    @abstractmethod
    def get_node_names(self,indices):
        pass

    @abstractmethod
    def get_tip_names(self,indices):
        pass

class DockerSequenceMetabase(DockerBackboneMetabase):
    @abstractmethod
    def to_multiseq(self, indices):
        pass

    @abstractmethod
    def get_records(self,indices):
        pass

    @abstractmethod
    def get_stats(self, indices):
        pass

    @property
    @abstractmethod
    def mode(self):
        pass

    @property
    @abstractmethod
    def aligned(self):
        pass

class DockerAccessionMetabase(DockerBackboneMetabase):
    @property
    @abstractmethod
    def sources(self):
        pass

    @abstractmethod
    def to_identifier_by_src(self, source, exclude_missing):
        pass