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

    @property
    @abstractmethod
    def xrid(self):
        pass


class BiomeSampleMetabase(BiomeBackboneMetabase):

    @property
    @abstractmethod
    def xsid(self):
        pass
