from abc import ABC,abstractmethod
from pmaf.classifier._metakit import ClassifierBackboneMetabase

class DhnbClassifierBackboneMetabase(ABC):
    @classmethod
    @abstractmethod
    def build(cls, *args, **kwargs):
        pass

    @abstractmethod
    def close(self, **kwargs):
        pass

    @property
    @abstractmethod
    def state(self):
        pass

    @property
    @abstractmethod
    def passed_rids(self):
        pass

    @property
    @abstractmethod
    def excluded_rids(self):
        pass

    @property
    @abstractmethod
    def chunked(self):
        pass

    @property
    @abstractmethod
    def kmer_sizes(self):
        pass

    @property
    @abstractmethod
    def xrid(self):
        pass

    @property
    @abstractmethod
    def xmritem(self):
        pass

    @property
    @abstractmethod
    def xmhitem(self):
        pass

    @property
    @abstractmethod
    def rmeta(self):
        pass

    @property
    @abstractmethod
    def hmeta(self):
        pass

    @property
    @abstractmethod
    def basefile_fp(self):
        pass

    @abstractmethod
    def refine(self,method,*args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def verify_basefile(self, basefile_fp):
        pass

class DhnbClassifierBaseMetabase(DhnbClassifierBackboneMetabase,ClassifierBackboneMetabase):
    @abstractmethod
    def __init__(self,classifier_fp, database_instance, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def verify_database(self, database_instance):
        pass

    @classmethod
    @abstractmethod
    def verify_dataset(self, dataset_instance):
        pass

    @property
    @abstractmethod
    def xtid(self):
        pass

    @property
    @abstractmethod
    def tmeta(self):
        pass

    @property
    @abstractmethod
    def xmtitem(self):
        pass

class DhnbClassifierDatasetMetabase(DhnbClassifierBackboneMetabase):
    @abstractmethod
    def __init__(self, dataset_fp, seq_record_df, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def verify_classifier(self, classifier_instance):
        pass

    @property
    @abstractmethod
    def records(self):
        pass




