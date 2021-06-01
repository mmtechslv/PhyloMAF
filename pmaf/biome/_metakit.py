from abc import ABC, abstractmethod

class BiomeBackboneMetabase(ABC):

    @abstractmethod
    def _repr_appendage__(self):
        pass

    @abstractmethod
    def copy(self):
        pass

    @property
    @abstractmethod
    def shape(self):
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
    def name(self,value):
        pass


class BiomeFeatureMetabase(BiomeBackboneMetabase):

    def get_feature_ids(self, dtype=None):
        """This function and its sample twin is a rescue method to fix RepPhylogeny index problem. """
        if dtype is None:
            return self.xrid
        else:
            return self.xrid.astype(dtype)

    @property
    @abstractmethod
    def xrid(self):
        pass


class BiomeSampleMetabase(BiomeBackboneMetabase):

    def get_sample_ids(self, dtype):
        """This function and its sample twin is a rescue method to fix RepPhylogeny index problem. """
        if dtype is None:
            return self.xsid
        else:
            return self.xsid.astype(dtype)

    @property
    @abstractmethod
    def xsid(self):
        pass
